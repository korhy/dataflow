from setuptools import setup, find_packages

setup(
    name="korhy-dataflow",
    version="0.1.0",
    description="Data flow processing package",
    author="Clement Boudinel",
    author_email="clementboudinel@gmail.com",
    packages=find_packages(),
    install_requires=[
        "mlflow==2.1.1",
        "numpy==1.23.5",
        "pandas==1.5.3",
        "scipy==1.10.0",
        "scikit-learn==1.3.1",
        "google-cloud-bigquery",
        "google-cloud-storage==2.14.0",
        "google-api-core==2.8.2",
        "googleapis-common-protos==1.56.4",
        "protobuf==3.19.6",
        "h5py==3.10.0",
        "db-dtypes",
        "pyarrow",
        "tensorflow-macos==2.10.0; sys_platform == 'darwin' and 'ARM' in platform_version",
        "tensorflow==2.10.0; sys_platform == 'darwin' and 'ARM' not in platform_version",
        "tensorflow==2.10.0; sys_platform != 'darwin'",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
)
