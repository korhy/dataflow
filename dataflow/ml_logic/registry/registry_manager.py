from typing import Dict, Type
from .abstract_registry import AbstractModelRegistry
from .local_registry import LocalModelRegistry
# import other registries as you add them

class RegistryManager:
    """Manages singleton instances of all registries by name."""

    _registry_classes: Dict[str, Type[AbstractModelRegistry]] = {
        "local": LocalModelRegistry,
        # "mlflow": MLflowRegistry,
        # "bigquery": BigQueryRegistry,
        # etc.
    }

    _instances: Dict[str, AbstractModelRegistry] = {}

    @classmethod
    def get_registry(cls, registry_name: str) -> AbstractModelRegistry:
        if registry_name not in cls._registry_classes:
            raise ValueError(f"Unknown registry: {registry_name}")
        if registry_name not in cls._instances:
            cls._instances[registry_name] = cls._registry_classes[registry_name]()
        return cls._instances[registry_name]

    @classmethod
    def list_available_registries(cls):
        return list(cls._registry_classes.keys())
