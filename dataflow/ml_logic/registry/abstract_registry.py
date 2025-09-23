from abc import ABC, abstractmethod
from typing import Any, List

class AbstractModelRegistry(ABC):
    """Abstract base class for a model registry."""

    @abstractmethod
    def register_model(self, model_name: str, model_object: Any, **kwargs) -> None:
        """Register a new model."""
        pass

    @abstractmethod
    def get_model(self, model_name: str, **kwargs) -> Any:
        """Retrieve a model by name."""
        pass

    @abstractmethod
    def list_models(self, **kwargs) -> List[str]:
        """List all registered model names."""
        pass

    @abstractmethod
    def delete_model(self, model_name: str, **kwargs) -> None:
        """Delete a model by name."""
        pass

    # Optional: update_model
    def update_model(self, model_name: str, model_object: Any, **kwargs) -> None:
        """Update an existing model. Override if needed."""
        raise NotImplementedError("update_model is not implemented.")
