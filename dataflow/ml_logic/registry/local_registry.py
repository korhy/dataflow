import os
import pickle
from typing import Any, List
from .abstract_registry import AbstractModelRegistry
from .singleton import SingletonABCMeta
from dataflow.params import LOCAL_REGISTRY_DIR

class LocalModelRegistry(AbstractModelRegistry, metaclass=SingletonABCMeta):
    """A local file-based model registry."""

    def __init__(self, storage_dir: str = LOCAL_REGISTRY_DIR):
        self.storage_dir = os.path.abspath(storage_dir)
        if not os.path.isabs(self.storage_dir):
            raise ValueError("storage_dir must be an absolute path.")
        os.makedirs(self.storage_dir, exist_ok=True)

    def _model_path(self, model_name: str) -> str:
        return os.path.join(self.storage_dir, f"{model_name}.pkl")

    def register_model(self, model_name: str, model_object: Any, **kwargs) -> None:
        model_path = self._model_path(model_name)
        if os.path.exists(model_path):
            raise FileExistsError(f"Model '{model_name}' already exists.")
        with open(model_path, 'wb') as f:
            pickle.dump(model_object, f)

    def get_model(self, model_name: str, **kwargs) -> Any:
        model_path = self._model_path(model_name)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model '{model_name}' not found.")
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    def list_models(self, **kwargs) -> List[str]:
        return [f[:-4] for f in os.listdir(self.storage_dir) if f.endswith('.pkl')]

    def delete_model(self, model_name: str, **kwargs) -> None:
        model_path = self._model_path(model_name)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model '{model_name}' not found.")
        os.remove(model_path)

    def update_model(self, model_name: str, model_object: Any, **kwargs) -> None:
        model_path = self._model_path(model_name)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model '{model_name}' not found.")
        with open(model_path, 'wb') as f:
            pickle.dump(model_object, f)
