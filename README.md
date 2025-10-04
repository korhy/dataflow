# 🚀 DataFlow

**DataFlow** is a comprehensive Python package for machine learning model management and deployment. It provides a unified interface to manage your ML models across different storage backends with a clean, extensible architecture.

## ✨ Features

- **🏠 Local Registry**: Store models as pickle files locally
- **☁️ Google Cloud Storage**: Store models in GCS buckets
- **📊 MLflow Integration**: Full MLflow tracking and model registry support
- **🔄 Singleton Pattern**: Efficient instance management
- **🎯 Abstract Interface**: Consistent API across all backends
- **🛠️ Auto Model Detection**: Automatically detects model types (sklearn, tensorflow, etc.)

## 📦 Installation

### Prerequisites
- Python 3.8+
- Required dependencies will be installed automatically

### Install from source
```bash
git clone https://github.com/korhy/dataflow.git
cd dataflow
pip install -e .
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Local Model Registry

```python
from dataflow.ml_logic.registry.local_registry import LocalModelRegistry

# Create registry instance
registry = LocalModelRegistry()

# Register a model
model = train_your_model()  # Your trained model
registry.register_model("my_model", model)

# Load the model
loaded_model = registry.get_model("my_model")

# List all models
models = registry.list_models()

# Update a model
registry.update_model("my_model", updated_model)

# Delete a model
registry.delete_model("my_model")
```

### 2. Google Cloud Storage Registry

```python
from dataflow.ml_logic.registry.gcs_registry import GCSModelRegistry

# Create GCS registry (requires GCS_REGISTRY_BUCKET_NAME in .env)
gcs_registry = GCSModelRegistry()

# Same API as local registry
gcs_registry.register_model("my_model", model)
loaded_model = gcs_registry.get_model("my_model")
```

### 3. MLflow Registry

```python
from dataflow.ml_logic.registry.mlflow_registry import MLflowModelRegistry

# Create MLflow registry
mlflow_registry = MLflowModelRegistry()

# Register model with metrics and parameters
mlflow_registry.register_model(
    "my_model",
    model,
    metrics={"accuracy": 0.95, "f1_score": 0.93},
    params={"learning_rate": 0.01, "epochs": 100}
)

# Load model
loaded_model = mlflow_registry.get_model("my_model")

# Transition model stage
mlflow_registry.transition_model_stage("my_model", "1", "Production")
```

## ⚙️ Configuration

Create a `.env` file in your project root:

```bash
# Local Registry
LOCAL_REGISTRY_DIR=./models

# Google Cloud Storage
GCS_REGISTRY_BUCKET_NAME=your-gcs-bucket-name

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5001
```

## 🏗️ Architecture

```
dataflow/
├── ml_logic/
│   └── registry/
│       ├── abstract_registry.py      # Base abstract class
│       ├── local_registry.py         # Local file storage
│       ├── gcs_registry.py          # Google Cloud Storage
│       ├── mlflow_registry.py       # MLflow integration
│       ├── singleton.py             # Singleton metaclass
│       └── registry_manager.py      # Registry factory
└── params.py                       # Configuration parameters
```

## 🔧 Advanced Usage

### Registry Manager (Factory Pattern)

```python
from dataflow.ml_logic.registry.registry_manager import RegistryManager

# Get registry by name
local_registry = RegistryManager.get_registry("local")
gcs_registry = RegistryManager.get_registry("gcs")
mlflow_registry = RegistryManager.get_registry("mlflow")

# List available registries
available = RegistryManager.list_available_registries()
```

### Custom Model Types

The MLflow registry automatically detects and handles:
- **Scikit-learn** models
- **TensorFlow/Keras** models
- **PyTorch** models
- **XGBoost** models
- **LightGBM** models

### Singleton Pattern

All registries use singleton pattern for efficient resource management:

```python
# These will return the same instance
registry1 = LocalModelRegistry()
registry2 = LocalModelRegistry()
assert registry1 is registry2  # True

# Clear instances if needed
from dataflow.ml_logic.registry.singleton import SingletonABCMeta
SingletonABCMeta._instances.clear()
```

## 🧪 Testing

Run the test suite:

```bash
python -m unittest discover -s tests
```

Run specific tests:

```bash
python -m unittest tests.test_local_registry
```

## 📁 Project Structure

```
dataflow/
├── dataflow/
│   ├── __init__.py
│   ├── params.py
│   └── ml_logic/
│       ├── __init__.py
│       └── registry/
│           ├── __init__.py
│           ├── abstract_registry.py
│           ├── local_registry.py
│           ├── gcs_registry.py
│           ├── mlflow_registry.py
│           ├── singleton.py
│           └── registry_manager.py
├── tests/
│   ├── __init__.py
│   ├── test_local_registry.py
│   └── test_singleton.py
├── .env.sample
├── requirements.txt
├── pyproject.toml
├── docker-compose.yml
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/korhy/dataflow/issues) page
2. Create a new issue with detailed information
3. Contact: clementboudinel@gmail.com

## 🚀 Roadmap

- [ ] Add AWS S3 registry support
- [ ] Add Azure Blob Storage registry support
- [ ] Implement model versioning for local registry
- [ ] Add model metadata and tagging
- [ ] Create CLI interface
- [ ] Add more model format support (ONNX, CoreML)
- [ ] Implement model monitoring and drift detection
- [ ] Add model compression and optimization features

---

**Made with ❤️ by [Korhy](https://github.com/korhy)**
