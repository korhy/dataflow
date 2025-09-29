from .abstract_registry import AbstractModelRegistry
from .singleton import SingletonABCMeta
from .registry_manager import RegistryManager
from google.cloud import storage
from dataflow.params import GCS_REGISTRY_BUCKET_NAME
from tensorflow import keras

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

    def get_model(self, model_name: str):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(f"models/{model_name}")
        if not blob.exists():
            raise FileNotFoundError(f"Model '{model_name}' not found in GCS.")

        # Download to a temporary local file
        local_registry = RegistryManager.get_registry("local")
        blob.download_to_filename(local_registry._model_path(model_name))

        return local_registry.get_model(model_name)

    def list_models(self, **kwargs):
        bucket = self.client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix="models/")
        return [blob.name.split("/")[-1] for blob in blobs if blob.name != "models/"]

    def delete_model(self, model_name: str, **kwargs):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(f"models/{model_name}")
        if not blob.exists():
            raise FileNotFoundError(f"Model '{model_name}' not found in GCS.")
        blob.delete()

        # Also delete from local registry if exists
        local_registry = RegistryManager.get_registry("local")
        try:
            local_registry.delete_model(model_name)
        except FileNotFoundError:
            pass  # Ignore if not found locally

    def update_model(self, model_name: str, model_object, **kwargs):
        # Save model locally
        local_registry = RegistryManager.get_registry("local")
        local_registry.update_model(model_name, model_object)

        # Upload to GCS
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(f"models/{model_name}")
        blob.upload_from_filename(local_registry._model_path(model_name))

        # Clean up local copy
        local_registry.delete_model(model_name)
