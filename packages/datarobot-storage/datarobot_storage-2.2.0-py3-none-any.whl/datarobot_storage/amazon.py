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

import collections
import io
import logging
import math
import os
import tempfile
import time
import types
from base64 import b64encode
from builtins import object
from builtins import range
from hashlib import sha256
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type
from typing import Union
from urllib.parse import urlunparse

import boto3
import boto3.s3.transfer
import botocore.client
import botocore.config
import botocore.credentials
import botocore.exceptions
import botocore.session
from filechunkio import FileChunkIO

# The mypy_boto3_s3 library is defined as dev dependency of datarobot-storage.
# Downstream clients of the library do not get dev dependencies installed when
# using the datarobot-storage library. This makes it optional
if TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import Bucket
    from mypy_boto3_s3.service_resource import Object
    from mypy_boto3_s3.service_resource import S3ServiceResource

from typing_extensions import Self  # typing.Self available in 3.11+

from datarobot_storage.base import SeekableKeyInterface
from datarobot_storage.base import SeekableStorage
from datarobot_storage.base import Storage
from datarobot_storage.base import StorageGenerator
from datarobot_storage.enums import S3ServerSideEncryption
from datarobot_storage.exceptions import wrap_client_error
from datarobot_storage.put_generator import PutGenerator
from datarobot_storage.utils import ClientPool
from datarobot_storage.utils import StorageUtilsMixin
from datarobot_storage.utils import cached_property
from datarobot_storage.utils import retry

# Leave logs where they used to be. Please note that botocore library produces too many debug logs,
# so we have a special handler in drlogs to snooze it. If you still want to see these messages,
# then use ENABLE_BOTOCORE_DEBUG_LOGGING configuration setting
logger = logging.getLogger(__name__)

NA = object()


class S3InternalError(Exception):
    """Exception used for retries, in case AWS returns 200 but in fact it is
    5xx S3ResponseError.

    https://aws.amazon.com/premiumsupport/knowledge-center/s3-resolve-200-internalerror/
    """


class S3Key(SeekableKeyInterface):
    def __init__(self, key: 'Object'):
        self._key = key

    @property
    def boto_key(self):
        # Access to the underlying key, provided for drivers and tests.
        # Application code MUST NOT use this key directly
        return self._key

    @property
    def name(self):
        return self._key.key

    @property
    def size(self):
        if hasattr(self._key, 'size'):
            return self._key.size
        else:
            return self._key.content_length

    @property
    def last_modified(self):
        dt = self._key.last_modified
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    def delete(self):
        return self._key.delete()

    def _get_stream(self, offset=0, size=0) -> io.IOBase:
        """Return boto file-like object

        Returns
        -------
        botocore.response.StreamingBody(IOBase)
        """
        if size > 0:
            end = offset + size - 1
            range_header = "bytes=%d-%d" % (offset, end)
        else:
            range_header = "bytes=%d-" % offset

        response = self._key.get(Range=range_header)
        return response['Body']  # type: ignore[no-any-return]

    def get_generator_factory(self, chunk_size=Storage.CHUNK_SIZE) -> Callable:
        """Return generator factory method.

        See also https://alexwlchan.net/2019/02/working-with-large-s3-objects/
        Just need the `read` method, so this is much simplified
        """

        def create_generator(offset=0, size=0):
            # There is no way to construct a valid RFC7433 request for a 0-length empty file,
            # so we only do this if the file length is non-zero.
            if self.size:
                fobj = self._get_stream(offset, size)
                while True:
                    chunk = fobj.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        return create_generator

    def get_range(self, offset: int, size: int) -> bytes:
        """Return file bytes starting from offset for at most `size` bytes."""
        fobj = self._get_stream(offset, size)
        return fobj.read()  # type: ignore[no-any-return]


class Boto3MultiPartUploader(object):
    def __init__(self, bucket, s3_config, key_name: str) -> None:
        self.parts = []
        self.client = bucket.meta.client
        self.sha256_kwargs = s3_config.sha256_kwargs

        mp_config = dict(Bucket=bucket.name, Key=key_name, **s3_config.sha256_kwargs)

        if s3_config.encrypt_key:
            mp_config.update(s3_config.server_side_encryption_kwargs)

        self.mp = self.client.create_multipart_upload(**mp_config)

    @retry(exceptions=(S3InternalError,), max_tries=3, max_delay=1)
    def complete_upload_with_retry(self):
        """
        Complete multipart upload with retries. AWS may fail
        with internal servererror, so the only option is retry.

        https://aws.amazon.com/premiumsupport/knowledge-center/s3-resolve-200-internalerror/
        """
        return self.complete_upload()

    def complete_upload(self):
        self.client.complete_multipart_upload(
            Bucket=self.mp['Bucket'],
            UploadId=self.mp['UploadId'],
            MultipartUpload={'Parts': self.parts},
            Key=self.mp['Key'],
        )

    def upload_part(self, file_object, part_number):
        data = file_object.read()
        kwargs = {}

        if self.sha256_kwargs:
            digest = b64encode(sha256(data).digest()).decode('utf-8')
            kwargs = {'ChecksumSHA256': digest, **self.sha256_kwargs}

        part_metadata = self.client.upload_part(
            Bucket=self.mp['Bucket'],
            UploadId=self.mp['UploadId'],
            Key=self.mp['Key'],
            Body=data,
            PartNumber=part_number,
            **kwargs,
        )

        part = {'ETag': part_metadata['ETag'], 'PartNumber': part_number}

        if 'ChecksumSHA256' in part_metadata:
            part['ChecksumSHA256'] = part_metadata['ChecksumSHA256']

        self.parts.append(part)

    def abort_multipart_upload(self):
        self.client.abort_multipart_upload(
            Bucket=self.mp['Bucket'],
            UploadId=self.mp['UploadId'],
            Key=self.mp['Key'],
        )


