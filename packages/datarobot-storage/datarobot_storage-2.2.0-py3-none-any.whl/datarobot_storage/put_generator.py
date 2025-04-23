#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc. Confidential.
#
# This is unpublished proprietary source code of DataRobot, Inc.
# and its affiliates.
#
# The copyright notice above does not evidence any actual or intended
# publication of such source code.
#
# This file and its contents are subject to DataRobot Tool and Utility Agreement.
# For details, see
# https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
from __future__ import absolute_import

import collections
import gzip
import hashlib
import io
import logging

logger = logging.getLogger(__name__)


class PutGenerator(io.RawIOBase):
    """Base class providing bytes for storage backends to be able to
    put data from a stream.

    This class serves as a bridge between various sources and backends.
    """

    def read(self, nbytes=None):
        """Read up to nbytes from the underlying source.

        Since io.IOBase explicitly does not define read signature, it is
        defined here to best support streaming data to a storage backend
        while avoiding timeouts: the backend should only request what it
        can write in a few seconds, and the frontend may reduce that to
        what it can read in a few seconds.  Note that "a few seconds" is
        a rough 10% of a timeout reported by the underlying transports.

        Parameters
        ----------
        nbytes : int, optional
            Maximum number of bytes to read.

        Returns
        -------
        data: bytes
            One or more bytes of input read before timing out, or
            zero-length bytes for EOF.

        Raises
        ------
        Any exception indicates an error (or timeout) reading data.
        """
        raise NotImplementedError()


class FilePutGenerator(PutGenerator):
    """Implementation of PutGenerator that reads from any file-like object."""

    DEFAULT_CHUNK_SIZE = 64 * 1024  # Patch-able for testing.

    def __init__(self, fobj):
        super(FilePutGenerator, self).__init__()
        self._fobj = fobj
        self._bytes_read = 0

    def read(self, nbytes=None):
        response = self._fobj.read(nbytes or self.DEFAULT_CHUNK_SIZE)
        self._bytes_read += len(response)
        return response

    def bytes_read(self):
        """Returns the total number of actually read bytes so far"""
        return self._bytes_read


class HashingPutGeneratorDecorator(PutGenerator):
    """Simple proxying decorator that hashes proxied i/o on-the-fly w/o modifying it."""

    def __init__(self, delegate_put_generator, hash_algorithm):
        """
        Parameters
        ----------
        delegate_put_generator : `PutGenerator`
        hash_algorithm : str
            algorithm name compatible with std hashlib lib.
            In theory, any of `hashlib.algorithms_guaranteed` should always work here except md5,
            because this algorithm is not allowed in FedRamp/FIPS environments and is forbidden.
        """

        if hash_algorithm == 'md5':
            raise RuntimeError('Use of MD5 hash algorithm is not allowed')

        super(HashingPutGeneratorDecorator, self).__init__()
        self._input = delegate_put_generator
        self._hasher = hashlib.new(hash_algorithm)

    def read(self, nbytes=None):
        response = self._input.read(nbytes)
        self._hasher.update(response)
        return response

    def hexdigest(self):
        """Return hash of the data read so far"""

        return self._hasher.hexdigest()


class GzipPutGeneratorDecorator(PutGenerator):
    """Decorator that gzips input stream on-the-fly.

    Taken from and slightly amended for readability:
    https://stackoverflow.com/questions/2192529/python-creating-a-streaming-gzipd-file-like/2193508

    It also exposes the number of actually produced bytes.
    """

    DEFAULT_CHUNK_SIZE = 64 * 1024

    class Buffer(object):
        """Buffer for efficient storing and retrieving chunks of compressed data."""

        def __init__(self):
            # every element is a byte array of random size
            self._buf = collections.deque()
            self._size = 0

        def __len__(self):
            return self._size

        def write(self, data):
            self._buf.append(data)
            self._size += len(data)

        def read(self, size=-1):
            if size < 0:
                size = self._size
            ret_list = []
            # read and pop from the head until the requested size is fulfilled
            while size > 0 and len(self._buf):
                s = self._buf.popleft()
                size -= len(s)
                ret_list.append(s)
            # keep the remainder in the head for the next read
            if size < 0:
                ret_list[-1], remainder = ret_list[-1][:size], ret_list[-1][size:]
                self._buf.appendleft(remainder)
            ret = b''.join(ret_list)
            self._size -= len(ret)
            return ret

        def flush(self):
            pass

        def close(self):
            pass

    def __init__(self, delegate_put_generator, compresslevel=6):
        super(GzipPutGeneratorDecorator, self).__init__()

        self._input = delegate_put_generator
        self._compressed_data_buf = GzipPutGeneratorDecorator.Buffer()  # stores compressed data
        self._gzip = gzip.GzipFile(
            None, compresslevel=compresslevel, mode='wb', fileobj=self._compressed_data_buf
        )
        self._bytes_read = 0

    def _try_read_from_source_and_compress(self, nbytes):
        if self._gzip.closed:
            return None
        to_compress = self._input.read(nbytes)
        if not to_compress:
            # EOF: nothing left to compress
            # closing GZIP producer may generally speaking produce output bytes
            # so it is important to read from the buffer below rather than return prematurely
            self._gzip.close()
        else:
            # compress to the buffer
            self._gzip.write(to_compress)

    def read(self, nbytes=None):
        """Read from raw uncompressed input and return at most `nbytes` of compressed data.

        Maintains compressed data buffer to store already compressed but not yet returned data.
        Depending on buffer's current size one of the two scenarios may occur:
        - `0 <= len(buffer) < nbytes`: it will keep reading `nbytes` at a time from the source
            until there is something to return to not confuse it with EOF.
        - `len(buffer) >= nbytes`: it will not attempt to read from source at all and just
            return the head of the buffer of size `nbytes`.

        Parameters
        ----------
        nbytes : integer
            hint for the number of bytes to read from uncompressed source (`delegate_put_generator`)
            Defaults to `GzipPutGeneratorDecorator.DEFAULT_CHUNK_SIZE`

        Returns
        -------
        compressed data of max size `nbytes` : bytearray
        """
        nbytes = nbytes or GzipPutGeneratorDecorator.DEFAULT_CHUNK_SIZE

        buffer = self._compressed_data_buf

        # The buffer may contain previously unread data generally speaking
        compressed = buffer.read(nbytes)

        # If the size of the leftover is strictly smaller than `nbytes`,
        # attempt to read from source just once rather than return prematurely
        # since that is what clients may expect generally speaking.
        if 0 < len(compressed) < nbytes:
            self._try_read_from_source_and_compress(nbytes)
            compressed += self._compressed_data_buf.read(nbytes - len(compressed))

        # Keep reading from the input until the EOF or until there is at least something to return.
        # Generally speaking each read-and-compress cycle produces less bytes than was requested,
        # in other words the implementation treats `nbytes` as the number of bytes read from
        # the source, rather the number of bytes to produce.
        # Note that the loop is needed because in case compression does not produce any new
        # bytes, it is important to continue reading so that it does not appear as EOF
        # to the reader.
        while not compressed and not self._gzip.closed:
            self._try_read_from_source_and_compress(nbytes)
            compressed = self._compressed_data_buf.read(nbytes)

        self._bytes_read += len(compressed)
        return compressed

    def bytes_read(self):
        """Returns the number of produced (compressed) data bytes"""

        return self._bytes_read

    def close(self):
        self._gzip.close()
