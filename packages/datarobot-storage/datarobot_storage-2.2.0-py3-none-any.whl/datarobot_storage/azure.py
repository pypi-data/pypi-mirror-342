# coding=utf-8
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
#
from __future__ import absolute_import
from __future__ import division

import datetime
import logging
import os
import time
from collections.abc import Mapping
from functools import partial
from typing import List
from typing import Optional
from typing import Union
from urllib.parse import quote

import typing_extensions

# pylint: disable=no-name-in-module
from azure.core import exceptions
from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
from azure.storage import blob

from datarobot_storage.base import SeekableKeyInterface
from datarobot_storage.base import SeekableStorage
from datarobot_storage.base import Storage
from datarobot_storage.base import StorageGenerator

SIGNED_BLOB_URL_TEMPLATE = (
    'https://{account_name}.blob.core.windows.net/{container_name}/{remote_name}?{blob_sas_token}'
)
BLOB_SAS_PERMISSIONS = blob.BlobSasPermissions(read=True, list=True)


logger = logging.getLogger(__name__)


class AzureKey(SeekableKeyInterface):
    """
    TODO: replace use of `self.blob_service_client.get_blob_client` with `self.get_key(name).client`
    """

    def __init__(self, name=None, client=None):
        self.name = name
        self.client = client

    def get_range(self, offset: int, size: int):
        return self.client.download_blob(offset=offset).read(size=size)

    @property
    def size(self):
        return self.client.get_blob_properties().size


class AzureBlobStorageConfig(object):
    """
    All Azure Blob Storage access configuration parameters in one place.

    Parameters
    ----------
    prefix : str, optional
        A prefix to be used when constructing file path or storage key.
    container_name : str
        The name of the Azure Blob Storage container.
    connection_string : str, optional
        The connection string for accessing Azure Blob Storage.
    account_name : str, optional
        The Azure Storage account name.
    account_key : str, optional
        The account key for authentication.
    tenant_id : str, optional
        The Azure Active Directory tenant ID.
    client_id : str, optional
        The client (application) ID for authentication.
    client_secret : str, optional
        The client secret for authentication.
    token_file : str, optional
        Token file path where azure federated token is stored
    authority_host : str, optional
        The Azure authority host

    Raises
    ------
    ValueError
        If `container_name` is not provided or an empty string.
    ValueError
        If neither `connection_string` nor `account_name` is provided.

    Attributes
    ----------
    prefix : str
        A prefix to be used when constructing file path or storage key.
    connection_string : str
        The connection string for accessing Azure Blob Storage.
    account_name : str
        The Azure Storage account name.
    account_key : str
        The account key for authentication.
    container_name : str
        The name of the Azure Blob Storage container.
    tenant_id : str
        The Azure Active Directory tenant ID.
    client_id : str
        The client (application) ID for authentication.
    client_secret : str
        The client secret for authentication.
    token_file : str
        Token file path where azure federated token is stored
    authority_host : str
        The Azure authority host
    """

    prefix: str
    container_name: Optional[str]
    connection_string: Optional[str]
    account_name: Optional[str]
    account_key: Optional[str]
    tenant_id: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    token_file: Optional[str]
    authority_host: Optional[str]

    def __init__(
        self,
        prefix: str = "",
        container_name: Optional[str] = None,
        connection_string: Optional[str] = None,
        account_name: Optional[str] = None,
        account_key: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_file: Optional[str] = None,
        authority_host: Optional[str] = None,
    ):
        self.connection_string = connection_string
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.prefix = prefix
        self.token_file = token_file
        self.authority_host = authority_host

        if not self.container_name:
            raise ValueError("AZURE_BLOB_STORAGE_CONTAINER_NAME is required")

        if not self.connection_string and not self.account_name:
            raise ValueError(
                "Either AZURE_BLOB_STORAGE_ACCOUNT_NAME or "
                "AZURE_BLOB_STORAGE_CONNECTION_STRING are required"
            )

    def __repr__(self) -> str:
        details = dict(container=self.container_name, authentication='managed_identity')

        if self.is_shared_key:
            details['authentication'] = 'shared_key'
        if self.is_service_principal:
            details['authentication'] = 'service_principal'

        details_string = ', '.join(f"{k}='{v}'" for k, v in details.items())
        return f"{self.__class__.__name__}({details_string})"

    @property
    def is_shared_key(self) -> bool:
        return bool(self.account_name and self.account_key)

    @property
    def is_connection_string(self) -> bool:
        return bool(self.connection_string)

    @property
    def is_service_principal(self) -> bool:
        return bool(self.account_name and self.client_id and self.tenant_id and self.client_secret)

    @property
    def credential(self) -> Union[DefaultAzureCredential, ClientSecretCredential, str]:
        if self.is_shared_key:
            logger.debug('Using Shared Key Secret to connect to Azure Blob Service')
            return self.account_key  # type: ignore[return-value]

        if self.is_service_principal:
            logger.debug('Using Service Principal credentials to connect to Azure Blob Service')
            return ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)  # type: ignore[arg-type]

        logger.debug('Authenticate as Azure Managed Identity to connect to Azure Blob Service')
        return DefaultAzureCredential()

    @property
    def account_url(self) -> str:
        if not self.account_name:
            raise ValueError("AZURE_BLOB_STORAGE_ACCOUNT_NAME is required")

        return 'https://{account_name}.blob.core.windows.net'.format(account_name=self.account_name)

    @classmethod
    def from_dict(cls, _dict: Mapping) -> typing_extensions.Self:
        return cls(
            connection_string=_dict.get('AZURE_BLOB_STORAGE_CONNECTION_STRING'),
            account_name=_dict.get('AZURE_BLOB_STORAGE_ACCOUNT_NAME'),
            account_key=_dict.get('AZURE_BLOB_STORAGE_ACCOUNT_KEY'),
            container_name=_dict.get('AZURE_BLOB_STORAGE_CONTAINER_NAME', ''),
            tenant_id=_dict.get('AZURE_TENANT_ID'),
            client_id=_dict.get('AZURE_CLIENT_ID'),
            client_secret=_dict.get('AZURE_CLIENT_SECRET'),
            prefix=_dict.get('FILE_STORAGE_PREFIX', ''),
            token_file=_dict.get('AZURE_FEDERATED_TOKEN_FILE', ''),
            authority_host=_dict.get('AZURE_AUTHORITY_HOST', ''),
        )


