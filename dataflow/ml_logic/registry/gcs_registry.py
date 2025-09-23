from .abstract_registry import AbstractModelRegistry
from .singleton import SingletonABCMeta
from .registry_manager import RegistryManager
from google.cloud import storage
from dataflow.params import GCS_REGISTRY_BUCKET_NAME

class GCSModelRegistry(AbstractModelRegistry, metaclass=SingletonABCMeta):
    """A Google Cloud Storage-based model registry."""

    def __init__(self, bucket_name: str = GCS_REGISTRY_BUCKET_NAME):
        self.client = storage.Client()
        self.bucket_name = bucket_name

    def register_model(self, model_name, model_object, **kwargs):
        # Save model locally
        local_registry = RegistryManager.get_registry("local")
        local_registry.register_model(model_name, model_object)

        # Upload to GCS
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(f"models/{model_name}")
        blob.upload_from_filename(local_registry._model_path(model_name))

        # Clean up local copy
        local_registry.delete_model(model_name)
