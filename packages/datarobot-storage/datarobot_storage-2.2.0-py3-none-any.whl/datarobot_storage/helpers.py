# Copyright 2023 DataRobot, Inc. and its affiliates.
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
import asyncio
import functools
import os
from typing import Mapping
from typing import Optional

from datarobot_storage.amazon import S3Configuration
from datarobot_storage.amazon import S3Storage
from datarobot_storage.azure import AzureBlobStorage
from datarobot_storage.azure import AzureBlobStorageConfig
from datarobot_storage.base import AsyncStorage
from datarobot_storage.base import Storage
from datarobot_storage.enums import FileStorageBackend
from datarobot_storage.google import GoogleStorage
from datarobot_storage.google import GoogleStorageConfig
from datarobot_storage.utils.async_storage import AsyncStorageWrapper


def get_storage(
    storage_type: Optional[str] = None, config_dict: Optional[Mapping] = None
) -> Storage:
    """
    Get an instance of the file storage backend based on the provided storage type.

    Parameters
    ----------
    storage_type : str, optional
        Type of file storage backend. If not provided, it defaults
        to the value of the 'FILE_STORAGE_TYPE' environment variable.
    config_dict : Mapping or None, optional
        Dictionary defining configuration options for the storage, default to environment variables.

    Returns
    -------
    datarobot_storage.StorageType
        An instance of the corresponding file storage backend.

    Raises
    ------
    ValueError
        If arguyment storage_type is not defined and environment variable FILE_STORAGE_TYPE not set.
        If the specified storage type is not supported.
    NotImplementedError
        If the specified storage type is not supported yet.

    Notes
    -----
    The supported storage types are defined in the `datarobot_storage.FileStorageBackend` enum.

    Example
    -------
    >>> storage = get_storage(FileStorageBackend.S3)
    >>> isinstance(storage, S3Storage)
    True
    >>> get_storage().exists('/nonexistent')  # doctest: +SKIP
    False
    """
    config_dict = config_dict or os.environ
    storage_type = storage_type or config_dict.get('FILE_STORAGE_TYPE')

    if storage_type is None:
        raise ValueError('Undefined file storage type, set FILE_STORAGE_TYPE')
    elif storage_type not in FileStorageBackend.all():
        raise ValueError('Unsupported storage type requested')

    if storage_type == FileStorageBackend.S3:
        return S3Storage(storage_config=S3Configuration.from_dict(config_dict))

    elif storage_type == FileStorageBackend.AZURE_BLOB:
        return AzureBlobStorage(storage_config=AzureBlobStorageConfig.from_dict(config_dict))

    elif storage_type == FileStorageBackend.GOOGLE:
        return GoogleStorage(storage_config=GoogleStorageConfig.from_dict(config_dict))

    raise NotImplementedError('Storage type not supported yet')


def make_awaitable(storage: Storage) -> AsyncStorage:
    """
    Wrap Storage into a proxy object providing awaitable alternatives to Storage methods.
    """
    return AsyncStorageWrapper(storage)


def get_async_storage(*args, **kwargs) -> AsyncStorage:
    """
    Get an instance of the file storage with awaitable methods.

    Wraps get_storage helper, please refer to get_storage  documentation for usage details.
    """
    return make_awaitable(get_storage(*args, **kwargs))