class AzureBlobStorage(Storage):

    prefix: str
    config: AzureBlobStorageConfig
    blob_service_client: blob.BlobServiceClient

    def __init__(
        self,
        connection_string: Optional[str] = None,
        account_name: Optional[str] = None,
        account_key: Optional[str] = None,
        container_name: Optional[str] = None,
        storage_config: Optional[AzureBlobStorageConfig] = None,
    ):
        super().__init__()
        self.config = storage_config or AzureBlobStorageConfig.from_dict(os.environ)
        self.prefix = self.config.prefix

        # Things we historically allow to override from __init__ arguments
        self.config.connection_string = connection_string or self.config.connection_string
        self.config.account_name = account_name or self.config.account_name
        self.config.account_key = account_key or self.config.account_key
        self.config.container_name = container_name or self.config.container_name

        self.blob_service_client = self._init_blob_service_client(self.config)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(config={self.config})"

    @property
    def client(self) -> blob.BlobServiceClient:
        return self.blob_service_client  # type: ignore[no-any-return]

    @staticmethod
    def _init_blob_service_client(config: AzureBlobStorageConfig) -> blob.BlobServiceClient:
        """
        Choose proper method and construct BlobServiceClient according to configuration.
        """
        if config.is_connection_string:
            logger.debug('Using Connection String to connect to Azure Blob Service')
            return blob.BlobServiceClient.from_connection_string(config.connection_string)  # type: ignore[arg-type]

        return blob.BlobServiceClient(config.account_url, credential=config.credential)

    @property
    def container_name(self) -> str:
        return str(self.config.container_name)

    @property
    def azure_blob_account_key(self) -> Optional[str]:
        return self.config.account_key  # type: ignore[no-any-return]

    @property
    def azure_blob_account_name(self) -> Optional[str]:
        return self.config.account_name  # type: ignore[no-any-return]

    def get_key(self, name: str) -> AzureKey:
        remote_name = self._name(name)
        blob_client = self.blob_service_client.get_blob_client(self.container_name, remote_name)
        return AzureKey(name=remote_name, client=blob_client)

    def exists(self, name: str) -> bool:
        """
        Check if blob exists for a specific container.

        Parameters
        ----------
        name: str
            Name of blob
        """
        remote_name = self._name(name)
        exists = bool(
            self.blob_service_client.get_blob_client(self.container_name, remote_name).exists()
        )
        if not exists:
            logger.debug('Key not found in Azure Blob Storage', extra={'key': remote_name})
        return exists

    def url(self, name: str, expires_in: Optional[int] = 600) -> Optional[str]:
        if not self.exists(name):
            logger.error('No file in Azure Blob storage', extra={'file_name': name})
            return None

        remote_name = self._name(name)
        blob_client = self.blob_service_client.get_blob_client(self.container_name, remote_name)

        if not expires_in:
            return str(blob_client.url)

        now = datetime.datetime.now(datetime.timezone.utc)
        expiration_time = now + datetime.timedelta(seconds=expires_in)

        blob_sas_token_getter = partial(
            blob.generate_blob_sas,
            account_name=self.azure_blob_account_name,
            container_name=self.container_name,
            blob_name=remote_name,
            permission=BLOB_SAS_PERMISSIONS,
            expiry=expiration_time,
        )

        if self.azure_blob_account_key:
            blob_sas_token = blob_sas_token_getter(account_key=self.azure_blob_account_key)
        else:
            delegation_key = self.blob_service_client.get_user_delegation_key(now, expiration_time)
            blob_sas_token = blob_sas_token_getter(user_delegation_key=delegation_key)

        return SIGNED_BLOB_URL_TEMPLATE.format(
            account_name=self.azure_blob_account_name,
            container_name=self.container_name,
            remote_name=quote(remote_name),
            blob_sas_token=blob_sas_token,
        )

    def file_size(self, name: str) -> int:
        if not self.exists(name):
            logger.error('No file in Azure Blob storage', extra={'file_name': name})
            return 0

        remote_name = self._name(name)
        size = (
            self.blob_service_client.get_blob_client(self.container_name, remote_name)
            .get_blob_properties()
            .size
        )
        return int(size)

    def list(self, path: str, recursive: bool = False) -> List[str]:
        """
        Get list of blobs for specific container.

        Parameters
        ----------
        path: str
            Prefix name for blob in container
        recursive : bool, optional
            List files in all subdirectories under the given `path`
        """
        original_path = path
        path = path.strip('/') if path else ''
        path = self._name(path).rstrip('/') + '/'
        client = self.blob_service_client.get_container_client(self.container_name)

        dirnames = []
        filenames = []

        if recursive:
            res = client.list_blobs(name_starts_with=path)
        else:
            res = client.walk_blobs(name_starts_with=path)

        for item in res:
            # That's what Azure calls a folder
            if isinstance(item, blob.BlobPrefix):
                dirnames.append(os.path.relpath(item.name, path))
                continue

            # That's what Azure calls a file
            if isinstance(item, blob.BlobProperties):
                path_start = self.prefix if recursive else path
                filenames.append(os.path.relpath(item.name, path_start))
                continue

            raise ValueError('Got an unknown item type when listing blobs')

        if not dirnames and not filenames:
            # Maybe it's a filename.
            if original_path and self.exists(original_path):
                filenames.append(original_path if recursive else os.path.basename(original_path))

        return dirnames + filenames

    def get(self, name: str, temp_filename: str) -> bool:
        """
        Get blob for specific container.

        Parameters
        ----------
        name: str
            Name of blob
        temp_filename
            Name of file object to store the blob
        """
        remote_name = self._name(name)

        try:
            downloader = self.blob_service_client.get_blob_client(
                self.container_name, remote_name
            ).download_blob()
        except exceptions.ResourceNotFoundError:
            logger.error('No file in Azure Blob storage', extra={'file_name': name})
            return False

        with open(temp_filename, 'wb') as stream:
            downloader.readinto(stream)

        return True

    def get_generator(self, name: str, **kwargs) -> StorageGenerator:
        """
        Returns generator to fetch blob in chunks.

        Parameters
        ----------
        name: str
            Name of blob
        """
        if not self.exists(name):
            logger.error('No file in Azure Blob storage', extra={'file_name': name})
            return StorageGenerator()

        remote_name = self._name(name)
        blob_client = self.blob_service_client.get_blob_client(self.container_name, remote_name)

        def create_generator(offset=0):
            offset = offset or None  # BlobClient.download_blob expects it to be None instead of 0
            return blob_client.download_blob(offset=offset).chunks()

        # Default chunk size is 4MB and can be changed during BlobServiceClient initialization.
        # (Using max_single_get_size or max_chunk_get_size).
        return StorageGenerator(create_generator)

    def put(self, name: str, local_filename: str) -> bool:
        """
        Upload file into blob for specific container.

        Parameters
        ----------
        name: str
            Name of blob
        local_filename
            Name of file object to upload into the blob
        """
        remote_name = self._name(name)

        logging_extra = {
            'file_name': name,
            'local_file': local_filename,
            'storage_path': remote_name,
        }

        try:
            client = self.blob_service_client.get_blob_client(self.container_name, remote_name)
            with open(local_filename, 'rb') as stream:
                client.upload_blob(stream, overwrite=True)
        except Exception:
            logger.error("Failed to put file into storage", extra=logging_extra, exc_info=True)
            return False
        return True

    def copy(self, name: str, new_name: str) -> bool:
        """
        For copying within storage.

        Parameters
        ----------
        name: str
            Name of blob which will be copied
        new_name
            Name of new blob
        """
        blob_url = self.url(name)
        if blob_url is None:
            return False

        remote_name_copy = self._name(new_name)
        blob_client = self.blob_service_client.get_blob_client(
            self.container_name, remote_name_copy
        )

        blob_client.start_copy_from_url(blob_url)
        status = blob_client.get_blob_properties().copy.status

        while status == 'pending':
            status = blob_client.get_blob_properties().copy.status
            time.sleep(5)  # Polling each 5s to check if copy process is completed

        if status == 'success':
            return True

        # (status in ('failed', 'aborted')
        logger.error('Failed to make a copy', extra={'source': name, 'destination': new_name})
        return False

    def delete(self, name: str) -> bool:
        """
        Delete blob.

        Parameters
        ----------
        name: str
            Name of blob to delete
        """

        try:
            if not self.exists(name):
                logger.error('No file in Azure Blob storage', extra={'file_name': name})
                return False

            remote_name = self._name(name)
            self.blob_service_client.get_blob_client(self.container_name, remote_name).delete_blob()

        except Exception:
            logger.error(
                'Failed to delete file from storage', extra={'file_name': name}, exc_info=True
            )
            return False

        return True

    def delete_all(self, name: Optional[str] = None) -> None:
        """
        Just to support test cleanup. Don't use this in production. It's slow.
        """
        name = name or str()

        prefixed_name = self._name(name)
        blob_iter = self.blob_service_client.get_container_client(self.container_name).list_blobs(
            name_starts_with=prefixed_name,
        )

        for item in blob_iter:
            if name and not item.name.startswith(prefixed_name):
                continue

            self.blob_service_client.get_blob_client(self.container_name, item.name).delete_blob()

        return

    def get_seekable(self, name: str) -> SeekableStorage:
        return SeekableStorage(self.get_key(name))