class S3Configuration(object):
    """
    All S3Storage configuration parameters in one place.

    Parameters
    ----------
    aws_access_key_id : str, optional
        AWS access key ID. Default is None.
    aws_secret_access_key : str, optional
        AWS secret access key. Default is None.
    aws_session_token : str, optional
        AWS session token. Default is None.
    aws_profile : str, optional
        AWS profile name. Default is None.
    aws_ca_bundle : str or None
        Path to a CA bundle to use for HTTPS certificate validation
    s3_role_arn : str or None
        ARN of a role to assume for S3 access.
    s3_host : str, optional
        S3 host address. Default is an empty string.
    s3_port : int, optional
        S3 port number. Default is 443.
    s3_bucket : str, optional
        S3 bucket name. Default is an empty string.
    s3_region : str, optional
        AWS region for S3. Default is an empty string.
    s3_service : str, optional
        AWS service name for S3. Default is an empty string.
    s3_is_secure : bool, optional
        Use secure (HTTPS) connection for S3. Default is True.
    s3_validate_certs : bool, optional
        Validate S3 SSL certificates. Default is True.
    s3_addressing_style : str, optional
        S3 addressing style. Default is "auto".
    s3_server_side_encryption : str, optional
        S3 server-side encryption algorithm. Default is `S3ServerSideEncryption.S3_SSE_AES`.
    s3_server_side_encryption_key_id : str, optional
        S3 server-side encryption key ID. Default is an empty string.
    boto_http_socket_timeout : int, optional
        Timeout for HTTP socket in seconds. Default is 150.
    boto_num_retries : int, optional
        Number of retries for Boto requests. Default is 7.
    boto_metadata_service_timeout : int, optional
        Timeout for Boto metadata service. Default is 2.
    boto_metadata_service_num_attempts : int, optional
        Number of attempts for Boto metadata service. Default is 7.
    botocore_extra_ciphers : str, optional
        Extra ciphers for Botocore. Default is an empty string.
    local_data_directory : str, optional
        Local directory for storing data. Default is a system temporary directory.
    prefix : str, optional
        A prefix to be used when constructing file path or storage key.
    multipart_upload_enabled : bool, optional
        Enable multipart upload for large files. Default is True.
    multipart_download_enabled : bool, optional
        Enable multipart download for large files. Default is True.
    use_sha256 : bool, optional
        Use SHA256 to calculate checksum on upload, required in FIPS 140-2 mode. Default is False.

    Attributes
    ----------
    aws_access_key_id : str or None
        AWS access key ID.
    aws_secret_access_key : str or None
        AWS secret access key.
    aws_session_token : str or None
        AWS session token.
    aws_profile : str or None
        AWS profile name.
    aws_ca_bundle : str or None
        Path to a CA bundle
    s3_role_arn : str or None
        ARN of a role to assume for S3 access.
    s3_host : str
        S3 host address.
    s3_port : int
        S3 port number.
    s3_bucket : str
        S3 bucket name.
    s3_region : str
        AWS region for S3.
    s3_service : str
        AWS service name for S3.
    s3_is_secure : bool
        Use secure (HTTPS) connection for S3.
    s3_validate_certs : bool
        Validate S3 SSL certificates.
    s3_addressing_style : str
        S3 addressing style.
    sse : str
        S3 server-side encryption algorithm.
    sse_kms_key_id : str
        S3 server-side encryption key ID.
    boto_http_socket_timeout : int
        Timeout for HTTP socket in seconds.
    boto_num_retries : int
        Number of retries for Boto requests.
    boto_metadata_service_timeout : int
        Timeout for Boto metadata service.
    boto_metadata_service_num_attempts : int
        Number of attempts for Boto metadata service.
    botocore_extra_ciphers : str
        Extra ciphers for Botocore.
    local_data_directory : str
        Local directory for storing data.
    multipart_upload_enabled : bool
        Enable multipart upload for large files.
    multipart_download_enabled : bool
        Enable multipart download for large files.
    """

    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_session_token: Optional[str]
    aws_profile: Optional[str]
    aws_ca_bundle: Optional[str]
    s3_role_arn: Optional[str]
    s3_host: str
    s3_port: int
    s3_bucket: str
    s3_region: str
    s3_service: str
    s3_is_secure: bool
    s3_validate_certs: bool
    s3_addressing_style: str
    sse: str
    sse_kms_key_id: str
    boto_http_socket_timeout: int
    boto_num_retries: int
    boto_metadata_service_timeout: int
    boto_metadata_service_num_attempts: int
    botocore_extra_ciphers: str
    local_data_directory: str
    prefix: str
    multipart_upload_enabled: bool
    multipart_download_enabled: bool
    use_sha256: bool

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_profile: Optional[str] = None,
        aws_ca_bundle: Optional[str] = None,
        s3_role_arn: Optional[str] = None,
        s3_host: str = "",
        s3_port: int = 443,
        s3_bucket: str = "",
        s3_region: str = "",
        s3_service: str = "",
        s3_is_secure: bool = True,
        s3_validate_certs: bool = True,
        s3_addressing_style: str = "auto",
        s3_server_side_encryption: str = S3ServerSideEncryption.S3_SSE_AES,
        s3_server_side_encryption_key_id: str = "",
        boto_http_socket_timeout: int = 150,
        boto_num_retries: int = 7,
        boto_metadata_service_timeout: int = 2,
        boto_metadata_service_num_attempts: int = 7,
        botocore_extra_ciphers: str = "",
        local_data_directory: str = "",
        prefix: str = "",
        multipart_upload_enabled: bool = True,
        multipart_download_enabled: bool = True,
        use_sha256: bool = False,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.aws_profile = aws_profile
        self.aws_ca_bundle = aws_ca_bundle
        self.s3_role_arn = s3_role_arn
        self.s3_bucket = s3_bucket
        self.s3_region = s3_region
        self.s3_service = s3_service
        self.s3_validate_certs = s3_validate_certs
        self.botocore_extra_ciphers = botocore_extra_ciphers

        self.boto_http_socket_timeout = boto_http_socket_timeout
        self.boto_num_retries = boto_num_retries
        self.boto_metadata_service_timeout = boto_metadata_service_timeout
        self.boto_metadata_service_num_attempts = boto_metadata_service_num_attempts

        self.s3_addressing_style = s3_addressing_style
        self.s3_host = s3_host
        self.s3_port = s3_port
        self.s3_is_secure = s3_is_secure

        self.sse = s3_server_side_encryption
        self.sse_kms_key_id = s3_server_side_encryption_key_id

        self.multipart_upload_enabled = multipart_upload_enabled
        self.multipart_download_enabled = multipart_download_enabled

        self.prefix = prefix
        self.local_data_directory = local_data_directory or tempfile.gettempdir()

        self.use_sha256 = use_sha256

    def __repr__(self) -> str:
        details = dict(bucket=self.s3_bucket)
        if self.prefix:
            details['prefix'] = self.prefix
        if self.aws_access_key_id:
            details['aws_access_key_id'] = self.aws_access_key_id
        elif self.aws_profile:
            details['aws_profile'] = self.aws_profile
        if self.s3_role_arn:
            details['assume_role'] = self.s3_role_arn
        details_string = ', '.join(f"{k}='{v}'" for k, v in details.items())
        return f"{self.__class__.__name__}({details_string})"

    @staticmethod
    def get_int(mapping, key) -> Union[int, object]:
        try:
            return int(mapping[key])
        except (ValueError, TypeError, KeyError):
            return NA

    @staticmethod
    def get_bool(mapping, key) -> Union[bool, object]:
        if key not in mapping:
            return NA
        return str(mapping[key]).lower() == 'true'

    @classmethod
    def from_dict(cls, _dict: collections.abc.Mapping) -> Self:
        # os.environ is always {str: str}, sp o values must be converted manually to integers/bools
        optional_kwargs = dict(
            aws_access_key_id=_dict.get('AWS_ACCESS_KEY_ID', NA),
            aws_secret_access_key=_dict.get('AWS_SECRET_ACCESS_KEY', NA),
            aws_session_token=_dict.get('AWS_SESSION_TOKEN', NA),
            aws_profile=_dict.get('AWS_PROFILE', NA),
            aws_ca_bundle=_dict.get('AWS_CA_BUNDLE', NA),
            s3_role_arn=_dict.get('S3_ROLE_ARN', NA),
            s3_bucket=_dict.get('S3_BUCKET', NA),
            s3_host=_dict.get('S3_HOST', NA),
            s3_port=cls.get_int(_dict, 'S3_PORT'),
            s3_region=_dict.get('S3_REGION', NA),
            s3_service=_dict.get('S3_SERVICE', NA),
            s3_is_secure=cls.get_bool(_dict, 'S3_IS_SECURE'),
            s3_validate_certs=cls.get_bool(_dict, 'S3_VALIDATE_CERTS'),
            s3_addressing_style=_dict.get('S3_ADDRESSING_STYLE', NA),
            s3_server_side_encryption=_dict.get('S3_SERVER_SIDE_ENCRYPTION', NA),
            s3_server_side_encryption_key_id=_dict.get('AWS_S3_SSE_KMS_KEY_ID', NA),
            botocore_extra_ciphers=_dict.get('S3_BOTOCORE_CIPHERS_ADDITION', NA),
            boto_http_socket_timeout=cls.get_int(_dict, 'FILE_STORAGE_S3_TIMEOUT'),
            boto_num_retries=cls.get_int(_dict, 'FILE_STORAGE_S3_RETRIES'),
            boto_metadata_service_timeout=cls.get_int(_dict, 'METADATA_SERVICE_TIMEOUT'),
            boto_metadata_service_num_attempts=cls.get_int(_dict, 'METADATA_SERVICE_RETRIES'),
            multipart_upload_enabled=cls.get_bool(_dict, 'MULTI_PART_S3_UPLOAD'),
            multipart_download_enabled=cls.get_bool(_dict, 'MULTI_PART_S3_DOWNLOAD'),
            local_data_directory=_dict.get('DATA_DIR', NA),
            prefix=_dict.get('FILE_STORAGE_PREFIX', NA),
            use_sha256=cls.get_bool(_dict, 'ENABLE_FIPS_140_2_MODE'),
        )
        return cls(**{k: v for k, v in optional_kwargs.items() if v is not NA})

    @classmethod
    def from_environ(cls) -> Self:
        return cls.from_dict(os.environ)

    def _get_encryption_type(self) -> str:
        # (Backward compatibility) S3_SERVER_SIDE_ENCRYPTION cannot be None since the value of
        # S3ServerSideEncryption.DISABLED was changed from None to 'DISABLED'
        return self.sse or S3ServerSideEncryption.DISABLED

    @property
    def s3_encryption_type(self) -> str:
        # TODO: only need this or _get_encryption_type
        return self._get_encryption_type()

    @property
    def encrypt_key(self) -> bool:
        return self._get_encryption_type() in [
            S3ServerSideEncryption.S3_SSE_AES,
            S3ServerSideEncryption.S3_SSE_KMS,
        ]

    @property
    def server_side_encryption_kwargs(self) -> Dict[str, str]:
        """
        Get kwargs for enabling server side encryption
        """
        if self.sse in [
            S3ServerSideEncryption.S3_SSE_AES,
            S3ServerSideEncryption.S3_SSE_KMS,
        ]:
            sse = {'ServerSideEncryption': self.sse}
            if self.sse_kms_key_id:
                sse['SSEKMSKeyId'] = self.sse_kms_key_id
            return sse
        else:
            return {}

    @property
    def sha256_kwargs(self):
        return {'ChecksumAlgorithm': 'SHA256'} if self.use_sha256 else {}

    @property
    def endpoint_url(self) -> str:
        """
        A parameter for create_connection
        """
        host = self.s3_host
        port = self.s3_port
        is_secure = self.s3_is_secure

        if port:
            host_port = '{}:{}'.format(host, port)
        else:
            host_port = host

        scheme = 'https' if is_secure else 'http'
        return urlunparse([scheme, host_port, '', '', '', ''])


