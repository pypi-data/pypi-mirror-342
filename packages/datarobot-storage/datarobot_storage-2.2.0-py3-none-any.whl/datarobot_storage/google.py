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

import base64
import binascii
import collections
import datetime
import hashlib
import io
import json
import logging
import os
import re
import tempfile
import time
from collections.abc import Mapping
from typing import Iterable
from typing import List
from typing import Optional
from urllib.parse import quote

import google.api_core.exceptions  # GoogleAPIError and derived errors.
import google.auth
import google.auth.exceptions  # GoogleAuthError and derived errors.
import google.auth.transport.requests
import google.cloud.storage  # pylint: disable=import-error
import google.resumable_media.requests
from google.oauth2 import service_account

from datarobot_storage.base import SeekableKeyInterface
from datarobot_storage.base import SeekableStorage
from datarobot_storage.base import Storage
from datarobot_storage.base import StorageGenerator
from datarobot_storage.utils import StorageUtilsMixin
from datarobot_storage.utils import cached_property

SIGNED_URL_LIFETIME = 600  # Seconds, as seen in S3Storage.

logger = logging.getLogger(__name__)


class GoogleStorageCredentialsSource(object):
    PATH = 'path'
    CONTENTS = 'contents'
    ADC = 'adc'  # "Application Default Credentials"

    @classmethod
    def all(cls) -> List[str]:
        return [cls.PATH, cls.CONTENTS, cls.ADC]


def google_storage_factory(*args, **kwargs):
    """Factory method to create a GoogleStorage object."""
    return GoogleStorage(*args, **kwargs)


# This function borrowed from here:
#       https://cloud.google.com/storage/docs/access-control/signing-urls-manually#python-sample
# and reformatted a bit to meet local style.
def generate_signed_url_with_keyfile(
    service_account_file,
    bucket_name,
    blob_name,
    subresource=None,
    expiration=SIGNED_URL_LIFETIME,
    http_method='GET',  # Implies read-only(?)
    query_parameters=None,
    headers=None,
) -> str:
    escaped_blob_name = quote(blob_name, safe='/~')
    canonical_uri = '/{}'.format(escaped_blob_name)

    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    request_timestamp = datetime_now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = datetime_now.strftime('%Y%m%d')

    google_credentials = service_account.Credentials.from_service_account_file(service_account_file)
    client_email = google_credentials.service_account_email
    credential_scope = '{}/auto/storage/goog4_request'.format(datestamp)
    credential = '{}/{}'.format(client_email, credential_scope)

    if headers is None:
        headers = dict()
    host = '{}.storage.googleapis.com'.format(bucket_name)
    headers['host'] = host

    canonical_headers = ''
    ordered_headers = collections.OrderedDict(sorted(headers.items()))
    for k, v in ordered_headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += '{}:{}\n'.format(lower_k, strip_v)

    signed_headers = ''
    for k, _ in ordered_headers.items():
        lower_k = str(k).lower()
        signed_headers += '{};'.format(lower_k)
    signed_headers = signed_headers[:-1]  # remove trailing ';'

    if query_parameters is None:
        query_parameters = dict()
    query_parameters['X-Goog-Algorithm'] = 'GOOG4-RSA-SHA256'
    query_parameters['X-Goog-Credential'] = credential
    query_parameters['X-Goog-Date'] = request_timestamp
    query_parameters['X-Goog-Expires'] = expiration
    query_parameters['X-Goog-SignedHeaders'] = signed_headers
    if subresource:
        query_parameters[subresource] = ''

    canonical_query_string = ''
    ordered_query_parameters = collections.OrderedDict(sorted(query_parameters.items()))
    for k, v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe='')
        encoded_v = quote(str(v), safe='')
        canonical_query_string += '{}={}&'.format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1]  # remove trailing ';'

    canonical_request = '\n'.join(
        [
            http_method,
            canonical_uri,
            canonical_query_string,
            canonical_headers,
            signed_headers,
            'UNSIGNED-PAYLOAD',
        ]
    )

    canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()

    string_to_sign = '\n'.join(
        ['GOOG4-RSA-SHA256', request_timestamp, credential_scope, canonical_request_hash]
    )

    signature = binascii.hexlify(google_credentials.signer.sign(string_to_sign)).decode()

    scheme_and_host = '{}://{}'.format('https', host)
    signed_url = '{}{}?{}&x-goog-signature={}'.format(
        scheme_and_host, canonical_uri, canonical_query_string, signature
    )

    return signed_url


