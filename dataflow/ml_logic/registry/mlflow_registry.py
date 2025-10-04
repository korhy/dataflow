from dataflow.params import MLFLOW_TRACKING_URI
from .abstract_registry import AbstractModelRegistry
from .singleton import SingletonABCMeta
from .registry_manager import RegistryManager
import mlflow
from mlflow.tracking import MlflowClient
import os

class MLflowModelRegistry(AbstractModelRegistry, metaclass=SingletonABCMeta):
    """A placeholder for MLflow-based model registry."""

    def __init__(self, tracking_uri=MLFLOW_TRACKING_URI, experiment_name="Default", *args, **kwargs):
        # Set tracking URI
        mlflow.set_tracking_uri(tracking_uri)

        self.client = MlflowClient()
        self.experiment_name = experiment_name

        # Ensure experiment exists
        try:
            experiment = self.client.get_experiment_by_name(experiment_name)
            if experiment is None:
                experiment_id = self.client.create_experiment(experiment_name)
                print(f"✅ Created MLflow experiment: {experiment_name} (ID: {experiment_id})")
            else:
                experiment_id = experiment.experiment_id
                print(f"✅ Using existing MLflow experiment: {experiment_name} (ID: {experiment_id})")

            self.experiment_id = experiment_id
            mlflow.set_experiment(experiment_name)

        except Exception as e:
            print(f"❌ MLflow experiment setup failed: {e}")
            raise

    def _detect_model_type(self, model_object):
        """Detect the type of model and return appropriate logging function"""
        model_type = type(model_object).__module__

        # TensorFlow/Keras models
        if 'tensorflow' in model_type or 'keras' in model_type:
            return mlflow.tensorflow.log_model

        # Scikit-learn models
        elif 'sklearn' in model_type:
            return mlflow.sklearn.log_model

        # PyTorch models
        elif 'torch' in model_type:
            return mlflow.pytorch.log_model

        # XGBoost models
        elif 'xgboost' in model_type:
            return mlflow.xgboost.log_model

        # LightGBM models
        elif 'lightgbm' in model_type:
            return mlflow.lightgbm.log_model

        else:
            # Fallback to pickle for unknown types
            return mlflow.sklearn.log_model

    def register_model(self, model_name, model_object, metrics=None, params=None, **kwargs):
        # Detect appropriate logging function
        log_model_func = self._detect_model_type(model_object)

        with mlflow.start_run():
            mlflow.autolog()

            # Log metrics if provided
            if metrics:
                self.log_model_metrics(metrics)
            # Log params if provided
            if params:
                self.log_model_params(params)

            # Log the model
            if 'sklearn' in log_model_func.__module__:
                model_info = log_model_func(
                    sk_model=model_object,
                    artifact_path='model',
                    registered_model_name=model_name
                )
            else:
                model_info = log_model_func(
                    model=model_object,
                    artifact_path='model',
                    registered_model_name=model_name
                )

        print(f"✅ Model '{model_name}' registered successfully!")
        return model_info

    def get_model(self, model_name: str, stage='Production'):
        #Load Model from MLFlow
        try:
            model_versions = self.client.get_latest_versions(name=model_name, stages=[stage])
            model_uri = model_versions[0].source
            assert model_uri is not None
        except:
            print(f"\n❌ No model found with name {model_name} in stage {stage}")
            return None

        model = mlflow.tensorflow.load_model(model_uri=model_uri)

        print("✅ model loaded from mlflow")
        return model

    def list_models(self, **kwargs):
        data = self.client.search_registered_models()
        models = []
        for model in data:
            models.append(model.name)
        result = []
        for model in models:
            model_versions = {"name": model}
            data = self.client.search_model_versions(filter_string =f"name='{model}'")
            versions = list(map(lambda x: dict(x), data))
            model_versions["latest_versions"] = versions
            result.append(model_versions)

        return result

    def delete_model(self, model_name: str, **kwargs):
        self.client.delete_registered_model(name=model_name)
        print(f"✅ Model '{model_name}' deleted successfully.")

    def update_model(self, model_name: str, model_object, **kwargs):
        # For MLflow, updating a model typically means registering a new version
        self.register_model(model_name, model_object, **kwargs)

    def transition_model_stage(self, model_name: str, version: str, stage: str, archive_existing_versions: bool = False, **kwargs):
        """
        Transition a model version to a specified stage.
         Args:
             model_name (str): The name of the registered model.
             version (str): The version of the model to transition.
             stage (str): The target stage (e.g., "Staging", "Production", "Archived").
             archive_existing_versions (bool): Whether to archive existing versions in the target stage.
         """
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
            archive_existing_versions=archive_existing_versions
        )
        print(f"✅ Model '{model_name}' version {version} transitioned to stage '{stage}'.")


    def log_model_metrics(self, metrics: dict, **kwargs):
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
            print(f"✅ Logged metric: {key} = {value}")

    def log_model_params(self, params: dict, **kwargs):
        for key, value in params.items():
            mlflow.log_param(key, value)
            print(f"✅ Logged param: {key} = {value}")