class Boto3Driver(object):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#bucket

    CHUNK_SIZE = Storage.CHUNK_SIZE
    MultipartUploader = Boto3MultiPartUploader

    # A dictionary to override default pagination settings. Check the documentation for details:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#paginators
    pagination_config: Dict[str, Any] = {}

    def __init__(self, s3_config):
        self.s3_config = s3_config

    def patch_libraries(self):
        # this is a patch for https://datarobot.atlassian.net/browse/ENT-6578
        # if S3_VALIDATE_CERTS is false; then the idea is to not validate certs
        # however the "validate_certs" flag on the boto side doesn't work therefore
        # create a ssl context to allow unverified SSL
        if not self.s3_config.s3_validate_certs:
            import ssl

            # pylint: disable=protected-access
            # noinspection PyUnresolvedReferences
            ssl._create_default_https_context = ssl._create_unverified_context

        # Patch cipher suites that are used for HTTPs. Required when DataRobot can not establish
        # a secure connection with S3 endpoint (e.g. when it's not AWS but some 3rd-party solution).
        if self.s3_config.botocore_extra_ciphers:
            import botocore.httpsession

            # For boto-core>=1.34.63 and urllib3>=2.0.0 this path doesn't need to be applied.
            # https://github.com/boto/botocore/blob/649518672202385cc006d6c43b821dc29d48a67f/botocore/httpsession.py#L51-L57
            # https://github.com/boto/botocore/blob/649518672202385cc006d6c43b821dc29d48a67f/botocore/httpsession.py#L114-L119
            should_apply_patch = botocore.httpsession.DEFAULT_CIPHERS is not None
            if (
                should_apply_patch
                and self.s3_config.botocore_extra_ciphers
                not in botocore.httpsession.DEFAULT_CIPHERS
            ):
                botocore.httpsession.DEFAULT_CIPHERS += self.s3_config.botocore_extra_ciphers
                logger.info(
                    'Using new default cipher suite in botocore.httpsession',
                    extra={'additional_suite': self.s3_config.botocore_extra_ciphers},
                )

    def bucket_multipart_upload(
        self, bucket, key_name, filename, chunk_size, callback, logging_info
    ):
        # pylint: disable=not-callable
        uploader = self.MultipartUploader(bucket, self.s3_config, key_name)
        chunk_count = int(math.ceil(logging_info['source_size'] // chunk_size))

        logging_info['chunk_count'] = chunk_count + 1
        logger.debug('Uploading file in chunks', extra=logging_info)

        for i in range(chunk_count + 1):
            part_number = i + 1
            offset = chunk_size * i
            nbytes = min(chunk_size, logging_info['source_size'] - offset)
            logging_info.update({'chunk_number': i, 'byte_offset': offset})
            logger.debug('Uploading chunk', extra=logging_info)
            with FileChunkIO(filename, 'r', offset=offset, bytes=nbytes) as fp:
                uploader.upload_part(fp, part_number)

            callback(offset, nbytes, logging_info['source_size'])

        uploader.complete_upload_with_retry()

    def create_session(self) -> boto3.session.Session:
        """
        Returns
        -------
        boto3.session.Session
        """
        self.patch_libraries()

        # When using IAM Roles we talk to the metadata service and need retries.
        # Both metadata_service_timeout and metadata_service_num_attempts are not accessible as
        # as boto3.session.Session properties yet. Need to configure them on botocore.Session first.
        # I hope sometime this will be implemented https://github.com/boto/boto3/issues/2561, and
        # we will be able to move setting these into config method and delete the following lines.
        botocore_session = botocore.session.get_session()
        botocore_session.set_config_variable(
            'metadata_service_timeout', self.s3_config.boto_metadata_service_timeout
        )
        botocore_session.set_config_variable(
            'metadata_service_num_attempts', self.s3_config.boto_metadata_service_num_attempts
        )

        session = boto3.session.Session(
            botocore_session=botocore_session,
            aws_access_key_id=self.s3_config.aws_access_key_id,
            aws_secret_access_key=self.s3_config.aws_secret_access_key,
            aws_session_token=self.s3_config.aws_session_token,
            profile_name=self.s3_config.aws_profile,
        )
        if self.s3_config.s3_role_arn:
            # Use assumed role with auto-refreshable credentials for access. Useful for long-running
            # jobs in cloud that need to use different role than one configured in pod.
            # In such cases, K8s ensures that web identity token mounted in pod doesn't expire, and
            # DeferredRefreshableCredentials/AssumeRoleCredentialFetcher ensures temporary creds
            # for assumed role doesn't expire.

            # Another opened (forever) issue in boto3 -> https://github.com/boto/boto3/issues/443
            # https://stackoverflow.com/questions/44171849/aws-boto3-assumerole-example-which-includes-role-usage
            fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
                client_creator=botocore_session.create_client,
                role_arn=self.s3_config.s3_role_arn,
                source_credentials=session.get_credentials(),
            )
            botocore_session._credentials = botocore.credentials.DeferredRefreshableCredentials(
                method='assume-role',
                refresh_using=fetcher.fetch_credentials,
            )

        return session

    @property
    def boto_config(self) -> botocore.config.Config:
        """Return S3 boto configuration

        Returns
        -------
        botocore.config.Config
        """
        data = {'signature_version': 's3v4'}

        if self.s3_config.s3_region:
            data['region_name'] = self.s3_config.s3_region

        # TODO: datarobot.schema only validates numbers as string
        # TODO: Add calling_format option

        # Using Standard retry mode.
        # See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html for details
        data['retries'] = {'mode': 'standard', 'max_attempts': self.s3_config.boto_num_retries}

        # See also: https://urllib3.readthedocs.io/en/latest/user-guide.html#using-timeouts
        data['connect_timeout'] = self.s3_config.boto_http_socket_timeout
        data['read_timeout'] = self.s3_config.boto_http_socket_timeout

        if self.s3_config.s3_addressing_style:
            data['s3'] = {'addressing_style': self.s3_config.s3_addressing_style}

        # https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
        return botocore.config.Config(**data)

    def create_connection(self) -> 'S3ServiceResource':
        session = self.create_session()
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
        # or boto3.client('s3', ...)?
        return session.resource(
            self.s3_config.s3_service or 's3',
            endpoint_url=self.s3_config.endpoint_url if self.s3_config.s3_host else None,
            use_ssl=self.s3_config.s3_is_secure,
            verify=self.s3_config.aws_ca_bundle or self.s3_config.s3_validate_certs,
            config=self.boto_config,
        )

    @staticmethod
    def get_bucket(connection: 'S3ServiceResource', bucket_name: str) -> 'Bucket':
        """
        Try reading bucket to verify it exists, then return the bucket
        """
        s3_client = connection.meta.client
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            bucket = connection.Bucket(bucket_name)
            # bucket.load() -- should do the same thing, but:
            # XXX botocore.exceptions.ClientError: An error occurred (AuthorizationHeaderMalformed)
            # XXX when calling the ListBuckets operation: The authorization header is malformed;
            # XXX a non-empty region must be provided in the credential.
            return bucket
        except botocore.exceptions.ClientError as e:
            logger.error(
                'Failed to lookup bucket', extra={'bucket_name': bucket_name}, exc_info=True
            )
            raise wrap_client_error(e)

    @staticmethod
    def bucket_get_key(bucket: 'Bucket', key_name: str, load_key=True) -> Optional[S3Key]:
        """
        Create KeyInterface instance, optionally read the key to verify it exists.
        """
        key = bucket.Object(key_name)
        try:
            if load_key:
                key.load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.debug('S3 Key not found', extra={'key': key_name})
                return None
            raise wrap_client_error(e)
        return S3Key(key)

    def bucket_key_exists(self, bucket, key_name) -> bool:
        return self.bucket_get_key(bucket, key_name) is not None

    def bucket_list(self, bucket, prefix=None, delimiter=None, recursive=False):
        S3Prefix = collections.namedtuple('S3Prefix', ('key',))
        s3_objects = []

        paginator = bucket.meta.client.get_paginator('list_objects_v2')
        s3_query_params = dict(Bucket=bucket.name, Prefix=prefix, Delimiter=delimiter or '')
        if self.pagination_config:
            s3_query_params['PaginationConfig'] = self.pagination_config

        for bucket_page_result in paginator.paginate(**s3_query_params):
            for key in bucket_page_result.get('Contents', []):
                key_object = self.bucket_get_key(bucket, key['Key'], load_key=False)
                if key_object is not None:
                    s3_objects.append(S3Key(key_object.boto_key))
            for key_prefix in bucket_page_result.get('CommonPrefixes', []):
                s3_prefix = S3Prefix(key=key_prefix['Prefix'])
                if recursive:
                    s3_objects.extend(self.bucket_list(bucket, s3_prefix.key, delimiter, recursive))
                else:
                    s3_objects.append(S3Key(s3_prefix))

        return s3_objects

    def bucket_list_generator(self, bucket, prefix=None, delimiter=None) -> Iterable[S3Key]:
        S3Prefix = collections.namedtuple('S3Prefix', ('key',))

        paginator = bucket.meta.client.get_paginator('list_objects_v2')
        s3_query_params = dict(Bucket=bucket.name, Prefix=prefix, Delimiter=delimiter or '')
        if self.pagination_config:
            s3_query_params['PaginationConfig'] = self.pagination_config

        for bucket_page_result in paginator.paginate(**s3_query_params):
            for key in bucket_page_result.get('Contents', []):
                key_object = self.bucket_get_key(bucket, key['Key'], load_key=False)
                if key_object is not None:
                    yield S3Key(key_object.boto_key)
            for key_prefix in bucket_page_result.get('CommonPrefixes', []):
                s3_prefix = S3Prefix(key=key_prefix['Prefix'])
                yield S3Key(s3_prefix)

    def bucket_download(
        self, bucket: 'Bucket', key_name: str, filename: str, transfer_config=None, callback=None
    ) -> None:
        if not self.bucket_key_exists(bucket, key_name):
            raise FileNotFoundError(key_name)

        bucket.download_file(
            key_name,
            filename,
            Config=transfer_config,
            Callback=callback,
            # Note ServerSideEncryption is not valid/required here.
        )

    def bucket_multipart_download(
        self, bucket: 'Bucket', key_name: str, filename: str, chunk_size: int, callback: Callable
    ) -> None:
        key = self.bucket_get_key(bucket, key_name)

        if key is None:
            raise FileNotFoundError(key_name)

        # S3Storage public interface allows custom callback methods for put/get operations, those
        # custom methods will expect two arguments: bytes already transferred and overall size.
        def _callback(transferred):
            return callback(transferred, key.size)

        transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_threshold=chunk_size, multipart_chunksize=chunk_size, use_threads=False
        )
        self.bucket_download(bucket, key_name, filename, transfer_config, _callback)

    def bucket_generator_download(self, key):
        return key.get_generator_factory(self.CHUNK_SIZE)

    def bucket_upload(self, bucket: 'Bucket', key_name: str, filename: str) -> None:
        extra_args = dict(self.s3_config.sha256_kwargs)
        extra_args.update(self.s3_config.server_side_encryption_kwargs)
        bucket.upload_file(filename, key_name, ExtraArgs=extra_args)

    def bucket_delete_key(self, bucket: 'Bucket', key_name: str):
        if not self.bucket_key_exists(bucket, key_name):
            raise FileNotFoundError(key_name)
        obj = bucket.Object(key_name)
        return obj.delete()

    def bucket_delete_key_batch(self, bucket: 'Bucket', key_name_list: List[str]) -> None:
        verbose = logger.isEnabledFor(logging.DEBUG)
        deletion_result = bucket.delete_objects(
            Delete={
                'Objects': [{'Key': key_name} for key_name in key_name_list],
                'Quiet': not verbose,
            },
            **self.s3_config.sha256_kwargs,
        )

        for failure in deletion_result.get('Errors', []):
            failure_details = {'key': failure['Key'], 'reason': failure['Message']}
            logger.warning('S3 delete_batch failed', extra=failure_details)

        if verbose:
            for success in deletion_result.get('Deleted', []):
                logger.debug('S3 delete_batch object deleted', extra={'key': success['Key']})

    def bucket_copy_key(self, bucket: 'Bucket', dest_key_name: str, source_key_name: str) -> None:
        if not self.bucket_key_exists(bucket, source_key_name):
            raise FileNotFoundError(source_key_name)

        extra_args = {}
        extra_args.update(self.s3_config.sha256_kwargs)
        extra_args.update(self.s3_config.server_side_encryption_kwargs)
        copy_source = {'Bucket': bucket.name, 'Key': source_key_name}

        bucket.copy(copy_source, dest_key_name, ExtraArgs=extra_args)

    def bucket_generate_presigned_url(
        self, bucket: 'Bucket', key_name: str, lifetime: int
    ) -> Optional[str]:
        # see example: https://github.com/boto/boto3/issues/110#issuecomment-140416008
        if not self.bucket_key_exists(bucket, key_name):
            raise FileNotFoundError(key_name)
        s3_client = bucket.meta.client
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket.name, 'Key': key_name},
                ExpiresIn=lifetime,
            )
            return str(url)
        except Exception:
            # XXX Move up, file_name should be original.
            logger.info("No url for file in storage", extra={'file_name': key_name}, exc_info=True)
            return None


