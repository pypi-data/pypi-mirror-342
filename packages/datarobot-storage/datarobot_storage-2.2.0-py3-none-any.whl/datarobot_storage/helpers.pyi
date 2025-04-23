from datarobot_storage.amazon import S3Configuration as S3Configuration, S3Storage as S3Storage
from datarobot_storage.azure import AzureBlobStorage as AzureBlobStorage, AzureBlobStorageConfig as AzureBlobStorageConfig
from datarobot_storage.base import AsyncStorage as AsyncStorage, Storage as Storage
from datarobot_storage.enums import FileStorageBackend as FileStorageBackend
from datarobot_storage.google import GoogleStorage as GoogleStorage, GoogleStorageConfig as GoogleStorageConfig
from datarobot_storage.utils.async_storage import AsyncStorageWrapper as AsyncStorageWrapper
from typing import Mapping

def get_storage(storage_type: str | None = None, config_dict: Mapping | None = None) -> Storage: ...
def make_awaitable(storage: Storage) -> AsyncStorage: ...
def get_async_storage(*args, **kwargs) -> AsyncStorage: ...