def generate_signed_url_with_gce(
    bucket_name,
    blob_name,
    subresource=None,
    expiration=SIGNED_URL_LIFETIME,
    http_method='GET',
    query_parameters=None,
    headers=None,
):  # pylint: disable=unused-argument
    # https://cloud.google.com/storage/docs/access-control/signed-urls#signing-gae
    raise ValueError('Unable to sign URL, no KEYFILE configured')


class GoogleStorageConfig(object):
    """
    Configuration parameters for accessing Google Cloud Storage.

    Parameters
    ----------
    prefix : str, optional
        A prefix to be used when constructing file path or storage key.
    bucket_name : str, optional
        The name of the Google Cloud Storage bucket.
    credentials_source : str, optional
        The source of Google Cloud Storage credentials, either 'path', 'contents' or 'adc',
        where 'adc' stands for Application Default Credentials.
    service_account_keyfile : str, optional
        The path to the service account keyfile, required if `credentials_source` is 'path'.
    service_account_keyfile_content : str, optional
        The contents of the service account keyfile, required if `credentials_source` is 'contents'.

    Raises
    ------
    ValueError
        If `credentials_source` is not a valid option.
        If `service_account_keyfile` is not provided when `credentials_source` is 'path'.
        If `service_account_keyfile_content` is not provided when `credentials_source` is 'contents'

    Attributes
    ----------
    prefix : str
        A prefix to be used when constructing file path or storage key.
    bucket_name : str
        The name of the Google Cloud Storage bucket.
    credentials_source : str
        The source of Google Cloud Storage credentials, either 'path', 'contents' or 'adc'
    service_account_keyfile : str
        The path to the service account keyfile, required if `credentials_source` is 'path'.
    service_account_keyfile_content : str
        The contents of the service account keyfile, required if `credentials_source` is 'contents'.
    """

    prefix: str
    bucket_name: Optional[str]
    credentials_source: Optional[str]
    service_account_keyfile: Optional[str]
    service_account_keyfile_content: Optional[str]

    def __init__(
        self,
        prefix: str = "",
        bucket_name: Optional[str] = None,
        credentials_source: Optional[str] = None,
        service_account_keyfile: Optional[str] = None,
        service_account_keyfile_content: Optional[str] = None,
        fips_enabled: Optional[bool] = False,
    ):
        self.prefix = prefix
        self.bucket_name = bucket_name
        self.credentials_source = credentials_source
        self.service_account_keyfile = service_account_keyfile
        self.service_account_keyfile_content = service_account_keyfile_content
        self.fips_enabled = fips_enabled

        if self.credentials_source not in GoogleStorageCredentialsSource.all():
            raise ValueError('Valid GOOGLE_STORAGE_CREDENTIALS_SOURCE is required')

        if self.credentials_source == GoogleStorageCredentialsSource.PATH:
            if not self.service_account_keyfile:
                raise ValueError('GOOGLE_STORAGE_KEYFILE_PATH is not set')

        if self.credentials_source == GoogleStorageCredentialsSource.CONTENTS:
            if not self.service_account_keyfile_content:
                raise ValueError('GOOGLE_STORAGE_KEYFILE_CONTENTS is not set')

    @classmethod
    def from_dict(cls, d: Mapping):
        """
        Create an instance of GoogleStorageConfig from a dictionary.

        Parameters
        ----------
        d : Mapping
            Dictionary containing configuration parameters.

        Returns
        -------
        GoogleStorageConfig
            An instance of the class with parameters populated from the dictionary.
        """
        return cls(
            prefix=d.get('FILE_STORAGE_PREFIX', ''),
            bucket_name=d.get('GOOGLE_STORAGE_BUCKET'),
            credentials_source=d.get('GOOGLE_STORAGE_CREDENTIALS_SOURCE'),
            service_account_keyfile=d.get('GOOGLE_STORAGE_KEYFILE_PATH'),
            service_account_keyfile_content=d.get('GOOGLE_STORAGE_KEYFILE_CONTENTS'),
            fips_enabled=str(d.get('ENABLE_FIPS_140_2_MODE')).lower() == 'true',
        )


