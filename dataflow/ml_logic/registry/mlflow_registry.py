from .abstract_registry import AbstractModelRegistry
from .singleton import SingletonABCMeta
from .registry_manager import RegistryManager
import mlflow
from mlflow.tracking import MlflowClient

class MLflowRegistry(AbstractModelRegistry, metaclass=SingletonABCMeta):
    """A placeholder for MLflow-based model registry."""

    def __init__(self, *args, **kwargs):
        self.client = MlflowClient()

    def register_model(self, model_name, model_object, **kwargs):
        mlflow.tensorflow.log_model(
            model=model_object,
            artifact_path=model_name,
            registered_model_name=model_name
        )

    def get_model(self, model_name: str):
        raise NotImplementedError("MLflowRegistry is not yet implemented.")

    def list_models(self, **kwargs):
        raise NotImplementedError("MLflowRegistry is not yet implemented.")

    def delete_model(self, model_name: str, **kwargs):
        raise NotImplementedError("MLflowRegistry is not yet implemented.")

    def update_model(self, model_name: str, model_object, **kwargs):
        raise NotImplementedError("MLflowRegistry is not yet implemented.")
