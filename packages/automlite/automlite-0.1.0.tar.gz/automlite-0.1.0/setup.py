from setuptools import setup, find_packages

setup(
    name="automlite",
    version="0.1.0",
    description="An automated machine learning pipeline for classification and regression tasks",
    author="Manan Verma",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "lightgbm>=3.3.0",
        "xgboost>=1.5.0",
        "catboost>=1.0.0",
        "optuna>=2.10.0",
        "shap>=0.40.0",
        "joblib>=1.1.0",
        "tqdm>=4.62.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.12b0",
            "flake8>=4.0.0",
            "mypy>=0.910"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        'console_scripts': [
            'automl=automl.cli:main',
        ],
    },
) 