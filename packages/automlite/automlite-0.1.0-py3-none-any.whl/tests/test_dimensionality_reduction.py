import pytest
import numpy as np
import pandas as pd
from automl.dimensionality_reduction import DimensionalityReducer

@pytest.fixture
def sample_classification_data():
    """Create sample classification data."""
    np.random.seed(42)
    n_samples = 100
    n_features = 10
    
    # Generate random features
    X = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    
    # Generate binary target
    y = pd.Series(np.random.randint(0, 2, n_samples), name='target')
    
    return X, y

@pytest.fixture
def sample_regression_data():
    """Create sample regression data."""
    np.random.seed(42)
    n_samples = 100
    n_features = 10
    
    # Generate random features
    X = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    
    # Generate continuous target
    y = pd.Series(np.random.randn(n_samples), name='target')
    
    return X, y

def test_init_valid_params():
    """Test initialization with valid parameters."""
    dr = DimensionalityReducer(task_type='classification', variance_threshold=0.95)
    assert dr.task_type == 'classification'
    assert dr.variance_threshold == 0.95
    assert dr.force_method is None

def test_init_invalid_task_type():
    """Test initialization with invalid task type."""
    with pytest.raises(ValueError, match="task_type must be either 'classification' or 'regression'"):
        DimensionalityReducer(task_type='invalid')

def test_init_invalid_variance_threshold():
    """Test initialization with invalid variance threshold."""
    with pytest.raises(ValueError, match="variance_threshold must be between 0 and 1"):
        DimensionalityReducer(variance_threshold=1.5)

def test_init_invalid_force_method():
    """Test initialization with invalid force method."""
    with pytest.raises(ValueError, match="force_method must be either 'pca', 'lda', or None"):
        DimensionalityReducer(force_method='invalid')

def test_validate_data_not_dataframe(sample_classification_data):
    """Test validation with non-DataFrame input."""
    _, y = sample_classification_data
    dr = DimensionalityReducer()
    
    with pytest.raises(TypeError, match="X must be a pandas DataFrame"):
        dr._validate_data(np.array([[1, 2], [3, 4]]), y)

def test_validate_data_missing_values(sample_classification_data):
    """Test validation with missing values."""
    X, y = sample_classification_data
    X.iloc[0, 0] = np.nan
    dr = DimensionalityReducer()
    
    with pytest.raises(ValueError, match="X contains missing values"):
        dr._validate_data(X, y)

def test_validate_data_infinite_values(sample_classification_data):
    """Test validation with infinite values."""
    X, y = sample_classification_data
    X.iloc[0, 0] = np.inf
    dr = DimensionalityReducer()
    
    with pytest.raises(ValueError, match="X contains infinite values"):
        dr._validate_data(X, y)

def test_pca_regression(sample_regression_data):
    """Test PCA on regression data."""
    X, y = sample_regression_data
    dr = DimensionalityReducer(task_type='regression')
    X_transformed = dr.fit_transform(X, y)
    
    # Check output shape and type
    assert isinstance(X_transformed, pd.DataFrame)
    assert X_transformed.shape[0] == X.shape[0]
    assert X_transformed.shape[1] <= X.shape[1]
    
    # Check feature importance
    assert not dr.feature_importance_.empty
    assert '% Variance Explained' in dr.feature_importance_.columns
    assert 'Feature' in dr.feature_importance_.columns

def test_lda_classification(sample_classification_data):
    """Test LDA on classification data."""
    X, y = sample_classification_data
    dr = DimensionalityReducer(task_type='classification', force_method='lda')
    X_transformed = dr.fit_transform(X, y)
    
    # Check output shape and type
    assert isinstance(X_transformed, pd.DataFrame)
    assert X_transformed.shape[0] == X.shape[0]
    assert X_transformed.shape[1] == 1  # Binary classification = 1 component
    
    # Check feature importance
    assert not dr.feature_importance_.empty
    assert 'Discrimination Power' in dr.feature_importance_.columns
    assert 'Feature' in dr.feature_importance_.columns

def test_pca_variance_threshold(sample_regression_data):
    """Test PCA with different variance thresholds."""
    X, y = sample_regression_data
    
    # Test with high variance threshold
    dr_high = DimensionalityReducer(task_type='regression', variance_threshold=0.99)
    X_high = dr_high.fit_transform(X, y)
    
    # Test with low variance threshold
    dr_low = DimensionalityReducer(task_type='regression', variance_threshold=0.5)
    X_low = dr_low.fit_transform(X, y)
    
    # Higher threshold should keep more components
    assert X_high.shape[1] >= X_low.shape[1]

def test_transform_without_fit(sample_regression_data):
    """Test transform without fitting first."""
    X, _ = sample_regression_data
    dr = DimensionalityReducer()
    
    with pytest.raises(RuntimeError, match="Call fit before transform"):
        dr.transform(X)

def test_transform_wrong_features(sample_regression_data):
    """Test transform with wrong number of features."""
    X, y = sample_regression_data
    dr = DimensionalityReducer(task_type='regression')
    dr.fit(X, y)
    
    # Create new data with wrong number of features
    X_wrong = pd.DataFrame(np.random.randn(10, X.shape[1] + 1))
    
    with pytest.raises(ValueError, match="X has .* features, but DimensionalityReducer was trained with .*"):
        dr.transform(X_wrong)

def test_automatic_method_selection(sample_classification_data):
    """Test automatic method selection."""
    X, y = sample_classification_data
    dr = DimensionalityReducer(task_type='classification')
    
    # Should choose LDA for classification with enough features
    method = dr._choose_method(X, y)
    assert method == 'lda'
    
    # Should fall back to PCA for regression
    dr.task_type = 'regression'
    method = dr._choose_method(X, y)
    assert method == 'pca'

def test_lda_fallback_to_pca(sample_classification_data):
    """Test LDA fallback to PCA when matrices are singular."""
    X, y = sample_classification_data
    
    # Create perfect correlation between features to force singular matrix
    X['feature_1'] = X['feature_0']
    
    dr = DimensionalityReducer(task_type='classification', force_method='lda')
    with pytest.warns(UserWarning, match="LDA failed due to singular matrices"):
        X_transformed = dr.fit_transform(X, y)
    
    assert isinstance(X_transformed, pd.DataFrame)
    assert X_transformed.shape[0] == X.shape[0]

def test_feature_names_in_transform(sample_regression_data):
    """Test feature names in transformed data."""
    X, y = sample_regression_data
    dr = DimensionalityReducer(task_type='regression')
    X_transformed = dr.fit_transform(X, y)
    
    # Check that feature names are properly formatted
    expected_names = [f'Component_{i+1}' for i in range(X_transformed.shape[1])]
    assert list(X_transformed.columns) == expected_names 