class GoogleStorage(Storage, StorageUtilsMixin):
    """Implements Storage interface for GCP cloud storage backend."""

    service_account_keyfile: Optional[str]
    bucket_name: str
    prefix: str
    checksum_algorithm: str

    def __init__(
        self, bucket: Optional[str] = None, storage_config: Optional[GoogleStorageConfig] = None
    ):
        super(GoogleStorage, self).__init__()
        config = storage_config or GoogleStorageConfig.from_dict(os.environ)

        if config.credentials_source == GoogleStorageCredentialsSource.PATH:
            self.service_account_keyfile = config.service_account_keyfile
        elif config.credentials_source == GoogleStorageCredentialsSource.CONTENTS:
            self._set_keyfile_contents(config.service_account_keyfile_content)
        elif config.credentials_source == GoogleStorageCredentialsSource.ADC:
            self.service_account_keyfile = None
        else:
            raise ValueError('Invalid credentials source configured')

        self.checksum_algorithm = 'crc32c' if config.fips_enabled else 'md5'
        self.bucket_name = bucket or config.bucket_name
        self.prefix = config.prefix

    def __repr__(self):
        details = dict(bucket=self.bucket_name)
        if self.service_account_keyfile:
            details['service_account_keyfile'] = self.service_account_keyfile
        details_string = ', '.join(f"{k}='{v}'" for k, v in details.items())
        return f"{self.__class__.__name__}({details_string})"

    @property
    def client(self) -> google.cloud.storage.Client:
        return self._client

    def _set_keyfile_contents(self, keyfile_contents_base64):
        # Create a temporary file, the name of which can be passed to google libraries.
        # Performs some sanity checks on the configured value, raises ValueError if bad.
        try:
            keyfile_contents = base64.b64decode(keyfile_contents_base64)
            # pylint: enable=deprecated-method
        except binascii.Error:
            logger.error('GS: Error decoding base64 from keyfile contents', exc_info=True)
            raise ValueError('GS: Error decoding base64 from keyfile contents')
        try:
            # Test that it's valid JSON; catches most cut-n-paste errors.
            _ = json.loads(keyfile_contents)
        except ValueError:
            logger.error('GS: Error loading JSON from decoded keyfile contents', exc_info=True)
            raise ValueError('GS: Error loading JSON from decoded keyfile contents')
        self._tempfile = tempfile.NamedTemporaryFile()
        self._tempfile.write(keyfile_contents)
        self._tempfile.flush()
        self.service_account_keyfile = self._tempfile.name
        return

    def _blob_name(self, name):
        # FILE_STORAGE_PREFIX + name.
        # Leading and multiple "/" chars are not normalized by the server, but get
        # stored literally, which makes the GCP console display them as directories
        # with no name.  Trailing "/" chars are used by convention as placeholders
        # for directories.  Silently squash.
        name = str(name)
        full_name = '/'.join((self.prefix, name)).strip('/')
        return re.sub('//+', '/', full_name)

    def _create_client(self):
        # Get a new client connection.
        if self.service_account_keyfile is None:
            storage_client = google.cloud.storage.Client()
        else:
            storage_client = google.cloud.storage.Client.from_service_account_json(
                self.service_account_keyfile
            )
        return storage_client

    def _create_transport(self):
        # Get a new transport for resumable media download (get_generator).
        ro_scope = u'https://www.googleapis.com/auth/devstorage.read_only'
        if self.service_account_keyfile is None:
            # Application Default Credentials
            creds, _ = google.auth.default((ro_scope,))
        else:
            d = google.auth._default  # pylint: disable=protected-access
            f = d.load_credentials_from_file  # pylint: disable=protected-access
            creds, _ = f(filename=self.service_account_keyfile)
            if creds.requires_scopes:
                creds = creds.with_scopes(scopes=(ro_scope,))
        transport = google.auth.transport.requests.AuthorizedSession(creds)
        return transport

    def _get_bucket(self):
        # Each thread should have its own client and bucket object.
        storage_client = self._create_client()
        return storage_client.get_bucket(self.bucket_name)

    @cached_property
    def _client(self):
        # A cached client used by everything except get_generator.
        return self._create_client()

    @cached_property
    def _bucket(self) -> google.cloud.storage.bucket.Bucket:
        # A cached bucket used by everything except get_generator.
        return self._client.get_bucket(self.bucket_name)

    def exists(self, name: str) -> bool:
        # Ignoring exceptions, can't really map one to True/False.
        blob_name = self._blob_name(name)
        blob = self._bucket.get_blob(blob_name)
        return blob is not None

    def list(self, path: str, recursive: bool = False) -> List[str]:
        full_path = self._blob_name(path.strip('/') if path else '')
        blobs = self._list(full_path, recursive=recursive)
        return [self.removeprefix(x).lstrip('/') for x in blobs]

    def _list(self, blob_prefix, recursive=False):
        # Ignoring exceptions, can't really do much with one.

        blobs = self._client.list_blobs(self.bucket_name, prefix=blob_prefix, delimiter='/')

        # XXX Magic: iterating blobs only works once, and must be done before prefixes is valid.
        file_blobs = set(blobs)
        subdir_names = set(blobs.prefixes)

        dir_blob_prefix = blob_prefix + '/'
        if dir_blob_prefix in subdir_names:
            # Original `path` is a directory.  Query again to see the contents.
            blobs = self._client.list_blobs(self.bucket_name, prefix=dir_blob_prefix, delimiter='/')
            file_blobs = set(blobs)
            subdir_names = set(blobs.prefixes)

        filenames = []

        for blob in file_blobs:
            # Discard full path, just keep basename.
            if recursive:
                filenames.append(blob.name)
            else:
                filenames.append(blob.name.rsplit('/', 1)[-1])

        for prefix in subdir_names:
            if recursive:
                filenames.extend(self._list(prefix, recursive))
            else:
                # Discard full path, and the trailing "/".
                filenames.append(prefix.rstrip('/').rsplit('/', 1)[-1])

        return filenames

    def get(self, name: str, temp_filename: str) -> bool:
        # If not exists, log error and return False.
        blob_name = self._blob_name(name)
        bucket = self._bucket
        logging_extra = {'remote_path': name, 'local_path': temp_filename}
        try:
            blob = bucket.blob(blob_name)
            if blob is None:
                logger.error('GS get: source does not exist', extra=logging_extra)
                return False
            blob.download_to_filename(temp_filename, checksum=self.checksum_algorithm)
            return True
        except Exception:
            logger.error('GS get: error', extra=logging_extra, exc_info=True)
            return False

    def get_generator(self, name: str, **kwargs) -> StorageGenerator:
        # If not exists, log error and return StorageGenerator().
        if not self.exists(name):
            logger.error('GS get_generator: source does not exist', extra={'remote_path': name})
            return StorageGenerator()
        # Note quote() is broken in python2 when given unicode.
        blob_name = quote(self._blob_name(name), safe='')
        url_template = (
            'https://www.googleapis.com/download/storage/v1/b/{bucket}/o/{blob_name}?alt=media'
        )
        media_url = url_template.format(bucket=self.bucket_name, blob_name=blob_name)
        return StorageGenerator(
            DownloadBlobIterator(self._create_transport, media_url).get_generator
        )

    def put(self, name: str, local_filename: str) -> bool:
        # If put fails, log error and return False.
        blob_name = self._blob_name(name)
        bucket = self._bucket
        try:
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(local_filename, checksum=self.checksum_algorithm)
            return True
        except Exception:
            logger.error(
                'GS put: error',
                extra={'local_path': local_filename, 'remote_path': name},
                exc_info=True,
            )
            return False

    def copy(self, name: str, new_name: str) -> bool:
        # If source does not exist, log error and return False.
        # Other exceptions: log error and return False.
        blob_name = self._blob_name(name)
        new_blob_name = self._blob_name(new_name)
        bucket = self._bucket
        logging_extra = {'old_path': name, 'new_path': new_name}
        try:
            source_blob = bucket.blob(blob_name)
            if source_blob is None:
                logger.info('GS copy: source does not exist', extra=logging_extra)
                return False
            _ = bucket.copy_blob(source_blob, bucket, new_blob_name)
            return True
        except Exception:
            logger.error('GS copy: error', extra=logging_extra, exc_info=True)
            return False

    def delete(self, name: str) -> bool:
        # If file is deleted (or never existed), return True.
        # If exception, log warning and return False.
        if not self.exists(name):
            return False
        blob_name = self._blob_name(name)
        bucket = self._bucket
        try:
            blob = bucket.blob(blob_name)
            if blob is None:
                # Does not exist.  (Should not be reached - bucket.get_blob would
                # make a request, but it's faster to attempt a delete and handle
                # if it was not there.)
                return True
            blob.delete()
        except Exception:
            logger.warning('GS delete: error', extra={'remote_path': name}, exc_info=True)
            return False
        return True

    def delete_batch(self, name_iter: Iterable, batch_size: Optional[int] = 100) -> None:
        # The officially documented limit is 100 requests per batch.
        # We allow it as a parameter only to make testing faster.

        if batch_size is None:
            batch_size = 100

        bucket = self._bucket
        for sub_list in self.name_list_chunks(name_iter, batch_size):
            logger.info(
                'GS begin delete_batch',
                extra={'nfiles': len(sub_list), 'now': time.ctime(), 'sub_list': sub_list},
            )
            try:
                with self._client.batch():
                    for name in sub_list:
                        blob_name = self._blob_name(name)
                        blob = bucket.blob(blob_name)
                        blob.delete()
            except google.api_core.exceptions.NotFound:
                pass  # One or more files does not exist.
            except Exception:
                logger.warning('GS delete_batch: error', exc_info=True)
            logger.info(
                'GS done delete_batch', extra={'nfiles': len(sub_list), 'now': time.ctime()}
            )
        return

    def delete_all(self, name: str) -> None:
        # Just to support tests.
        prefix = self._blob_name(name)
        client = self._client
        blobs = client.list_blobs(self.bucket_name, prefix=prefix)
        for blob in blobs:
            logger.info('GS delete_all', extra={'blobname': blob.name})
            try:
                blob.delete()
            except google.api_core.exceptions.NotFound:
                pass
        return

    def url(self, name: str, expires_in: Optional[int] = SIGNED_URL_LIFETIME) -> Optional[str]:
        if not self.exists(name):
            return None
        blob_name = self._blob_name(name)
        if self.service_account_keyfile is None:
            # pylint: disable=assignment-from-no-return
            signed_url = generate_signed_url_with_gce(
                self.bucket_name,
                blob_name,
                expiration=expires_in,
            )
        else:
            signed_url = generate_signed_url_with_keyfile(
                self.service_account_keyfile,
                self.bucket_name,
                blob_name,
                expiration=expires_in,
            )
        return signed_url  # type: ignore[no-any-return]

    def get_key(self, name):
        blob_name = self._blob_name(name)
        return GoogleStorageKey(
            client=self._client,
            bucket=self._bucket,
            name=blob_name,
            checksum_algorithm=self.checksum_algorithm,
        )

    def file_size(self, name: str) -> int:
        return self.get_key(name).size  # type: ignore[no-any-return]

    def get_seekable(self, name: str) -> SeekableStorage:
        return SeekableStorage(self.get_key(name))


