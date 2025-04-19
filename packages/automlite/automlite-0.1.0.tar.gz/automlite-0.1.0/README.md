# AutoML

A comprehensive Automated Machine Learning (AutoML) library that handles the entire machine learning pipeline from data preprocessing to model deployment.

## Features

### 1. Automated Data Processing
- Automatic data type detection
- Missing value handling
- Outlier detection and treatment
- Feature scaling and encoding
- Advanced feature engineering

### 2. Intelligent Model Selection
- Automatic problem type detection (classification/regression)
- Model recommendation based on dataset characteristics
- Hyperparameter optimization using Bayesian optimization
- Cross-validation with appropriate strategies

### 3. Advanced Capabilities
- Time series handling with automatic feature creation
- Imbalanced data handling
- Automated feature selection using multiple methods
- Comprehensive model evaluation

### 4. Production-Ready
- Model monitoring and drift detection
- REST API deployment support
- Comprehensive logging
- Error handling and recovery

## Installation

You can install the package directly from PyPI:

```bash
pip install automl
```

## Command-Line Usage

You can run the AutoML pipeline directly from the command line:

```bash
automlite --train path/to/train.csv --target target_column_name --test path/to/test.csv --output path/to/output.csv --columns column1 column2 column3
```

Replace `path/to/train.csv`, `target_column_name`, `path/to/test.csv`, and `path/to/output.csv` with the actual paths and names relevant to your data. Specify the columns you want to include in the output file using the `--columns` argument. If not specified, all columns will be included by default.

## Quick Start

```python
from automl import AutoMLPipeline

# Initialize pipeline
pipeline = AutoMLPipeline(config={
    'problem_type': 'auto',
    'preprocessing': {
        'missing_values': 'auto',
        'outliers': 'iqr',
        'scaling': 'standard'
    },
    'feature_engineering': {
        'polynomial_features': True,
        'interaction_features': True
    },
    'model_selection': {
        'optimization_metric': 'accuracy',
        'cv_folds': 5
    }
})

# Fit pipeline
pipeline.fit(X_train, y_train)

# Make predictions
predictions = pipeline.predict(X_test)

# Get model performance
metrics = pipeline.evaluate(X_test, y_test)

# Get pipeline information
info = pipeline.get_pipeline_info()
print(f"Best model: {info['best_model']}")
print(f"Best score: {info['best_score']:.4f}")
```

## Project Structure

```
AutoML/
├── automl/
│   ├── __init__.py
│   ├── main.py              # Main AutoML pipeline
│   ├── data_analysis.py     # Data analysis components
│   ├── preprocessing.py     # Data preprocessing
│   ├── feature_engineering.py # Feature engineering
│   ├── model_selection.py   # Model selection and tuning
│   ├── evaluation.py        # Model evaluation
│   ├── time_series.py       # Time series handling
│   └── utils.py            # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_data_analysis.py
│   ├── test_preprocessing.py
│   ├── test_feature_engineering.py
│   ├── test_model_selection.py
│   └── test_evaluation.py
├── examples/
│   ├── classification_example.py
│   ├── regression_example.py
│   └── time_series_example.py
├── requirements.txt
├── setup.py
└── README.md
```

## Advanced Usage

### Time Series Analysis

```python
from automl import AutoMLPipeline

# Configure for time series
pipeline = AutoMLPipeline(config={
    'problem_type': 'time_series',
    'time_series': {
        'date_column': 'date',
        'lag_features': True,
        'rolling_features': True,
        'seasonal_features': True
    }
})

pipeline.fit(X_train, y_train)
```

### Handling Imbalanced Data

```python
pipeline = AutoMLPipeline(config={
    'problem_type': 'classification',
    'preprocessing': {
        'handle_imbalance': True,
        'imbalance_strategy': 'auto'  # Automatically choose best strategy
    }
})
```

### Custom Feature Engineering

```python
pipeline = AutoMLPipeline(config={
    'feature_engineering': {
        'polynomial_features': True,
        'interaction_features': True,
        'custom_features': [
            lambda df: df['A'] + df['B'],
            lambda df: df['C'] * df['D']
        ]
    }
})
```

## API Deployment

```python
from automl.deployment import create_api
from automl import AutoMLPipeline

# Train your model
pipeline = AutoMLPipeline()
pipeline.fit(X_train, y_train)

# Create API
app = create_api(pipeline)

# Run API
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by various AutoML frameworks and best practices in the ML community
- Built with modern Python libraries and tools
- Designed for both beginners and advanced users
