import numpy as np
import pandas as pd
import pytest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from automl.feature_importance import FeatureImportance

@pytest.fixture
def classification_data():
    """Create classification test data."""
    n_samples = 100
    n_features = 10
    X = pd.DataFrame(
        np.random.random((n_samples, n_features)),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    y = np.random.randint(0, 2, n_samples)
    return X, y

@pytest.fixture
def regression_data():
    """Create regression test data."""
    n_samples = 100
    n_features = 10
    X = pd.DataFrame(
        np.random.random((n_samples, n_features)),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    y = np.random.random(n_samples)
    return X, y

def test_init_valid():
    """Test valid initialization of FeatureImportance."""
    clf = RandomForestClassifier()
    fi = FeatureImportance(clf, 'classification')
    assert fi.model == clf
    assert fi.problem_type == 'classification'

def test_init_invalid_problem_type():
    """Test initialization with invalid problem type."""
    clf = RandomForestClassifier()
    with pytest.raises(ValueError, match="Problem type must be either 'classification' or 'regression'"):
        FeatureImportance(clf, 'invalid_type')

def test_feature_importance_classification(classification_data):
    """Test feature importance computation for classification."""
    X, y = classification_data
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X, y)
    
    fi = FeatureImportance(clf, 'classification')
    importance = fi.compute_importance(X)
    
    assert isinstance(importance, pd.DataFrame)
    assert len(importance) == X.shape[1]
    assert 'importance_value' in importance.columns
    assert all(importance['importance_value'] >= 0)

def test_feature_importance_regression(regression_data):
    """Test feature importance computation for regression."""
    X, y = regression_data
    reg = RandomForestRegressor(random_state=42)
    reg.fit(X, y)
    
    fi = FeatureImportance(reg, 'regression')
    importance = fi.compute_importance(X)
    
    assert isinstance(importance, pd.DataFrame)
    assert len(importance) == X.shape[1]
    assert 'importance_value' in importance.columns
    assert all(importance['importance_value'] >= 0)

def test_plot_importance(classification_data):
    """Test plotting feature importance."""
    X, y = classification_data
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X, y)
    
    fi = FeatureImportance(clf, 'classification')
    importance = fi.compute_importance(X)
    
    fig = fi.plot_importance(top_n=5)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_importance_custom_params(classification_data):
    """Test plotting feature importance with custom parameters."""
    X, y = classification_data
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X, y)
    
    fi = FeatureImportance(clf, 'classification')
    importance = fi.compute_importance(X)
    
    fig = fi.plot_importance(
        top_n=3,
        figsize=(10, 6),
        title='Custom Title',
        xlabel='Custom X Label',
        ylabel='Custom Y Label'
    )
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_importance_without_compute(classification_data):
    """Test getting importance without computing first."""
    X, y = classification_data
    clf = RandomForestClassifier(random_state=42)
    fi = FeatureImportance(clf, 'classification')
    
    with pytest.raises(ValueError, match="Feature importance has not been computed yet"):
        fi.plot_importance()