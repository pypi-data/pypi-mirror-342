from .storage import StorageService
from .tools import register_tools
from .resource import register_resource_provider
from ...config import config


def load(cfg: config.Config):
    storage_service = StorageService(cfg)
    register_tools(storage_service)
    register_resource_provider(storage_service)


__all__ = ["load", "StorageService"]
