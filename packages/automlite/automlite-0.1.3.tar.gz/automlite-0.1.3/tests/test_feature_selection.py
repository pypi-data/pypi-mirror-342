import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
from automl.feature_selection import FeatureSelector

@pytest.fixture
def classification_data():
    """Create a sample classification dataset with known properties."""
    X, y = make_classification(
        n_samples=100,
        n_features=20,
        n_informative=10,
        n_redundant=5,
        random_state=42
    )
    # Add some constant and highly correlated features
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
    X['constant'] = 1.0
    X['corr_1'] = X['feature_0'] * 0.95 + np.random.normal(0, 0.01, 100)
    X['corr_2'] = X['feature_1'] * 0.98 + np.random.normal(0, 0.01, 100)
    return X, y

@pytest.fixture
def regression_data():
    """Create a sample regression dataset with known properties."""
    X, y = make_regression(
        n_samples=100,
        n_features=20,
        n_informative=10,
        random_state=42
    )
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
    X['constant'] = 0.0
    X['corr_1'] = X['feature_0'] * 0.95 + np.random.normal(0, 0.01, 100)
    return X, y

def test_init():
    """Test initialization with different parameters."""
    fs = FeatureSelector('classification')
    assert fs.problem_type == 'classification'
    assert fs.n_features == 0.5
    
    fs = FeatureSelector('regression', n_features=10)
    assert fs.problem_type == 'regression'
    assert fs.n_features == 10

def test_invalid_init():
    """Test initialization with invalid parameters."""
    with pytest.raises(ValueError):
        FeatureSelector('invalid_type')
    
    with pytest.raises(ValueError):
        FeatureSelector('classification', n_features=0)
    
    with pytest.raises(ValueError):
        FeatureSelector('classification', n_features=1.5)

def test_low_variance_removal(classification_data):
    """Test removal of low variance features."""
    X, y = classification_data
    fs = FeatureSelector('classification')
    fs.fit(X, y)
    
    # Constant feature should be removed
    assert 'constant' not in fs.selected_features_

def test_correlation_removal(classification_data):
    """Test removal of highly correlated features."""
    X, y = classification_data
    fs = FeatureSelector('classification')
    fs.fit(X, y)
    
    # Only one of the correlated features should remain
    assert not ('corr_1' in fs.selected_features_ and 'feature_0' in fs.selected_features_)
    assert not ('corr_2' in fs.selected_features_ and 'feature_1' in fs.selected_features_)

def test_feature_importance(classification_data):
    """Test feature importance calculation and selection."""
    X, y = classification_data
    fs = FeatureSelector('classification', n_features=10)
    fs.fit(X, y)
    
    # Check if we get exactly 10 features
    assert len(fs.selected_features_) == 10
    
    # Check if importance scores are normalized
    importances = fs.get_feature_importances()
    assert all(0 <= score <= 1 for score in importances)

def test_regression_mode(regression_data):
    """Test feature selection in regression mode."""
    X, y = regression_data
    fs = FeatureSelector('regression')
    fs.fit(X, y)
    
    # Check if constant feature is removed
    assert 'constant' not in fs.selected_features_
    
    # Check if we get the expected number of features
    assert len(fs.selected_features_) <= int(0.5 * X.shape[1])

def test_transform(classification_data):
    """Test transform functionality."""
    X, y = classification_data
    fs = FeatureSelector('classification')
    X_transformed = fs.fit_transform(X, y)
    
    # Check if output is DataFrame
    assert isinstance(X_transformed, pd.DataFrame)
    
    # Check if columns match selected features
    assert list(X_transformed.columns) == fs.selected_features_
    
    # Test transform with missing features
    X_missing = X.drop(columns=[fs.selected_features_[0]])
    with pytest.raises(ValueError):
        fs.transform(X_missing)

def test_input_validation():
    """Test input validation."""
    fs = FeatureSelector('classification')
    
    # Test non-DataFrame input
    with pytest.raises(TypeError):
        fs.fit(np.array([[1, 2], [3, 4]]), [0, 1])
    
    # Test empty DataFrame
    with pytest.raises(ValueError):
        fs.fit(pd.DataFrame(), [])

def test_feature_names():
    """Test feature names tracking."""
    X = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'c': [7, 8, 9]
    })
    y = [0, 1, 0]
    
    fs = FeatureSelector('classification')
    fs.fit(X, y)
    
    assert isinstance(fs.feature_names_in_, np.ndarray)
    assert all(name in ['a', 'b', 'c'] for name in fs.feature_names_in_)

def test_get_feature_importances(classification_data):
    """Test get_feature_importances method."""
    X, y = classification_data
    fs = FeatureSelector('classification')
    fs.fit(X, y)
    
    importances = fs.get_feature_importances()
    assert isinstance(importances, pd.Series)
    assert len(importances) == len(fs.selected_features_)
    assert all(importance >= 0 for importance in importances)
    assert all(importance <= 1 for importance in importances) 