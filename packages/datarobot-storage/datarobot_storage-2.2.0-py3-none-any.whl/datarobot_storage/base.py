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
from __future__ import division

import abc
import inspect
import io
import logging
import os
import tempfile
from io import SEEK_CUR
from io import SEEK_END
from io import SEEK_SET
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import TypeVar

from datarobot_storage.put_generator import PutGenerator
from datarobot_storage.utils import safe_make_dir
from datarobot_storage.utils import try_file_remove

logger = logging.getLogger(__name__)


class StorageGenerator(object):
    def __init__(self, generator_factory=None):
        self._file_exists = generator_factory is not None
        self._generator_factory = generator_factory or self._empty_generator_factory
        self._decorators = []

    @staticmethod
    def _empty_generator_factory(*args, **kwargs):
        # Return an empty generator
        return iter(())

    @property
    def file_exists(self):
        return self._file_exists

    def push_decorator(self, decorator):
        """
        Adds a decorator to the storage generator.

        Parameters
        ----------
        decorator : Function that accepts a generator and returns a generator

        """
        self._decorators.append(decorator)

    def __iter__(self):
        generator_factory = self._generator_factory

        for decorator in self._decorators:
            generator_factory = decorator(generator_factory)

        return generator_factory()


class SeekableKeyInterface(abc.ABC):
    @abc.abstractmethod
    def get_range(self, offset: int, size: int) -> bytes:
        """Return bytes, starting at `offset` with at most `size` bytes."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def size(self) -> int:
        raise NotImplementedError


class SeekableStorage(io.RawIOBase):
    """Seekable file-like object interface for partial reads.

    This class is useful in scenarios where transferring the entire file
    data is unnecessary or wasteful. Example: The data is indexed and stored
    in a large binary file. During retrieval, we precisely know the byte
    range of the data to be fetched. In such cases, we aim to retrieve this
    specific data without downloading the entire file or iterating over it.
    The SeekableStorage is implemented for such scenarios.
    """

    def __init__(self, key: SeekableKeyInterface):
        self._key = key
        self._position = 0

    def size(self) -> int:
        return self._key.size

    def tell(self) -> int:
        return self._position

    def seek(self, offset: int, whence: int = SEEK_SET) -> int:
        if whence == SEEK_SET:
            self._position = offset
        elif whence == SEEK_CUR:
            self._position += offset
        elif whence == SEEK_END:
            self._position = self.size() + offset
        else:
            raise ValueError(
                "invalid whence (%r, should be %d, %d, %d)" % (whence, SEEK_SET, SEEK_CUR, SEEK_END)
            )

        return self._position

    def seekable(self) -> bool:
        return True

    def read(self, size: int = -1) -> bytes:
        if self._position == self.size():
            # We read the file till the end, let the iterator know about it
            return b""
        elif size == -1:
            # Read to the end of the file
            offset = self._position
            self.seek(offset=0, whence=SEEK_END)
        else:
            new_position = self._position + size
            if new_position >= self.size():
                return self.read()
            offset, size = self._position, size
            self.seek(offset=size, whence=SEEK_CUR)

        content_bytes = self._key.get_range(offset, size)
        return content_bytes

    def readable(self) -> bool:
        return True


class Storage(abc.ABC):
    """
    Provides cloud-agnostic storage interface for DataRobot services.

    Child classes implement this interface using 3rd-party libraries such as boto3 or azure-storage.
    """

    CHUNK_SIZE: int = 65536  # 64 KB
    local_data_directory: str
    prefix: str

    def __init__(self, *args, prefix='', local_data_directory='', **kwargs):
        super(Storage, self).__init__()
        self.prefix = prefix or ''
        self.local_data_directory = local_data_directory or tempfile.gettempdir()

    def _name(self, name: str) -> str:
        """
        Returns the full path to the object with the given name

        Parameters
        ----------
        name : str
            The name of the object

        Returns
        -------
        path : str
        """
        return os.path.join(self.prefix, name)

    @property
    @abc.abstractmethod
    def client(self) -> Any:
        """
        Native storage client, which can be used to access provider-specific features.

        Returns
        -------
        client : Any
            e.g. boto3.client
        """
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, name: str) -> bool:
        """
        Checks if the object with the given name exists in the storage.

        Parameters
        ----------
        name : str
            The name of the object

        Returns
        -------
        exists : bool
            True if object exists, otherwise False
        """
        raise NotImplementedError

    def exists_and_readable(self, name: str) -> bool:
        """
        Poll that a file exists and that get/get_generator could succeed.

        This should only be used in the very special case of polling for an input file
        before starting a job.  It avoids false positives of non-atomic storage backends
        (eg, HDFS) reporting a file exists before the initial write has completed.

        This must never be used within a job to check or wait for its own input - use
        the `exists` method instead.
        """
        return self.exists(name)

    @abc.abstractmethod
    def list(self, path: str, recursive=False) -> List[str]:
        """
        List all files under the given path

        Parameters
        ----------
        path : str
            Remote path (prefix)
        recursive : bool, optional
            List files in all subdirectories under the given `path`. When this flag is True, the
            output is a list of keys starting from `path`. If this flag is False, the output is a
            list of a direct keys underneath the given `path`

        Examples
        --------
        Given a file hierarchy:
         - some/path
         - some/path/file2.txt
         - some/path/file1.txt
         - some/path/subdirectory
         - some/path/subdirectory/file3.txt

        >>> storage.list('some/path', recursive=False)  # doctest: +SKIP
        subdirectory
        file1.txt
        file2.txt

        >>> storage.list('some/path', recursive=True)  # doctest: +SKIP
        some/path/file1.txt
        some/path/file2.txt
        some/path/subdirectory/file3.txt

        Returns
        -------
        paths : list[str]
            List of file paths
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, name: str, temp_filename: str) -> bool:
        """
        Get content of the remote blob to the local file.

        Parameters
        ----------
        name : str
            File object path on the storage
        temp_filename : str
            Local filename to write blob content to

        Returns
        -------
        result : bool
            True if download succeed, False if download fails or object doesn't exist.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_seekable(self, name: str) -> SeekableStorage:
        """
        Return seekable file-like object for partial reads.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_generator(self, name: str, **kwargs) -> StorageGenerator:
        """
        Return generator that yields objects for partial remote blob reads.

        Parameters
        ----------
        name : str
            File object path on the storage
        kwargs: unknown

        Returns
        -------
        generator : StorageGenerator
            If remote object not exists, log error and return StorageGenerator();
            otherwise, return StorageGenerator(fn), where fn allows offset=0
        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, name: str, source: str) -> bool:
        """
        Put local file to the remote storage

        Parameters
        ----------
        name : str
            Remote filename
        source : str
            Local filename to upload to remote storage

        Returns
        -------
        result : bool
            True if file was successfully put, otherwise False.
        """
        raise NotImplementedError

    def put_generator(self, name: str, source: PutGenerator) -> bool:
        """
        Stream data from a PutGenerator directly to backend storage.

        Note that, like the `put` method, a boolean status is returned and
        no exceptions are thrown in case of error.

        The default implementation stores data in a local temporary file,
        then calls `put`.  So far only a few backends have been updated to
        implement this method, see PLT-841 and PLT-831 for details.

        Parameters
        ----------
        name : string
            Remote filename
        source : PutGenerator
            Wrapper that provides stream of data to be put to storage

        Returns
        ------
        success : bool
            True if file was successfully put, otherwise False.
        """
        safe_make_dir(self.local_data_directory)
        with tempfile.NamedTemporaryFile(dir=self.local_data_directory) as tf:
            try:
                while True:
                    buf = source.read(self.CHUNK_SIZE)
                    if not buf:
                        break
                    tf.write(buf)
                tf.flush()
            except Exception:
                logger.error(
                    'Failed to read source stream', exc_info=True, extra={'file_name': name}
                )
                return False
            success = self.put(name, tf.name)
        return success

    @abc.abstractmethod
    def copy(self, name: str, new_name: str) -> bool:
        """
        Create duplicate of remote file withing the storage

        Parameters
        ----------
        name : str
            File object path on the storage
        new_name : str
            Path to create a copy at

        Returns
        -------
        result : bool
            True if operation succeed, False if fails or source object doesn't exist.
        """
        raise NotImplementedError

    def move(self, name: str, local_filename: str) -> bool:
        """
        Put local_filename into storage and remove local_filename

        Parameters
        ----------
        name : str
            File object path on the storage
        local_filename : str
            Local filename to upload to remote storage

        Returns
        -------
        result : bool
            True if operation succeed, False otherwise.
        """
        put = self.put(name, local_filename)
        if put:
            try_file_remove(local_filename)

        return put

    @abc.abstractmethod
    def delete(self, name: str) -> bool:
        """
        Delete object on the storage.

        Parameters
        ----------
        name : str
            Storage object path to be deleted.

        Returns
        -------
        result : bool
            True if deleted, False if deletion fails or object doesn't exist.
        """
        raise NotImplementedError

    def delete_batch(self, name_iter: Iterable, batch_size: Optional[int] = None) -> None:
        """
        Efficiently delete many files on storage.

        Parameters
        ----------
        name_iter : iterable
            An iterable yielding file names to be deleted
        batch_size: int or None
            Amount of blobs to be deleted per request

        Returns
        -------
        None
        """
        for name in name_iter:
            self.delete(name)

    @abc.abstractmethod
    def delete_all(self, name: str) -> None:
        """
        Delete all files on storage under specified path.

        This is useful as a utility and for local development.
        It is NOT recommended for use in production.

        Parameters
        ----------
        name : str
            Path on the storage

        Returns
        -------
        None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def url(self, name: str, expires_in: Optional[int] = None) -> Optional[str]:
        """
        Return a URL which client could use to directly download the file.

        Implementations should check for file object existence and return None if it doesn't exist.
        Otherwise, return a string containing a unique resource location for the object
        where the protocol of the URL will be implementation specific.
        Also, if link/file has limited access, provide expiration time in seconds.

        Returns
        -------
        url : Optional[str]
            URL which could be used to directly download the blob, None if object doesn't exist
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_size(self, name: str) -> int:
        """
        The size of the file in bytes.

        Parameters
        ----------
        name : str
            File object path on the storage

        Returns
        -------
        size : int
            Size in bytes, '0' if file doesn't exist.
        """
        raise NotImplementedError


class AsyncStorage:
    @property
    async def client(self) -> Any:
        raise NotImplementedError

    async def exists(self, name: str) -> bool:
        """
        Checks if the object with the given name exists in the storage.

        Parameters
        ----------
        name : str
            The name of the object

        Returns
        -------
        exists : bool
            True if object exists, otherwise False
        """
        raise NotImplementedError

    async def exists_and_readable(self, name: str) -> bool:
        """
        Poll that a file exists and that get/get_generator could succeed.

        This should only be used in the very special case of polling for an input file
        before starting a job.  It avoids false positives of non-atomic storage backends
        (eg, HDFS) reporting a file exists before the initial write has completed.

        This must never be used within a job to check or wait for its own input - use
        the `exists` method instead.
        """
        raise NotImplementedError

    async def list(self, path: str, recursive=False) -> List[str]:
        """
        List all files under the given path

        Parameters
        ----------
        path : str
            Remote path (prefix)
        recursive : bool, optional
            List files in all subdirectories under the given `path`. When this flag is True, the
            output is a list of keys starting from `path`. If this flag is False, the output is a
            list of a direct keys underneath the given `path`

        Examples
        --------
        Given a file hierarchy:
         - some/path
         - some/path/file2.txt
         - some/path/file1.txt
         - some/path/subdirectory
         - some/path/subdirectory/file3.txt

        >>> storage.list('some/path', recursive=False)  # doctest: +SKIP
        subdirectory
        file1.txt
        file2.txt

        >>> storage.list('some/path', recursive=True)  # doctest: +SKIP
        some/path/file1.txt
        some/path/file2.txt
        some/path/subdirectory/file3.txt

        Returns
        -------
        paths : list[str]
            List of file paths
        """
        raise NotImplementedError

    async def get(self, name: str, temp_filename: str) -> bool:
        """
        Get content of the remote blob to the local file.

        Parameters
        ----------
        name : str
            File object path on the storage
        temp_filename : str
            Local filename to write blob content to

        Returns
        -------
        result : bool
            True if download succeed, False if download fails or object doesn't exist.
        """
        raise NotImplementedError

    async def get_seekable(self, name: str) -> SeekableStorage:
        """Return seekable file-like object for partial reads."""
        raise NotImplementedError

    async def get_generator(self, name: str, **kwargs) -> StorageGenerator:
        """
        Return generator that yields objects for partial remote blob reads.

        Parameters
        ----------
        name : str
            File object path on the storage
        kwargs: unknown

        Returns
        -------
        generator : StorageGenerator
            If remote object not exists, log error and return StorageGenerator();
            otherwise, return StorageGenerator(fn), where fn allows offset=0
        """
        raise NotImplementedError

    async def put(self, name: str, source: str) -> bool:
        """
        Put local file to the remote storage

        Parameters
        ----------
        name : str
            Remote filename
        source : str
            Local filename to upload to remote storage

        Returns
        -------
        result : bool
            True if file was successfully put, otherwise False.
        """
        raise NotImplementedError

    async def put_generator(self, name: str, source: PutGenerator) -> bool:
        """
        Stream data from a PutGenerator directly to backend storage.

        Note that, like the `put` method, a boolean status is returned and
        no exceptions are thrown in case of error.

        The default implementation stores data in a local temporary file,
        then calls `put`.  So far only a few backends have been updated to
        implement this method, see PLT-841 and PLT-831 for details.

        Parameters
        ----------
        name : string
            Remote filename
        source : PutGenerator
            Wrapper that provides stream of data to be put to storage

        Returns
        ------
        success : bool
            True if file was successfully put, otherwise False.
        """
        raise NotImplementedError

    async def copy(self, name: str, new_name: str) -> bool:
        """
        Create duplicate of remote file withing the storage

        Parameters
        ----------
        name : str
            File object path on the storage
        new_name : str
            Path to create a copy at

        Returns
        -------
        result : bool
            True if operation succeed, False if fails or source object doesn't exist.
        """
        raise NotImplementedError

    async def move(self, name: str, local_filename: str) -> bool:
        """
        Put local_filename into storage and remove local_filename

        Parameters
        ----------
        name : str
            File object path on the storage
        local_filename : str
            Local filename to upload to remote storage

        Returns
        -------
        result : bool
            True if operation succeed, False otherwise.
        """
        raise NotImplementedError

    async def delete(self, name: str) -> bool:
        """
        Delete object on the storage.

        Parameters
        ----------
        name : str
            Storage object path to be deleted.

        Returns
        -------
        result : bool
            True if deleted, False if deletion fails or object doesn't exist.
        """
        raise NotImplementedError

    async def delete_batch(self, name_iter: Iterable, batch_size: Optional[int] = None) -> None:
        """
        Efficiently delete many files on storage.

        Parameters
        ----------
        name_iter : iterable
            An iterable yielding file names to be deleted
        batch_size: int or None
            Amount of blobs to be deleted per request

        Returns
        -------
        None
        """

    async def delete_all(self, name: str) -> None:
        """
        Delete all files on storage under specified path.

        This is useful as a utility and for local development.
        It is NOT recommended for use in production.

        Parameters
        ----------
        name : str
            Path on the storage

        Returns
        -------
        None
        """
        raise NotImplementedError

    async def url(self, name: str, expires_in: Optional[int] = None):
        """
        Return a URL which client could use to directly download the file.

        Implementations should check for file object existence and return None if it doesn't exist.
        Otherwise, return a string containing a unique resource location for the object
        where the protocol of the URL will be implementation specific.
        Also, if link/file has limited access, provide expiration time in seconds.

        Returns
        -------
        url : Optional[str]
            URL which could be used to directly download the blob, None if object doesn't exist
        """
        raise NotImplementedError

    async def file_size(self, name: str):
        """
        The size of the file in bytes.

        Parameters
        ----------
        name : str
            File object path on the storage

        Returns
        -------
        size : int
            Size in bytes, '0' if file doesn't exist.
        """
        raise NotImplementedError


StorageType = TypeVar('StorageType', Storage, AsyncStorage)