class bucket_from_pool(object):
    bucket_pool = None
    MAX_RETRY_ATTEMPTS = 1

    def __init__(self, storage):
        self.storage = storage
        self.bucket = None
        self.use_bucket_pool = storage.use_bucket_pool

        if self.storage.use_bucket_pool:
            if self.__class__.bucket_pool is None:
                bucket_from_pool.bucket_pool = ClientPool(self.storage.get_bucket)

    def __enter__(self) -> 'Bucket':
        if not self.storage.use_bucket_pool:
            return self.storage.bucket

        # Get bucket from pool and try reading its HEAD,
        # if failed, then try with another bucket.
        for attempt in range(self.MAX_RETRY_ATTEMPTS + 1):
            try:
                self.bucket = self.__class__.bucket_pool.fetch()
                # First bucket accessibility check
                self.bucket.meta.client.head_bucket(Bucket=self.bucket.name)
            except botocore.exceptions.ClientError as e:
                # If failed, then discard the bucket
                self.__class__.bucket_pool.discard(self.bucket)
                # and raise if we already did it
                if attempt >= self.MAX_RETRY_ATTEMPTS:
                    raise wrap_client_error(e)
            else:
                break

        # bucket is ready for usage in the target context
        return self.bucket

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: types.TracebackType,
    ) -> None:
        if self.storage.use_bucket_pool:
            self.__class__.bucket_pool.put(self.bucket)


