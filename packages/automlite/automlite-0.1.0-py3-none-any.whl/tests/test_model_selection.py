import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
from sklearn.preprocessing import StandardScaler
from automl.model_selection import ModelSelector

@pytest.fixture
def classification_data():
    """Create sample preprocessed classification data."""
    X_num, y = make_classification(
        n_samples=100,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        n_classes=2,
        random_state=42
    )
    
    # Create DataFrame with numeric features (already preprocessed)
    X = pd.DataFrame(
        StandardScaler().fit_transform(X_num),  # Data is already scaled
        columns=[f'feature_{i}' for i in range(10)]
    )
    
    y = pd.Series(y, name='target')
    
    return X, X.copy(), y  # Both tree and linear versions are the same (preprocessed)

@pytest.fixture
def regression_data():
    """Create sample preprocessed regression data."""
    X_num, y = make_regression(
        n_samples=100,
        n_features=10,
        n_informative=5,
        noise=0.1,
        random_state=42
    )
    
    # Create DataFrame with numeric features (already preprocessed)
    X = pd.DataFrame(
        StandardScaler().fit_transform(X_num),  # Data is already scaled
        columns=[f'feature_{i}' for i in range(10)]
    )
    
    y = pd.Series(y, name='target')
    
    return X, X.copy(), y  # Both tree and linear versions are the same (preprocessed)

def test_init_valid():
    """Test initialization with valid parameters."""
    ms = ModelSelector(problem_type='classification', n_splits=5)
    assert ms.problem_type == 'classification'
    assert ms.n_splits == 5
    assert ms.fixed_model is None

def test_init_invalid_problem_type():
    """Test initialization with invalid problem type."""
    with pytest.raises(ValueError, match="problem_type must be either 'classification' or 'regression'"):
        ModelSelector(problem_type='invalid')

def test_get_model_list():
    """Test getting model lists for different data versions."""
    ms = ModelSelector(problem_type='classification')
    
    tree_models = ms._get_model_list('tree')
    assert all(model in ['RandomForest', 'XGBoost', 'LightGBM', 'CatBoost'] for model in tree_models)
    
    linear_models = ms._get_model_list('linear')
    assert all(model in ['LogisticRegression', 'SVM'] for model in linear_models)
    
    with pytest.raises(ValueError, match="data_version must be either 'tree' or 'linear'"):
        ms._get_model_list('invalid')

def test_classification_optimization(classification_data):
    """Test optimization for classification problem."""
    X_tree, X_linear, y = classification_data
    ms = ModelSelector(problem_type='classification', n_splits=3)
    
    # Run optimization with fewer trials for testing
    results = ms.optimize(X_tree, X_linear, y, n_trials=2)
    
    # Check results structure
    assert 'tree' in results
    assert 'linear' in results
    for version in ['tree', 'linear']:
        assert 'best_score' in results[version]
        assert 'best_params' in results[version]
        assert 'model_scores' in results[version]
    
    # Check best pipeline
    data_version, model, params = ms.get_best_pipeline()
    assert data_version in ['tree', 'linear']
    assert model is not None
    assert params is not None

def test_regression_optimization(regression_data):
    """Test optimization for regression problem."""
    X_tree, X_linear, y = regression_data
    ms = ModelSelector(problem_type='regression', n_splits=3)
    
    # Run optimization with fewer trials for testing
    results = ms.optimize(X_tree, X_linear, y, n_trials=2)
    
    # Check results structure
    assert 'tree' in results
    assert 'linear' in results
    for version in ['tree', 'linear']:
        assert 'best_score' in results[version]
        assert 'best_params' in results[version]
        assert 'model_scores' in results[version]
    
    # Check best pipeline
    data_version, model, params = ms.get_best_pipeline()
    assert data_version in ['tree', 'linear']
    assert model is not None
    assert params is not None

def test_fixed_model(classification_data):
    """Test optimization with a fixed model."""
    X_tree, X_linear, y = classification_data
    ms = ModelSelector(
        problem_type='classification',
        fixed_model='RandomForest',
        n_splits=3
    )
    
    results = ms.optimize(X_tree, X_linear, y, n_trials=2)
    
    # Check that only RandomForest was tried
    for version in ['tree', 'linear']:
        model_scores = results[version]['model_scores']
        assert len(model_scores) == 1
        assert 'RandomForest' in model_scores

def test_feature_importance(classification_data):
    """Test feature importance extraction."""
    X_tree, X_linear, y = classification_data
    ms = ModelSelector(
        problem_type='classification',
        fixed_model='RandomForest',  # Use RandomForest to ensure feature_importances_ is available
        n_splits=3
    )
    
    ms.optimize(X_tree, X_linear, y, n_trials=2)
    importance_df = ms.get_feature_importance()
    
    assert isinstance(importance_df, pd.DataFrame)
    assert 'Feature' in importance_df.columns
    assert 'Importance' in importance_df.columns
    assert len(importance_df) > 0

def test_get_best_pipeline_without_optimize():
    """Test getting best pipeline without running optimization."""
    ms = ModelSelector(problem_type='classification')
    with pytest.raises(RuntimeError, match=r"Call optimize\(\) before getting the best pipeline"):
        ms.get_best_pipeline()

def test_get_feature_importance_without_importance():
    """Test getting feature importance when not available."""
    ms = ModelSelector(problem_type='classification')
    with pytest.raises(RuntimeError, match="No feature importance available for the best model"):
        ms.get_feature_importance() 