class GoogleStorageKey(SeekableKeyInterface):
    def __init__(self, client=None, bucket=None, name=None, checksum_algorithm=None):
        self.client = client
        self.bucket = bucket
        self.name = name
        self.checksum_algorithm = checksum_algorithm or 'md5'

    @property
    def _blob(self):
        blob = self.bucket.blob(self.name)  # This will not make an HTTP request
        blob.reload(self.client)  # Reload properties from Cloud Storage
        return blob

    @property
    def size(self):
        return self._blob.size

    def get_range(self, offset: int, size: int):
        end = (offset + size - 1) if size > 0 else None
        return self._blob.download_as_bytes(
            self.client, start=offset, end=end, checksum=self.checksum_algorithm
        )


class DownloadBlobIterator(object):
    def __init__(self, get_transport, media_url):
        self.get_transport = get_transport
        self.media_url = media_url
        return

    def get_generator(self, offset=0):
        logging_extra = {'blob_name': self.media_url}
        chunk_size = 20 * 1024 * 1024  # 20-MiB
        try:
            transport = self.get_transport()
            stream = io.BytesIO()
            download = google.resumable_media.requests.ChunkedDownload(
                self.media_url,
                chunk_size,
                stream,
                start=offset,
            )
            while not download.finished:
                download.consume_next_chunk(transport)
                stream.seek(0)
                while True:
                    chunk = stream.read(8192)
                    if not chunk:
                        break
                    yield chunk
                stream.seek(0)
                stream.truncate(0)
        except Exception:
            logger.error(
                'GS get_generator: error streaming file', exc_info=True, extra=logging_extra
            )
            raise
        return