class S3Storage(Storage, StorageUtilsMixin):
    """
    Provides access to S3-compatible Blob Storage.

    Parameters
    ----------
    bucket : str or None, optional
        The name of the S3 bucket. Default is None.
    use_bucket_pool : bool, optional
        Flag to enable the use of a bucket pool. Default is False.
    get_cb : Callable or None, optional
        Callback function for customizing 'get' operations. Default is None.
    put_cb : Callable or None, optional
        Callback function for customizing 'put' operations. Default is None.
    storage_config : S3Configuration or None, optional
        Configuration object for S3 storage. Default is None.

    Attributes
    ----------
    MULTIPART_CHUNK_SIZE : int
        Size of each chunk in multipart uploads. Default is 52428800 bytes (50 MiB).
    driver: Boto3Driver
        Implementation of the S3 driver
    get_cb: callable
        Callback function accepting two integers: transmitted and total bytes,
        called when multipart download is enabled
    put_cb: callable
        Callback function accepting two integers: uploaded amount and total source size in bytes,
        called when multipart upload is enabled
    config: S3Configuration
        Configuration object for S3 storage. Default is result of `S3Configuration.from_environ()`
    use_bucket_pool: bool
        Flag to enable the use of a bucket pool. Prevents creating bucket objects on every operation
        and could significantly improve the performance
    """

    MULTIPART_CHUNK_SIZE: int = 52428800

    config: S3Configuration
    prefix: str
    local_data_directory: str
    driver: Boto3Driver
    get_cb: Callable
    put_cb: Callable
    use_bucket_pool: bool

    def __init__(
        self,
        bucket: Optional[str] = None,
        use_bucket_pool: bool = False,
        get_cb: Optional[Callable] = None,
        put_cb: Optional[Callable] = None,
        storage_config: Optional[S3Configuration] = None,
    ):
        super().__init__()

        self.config = storage_config or S3Configuration.from_environ()

        if bucket:
            self.config.s3_bucket = bucket

        self.prefix = self.config.prefix
        self.local_data_directory = self.config.local_data_directory

        self.driver = Boto3Driver(self.config)
        self.get_cb = get_cb
        self.put_cb = put_cb
        self.use_bucket_pool = use_bucket_pool

    def __repr__(self):
        return f"{self.__class__.__name__}(config={self.config})"

    def get_key_name(self, name) -> str:
        """
        The method was introduced back in the monolith era, keeping it for backward compatibility.
        """
        return self._name(name)

    @property
    def client(self) -> botocore.client.BaseClient:
        return self.bucket.meta.client

    @property
    def bucket_name(self) -> str:
        return self.config.s3_bucket

    @cached_property
    def bucket(self) -> 'Bucket':
        return self.get_bucket()

    def get_bucket(self) -> 'Bucket':
        connection = self.driver.create_connection()
        bucket = self.driver.get_bucket(connection, self.bucket_name)
        return bucket

    def download_handler(self, transmitted: int, total: int) -> None:
        # Callback for download notifications.  Logs progress and calls optional user callback.
        if self.get_cb is not None:
            self.get_cb(transmitted, total)

    def upload_handler(self, offset: int, nbytes: int, total: int) -> None:
        # Callback for upload notifications.  Logs progress and calls optional user callback.
        # Note: total will be -1 when size is unknown.
        if self.put_cb is not None:
            self.put_cb(offset + nbytes, total)

    def exists(self, name: str) -> bool:
        key_name = self._name(name)
        with bucket_from_pool(self) as bucket:
            return self.driver.bucket_key_exists(bucket, key_name)

    def list(self, path: str, recursive: bool = False) -> List[str]:
        delimiter = '/'
        # Assume it's a directory - use an explicit trailing delimiter so a regular
        # filename cannot match.
        path = path.strip(delimiter) if path else ''
        key_name = self._name(path).rstrip(delimiter) + delimiter
        with bucket_from_pool(self) as bucket:
            content = self.driver.bucket_list(
                bucket, prefix=key_name, delimiter=delimiter, recursive=recursive
            )
            if recursive:
                files = [self.removeprefix(key.name).lstrip(delimiter) for key in content]
            else:
                files = [os.path.basename(key.name.rstrip(delimiter)) for key in content]
        if not files:
            # Otherwise - maybe it's a filename.
            if self.exists(path):
                return [path if recursive else os.path.basename(path)]
        return files

    def get_large(self, name: str, temp_filename: str) -> bool:
        key_name = self._name(name)
        try:
            with bucket_from_pool(self) as bucket:
                self.driver.bucket_multipart_download(
                    bucket,
                    key_name,
                    temp_filename,
                    chunk_size=self.MULTIPART_CHUNK_SIZE,
                    callback=self.download_handler,
                )
            return True
        except FileNotFoundError:
            logger.info('File does not exist in storage', extra={'file_name': name})
            return False

    def get_seekable(self, name: str) -> SeekableStorage:
        key_name = self._name(name)
        with bucket_from_pool(self) as bucket:
            key = self.driver.bucket_get_key(bucket, key_name)
        return SeekableStorage(key)  # type: ignore[arg-type]

    def get(self, name: str, temp_filename: str) -> bool:
        if self.config.multipart_download_enabled:
            return self.get_large(name, temp_filename)
        key_name = self._name(name)
        try:
            with bucket_from_pool(self) as bucket:
                self.driver.bucket_download(bucket, key_name, temp_filename)
            return True
        except FileNotFoundError:
            logger.info('File does not exist in storage', extra={'file_name': name})
            return False
        except botocore.exceptions.ClientError:
            logger.error(
                'S3 get failed',
                extra={'file_name': name, 'local_file_name': temp_filename},
                exc_info=True,
            )
            return False

    def get_generator(self, name: str, **kwargs) -> StorageGenerator:
        key_name = self._name(name)
        load_key = kwargs.get('load_key', True)

        with bucket_from_pool(self) as bucket:
            key = self.driver.bucket_get_key(bucket, key_name, load_key=bool(load_key))

        if key is None:
            logger.error('No file in S3 storage', extra={'file_name': name})
            return StorageGenerator()

        iter_fun = self.driver.bucket_generator_download(key)
        return StorageGenerator(iter_fun)

    def put_large(self, name: str, source_path: str) -> bool:
        start = time.time()
        key_name = self._name(name)
        logging_info = {
            'source_size': os.stat(source_path).st_size,
            'local_filename': source_path,
            'server_file_name': key_name,
        }
        try:
            with bucket_from_pool(self) as bucket:
                self.driver.bucket_multipart_upload(
                    bucket,
                    key_name,
                    source_path,
                    chunk_size=self.MULTIPART_CHUNK_SIZE,
                    callback=self.upload_handler,
                    logging_info=logging_info,
                )
        except botocore.exceptions.ClientError:
            msg = "S3 Put Failed. Indicates problem with authentication or encryption settings"
            logger.error(
                msg, extra={'file_name': name, 'local_file_name': source_path}, exc_info=True
            )
            return False
        except Exception:
            # DR-8240 Handle all types of AWS S3 errors by returning false
            # in the put_large function on any AWS exception
            # The retries themselves are covered in the store_file function
            logger.warning('Failed to put file in S3', extra=logging_info, exc_info=True)
            return False
        # DSX-3377 Let's put proper tracing in here
        logger.debug("S3 put_large success", extra={'duration': str(time.time() - start)})
        return True

    def put(self, name: str, local_filename: str) -> bool:
        if not os.path.exists(local_filename):
            return False
        if self.config.multipart_upload_enabled:
            return self.put_large(name, local_filename)
        start = time.time()
        key_name = self._name(name)
        try:
            with bucket_from_pool(self) as bucket:
                self.driver.bucket_upload(bucket, key_name, local_filename)
        except botocore.exceptions.ClientError:
            msg = "S3 Put Failed. Indicates problem with authentication or encryption settings"
            logger.error(
                msg, extra={'file_name': name, 'local_file_name': local_filename}, exc_info=True
            )
            return False
        except Exception:
            logger.error(
                "Failed to put file into storage",
                extra={'file_name': name, 'local_file_name': local_filename},
                exc_info=True,
            )
            return False
        # DSX-3377 use proper tracing here rather than debug log
        logger.debug("S3 put success", extra={'duration': str(time.time() - start)})
        return True

    def put_generator(self, name: str, source: PutGenerator) -> bool:
        start = time.time()
        key_name = self._name(name)

        def spool_source_files():
            # Break the source stream up into chunk-size temporary files.
            # Using real files (vs eg BytesIO) because it's known to work,
            # retry requests that got internal errors (see "Amazon S3 error
            # best practices"), and may be easier to scale for parallel
            # uploads.
            first = True
            while True:
                nbytes = 0
                with tempfile.NamedTemporaryFile(dir=self.local_data_directory) as tf:
                    while nbytes < self.MULTIPART_CHUNK_SIZE:
                        resid = self.MULTIPART_CHUNK_SIZE - nbytes
                        buf = source.read(resid)
                        if not buf:
                            break  # EOF from source.
                        tf.write(buf)
                        nbytes += len(buf)
                    if first or nbytes > 0:
                        # Yield the first block, then any block with data.
                        tf.flush()
                        tf.seek(0)
                        yield nbytes, tf
                    if nbytes == 0:
                        break
                    first = False

        with bucket_from_pool(self) as bucket:
            try:
                mp = self.driver.MultipartUploader(bucket, self.config, key_name)
            except botocore.exceptions.ClientError:
                msg = "S3 Put Failed. Indicates problem with authentication or encryption settings"
                logger.error(msg, extra={'file_name': name}, exc_info=True)
                return False

            logging_info = {
                'server_file_name': key_name,
                'local_filename': '-',
                'source_size': -1,
                'chunk_count': -1,
            }

            logger.debug('Uploading file stream in chunks', extra=logging_info)

            try:
                offset = 0
                chunk_no = 0
                for nbytes, fp in spool_source_files():
                    logging_info.update({'chunk_number': chunk_no, 'byte_offset': offset})
                    logger.debug('Uploading stream chunk', extra=logging_info)
                    mp.upload_part(fp, chunk_no + 1)
                    self.upload_handler(offset, nbytes, -1)
                    offset += nbytes
                    chunk_no += 1

                mp.complete_upload()

            except Exception:
                logger.error('Failed to put stream to S3', extra=logging_info, exc_info=True)
                try:
                    mp.abort_multipart_upload()
                except Exception:
                    pass  # Silently ignore.
                return False

        # DSX-3377 use proper tracing here instead of debug logging
        logger.debug('Put file stream success', extra={'duration': str(time.time() - start)})
        return True

    def copy(self, name: str, new_name: str) -> bool:
        """Copy a file within a bucket"""
        source_key_name = self._name(name)
        dest_key_name = self._name(new_name)
        try:
            with bucket_from_pool(self) as bucket:
                self.driver.bucket_copy_key(bucket, dest_key_name, source_key_name)
            return True
        except FileNotFoundError:
            logger.info('File does not exist in storage', extra={'file_name': name})
            return False
        except botocore.exceptions.ClientError:
            msg = "S3 Copy Failed. Indicates problem with authentication or encryption settings"
            logger.error(msg, extra={'file_name': name, 'new_name': new_name}, exc_info=True)
            return False
        except Exception:
            logger.error(
                "Failed to copy file",
                extra={'file_name': name, 'new_name': new_name},
                exc_info=True,
            )
            return False

    def delete(self, name: str) -> bool:
        key_name = self._name(name)
        try:
            with bucket_from_pool(self) as bucket:
                self.driver.bucket_delete_key(bucket, key_name)
        except FileNotFoundError:
            # Tests expect False.  Would prefer to be True.
            return False
        except Exception:
            logger.error(
                "Failed to delete file from storage", extra={'file_name': name}, exc_info=True
            )
            return False
        return True

    def url(self, name: str, expires_in: Optional[int] = 600) -> Optional[str]:
        key_name = self._name(name)
        try:
            with bucket_from_pool(self) as bucket:
                url = self.driver.bucket_generate_presigned_url(bucket, key_name, expires_in)
        except FileNotFoundError:
            logger.info("No url for file in storage", extra={'file_name': name})
            return None
        if url is None:
            logger.info("No url for file in storage", extra={'file_name': name}, exc_info=True)
        return url

    def file_size(self, name: str) -> int:
        if self.exists(name):
            key_name = self._name(name)
            with bucket_from_pool(self) as bucket:
                key = self.driver.bucket_get_key(bucket, key_name)
                if key is not None:
                    return int(key.size)
        return 0

    def delete_batch(self, name_iter: Iterable, batch_size: Optional[int] = 1000) -> None:
        # The officially documented limit is 1k requests per batch.
        # We allow it as a parameter only to make testing faster.
        if batch_size is None:
            batch_size = 1000
        with bucket_from_pool(self) as bucket:
            for sub_list in self.name_list_chunks(name_iter, batch_size):
                # DSX-3377 use proper tracing here instead of debug logging
                logger.debug(
                    'S3 begin delete_batch',
                    extra={'nfiles': len(sub_list), 'now': time.ctime(), 'sub_list': sub_list},
                )
                sub_list = [self._name(name) for name in sub_list]
                try:
                    self.driver.bucket_delete_key_batch(bucket, sub_list)
                except Exception:
                    logger.warning('S3 delete_batch: error', exc_info=True)
                logger.debug(
                    'S3 done delete_batch', extra={'nfiles': len(sub_list), 'now': time.ctime()}
                )

    def delete_all(self, name: str) -> None:
        """This is meant to be a corollary to rmdir, but be careful because
        directories don't exist in S3 per se, just prefixes (which, due to
        our use of the '/' delimiter, look an awful lot like directories)
        """
        key_name = self._name(name)
        with bucket_from_pool(self) as bucket:
            for key in self.driver.bucket_list_generator(bucket, prefix=key_name):
                key.delete()

    def last_modified_get_downloadable_package_info(self, name: str):
        # Optimization needed by common.mlops.download.get_downloadable_package_info.
        # We need the handle to the bucket item to get last mod time.  The exact filename
        # (key) path is provided, so the result set should be length == 1.
        # Return value is a string, eg "2009-10-12T17:50:30.000Z"
        key_name = self._name(name)
        with bucket_from_pool(self) as bucket:
            # Need to use `Bucket.list` in boto(2) to get the expected time format.
            keys = self.driver.bucket_list(bucket, prefix=key_name)
            if not keys:
                # Legacy formatted log message:
                # pylint: disable=logging-dynamic-error-message
                logger.warning("Failed to get mod time for S3 object %s", key_name)
                return None
            timestamp = keys[0].last_modified
            return timestamp

    def list_keys_by_prefix(self, prefix: str):
        # Optimization needed by ModelingMachine.engine.scale_out.socommon.S3ScoringAccessor
        # Recursively find all keys starting with the given prefix.
        # TODO: Add to Storage interface and other Storage flavours
        remote_prefix = self._name(prefix)
        with bucket_from_pool(self) as bucket:
            return self.driver.bucket_list(bucket, prefix=remote_prefix)

    def root_location(self) -> str:
        """
        Return root location for the storage.

        That has to be in URL format and include schema, bucket (for blob storage) and prefix.
        For example: s3://my_bucket/my_prefix

        Returns
        -------
        location : str
            Storage root location.
        """
        return os.path.join(f"s3://{self.bucket_name}", self.prefix)
