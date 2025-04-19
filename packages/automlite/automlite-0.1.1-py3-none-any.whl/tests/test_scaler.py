import pytest
import numpy as np
import pandas as pd
from scipy import stats
from automl.scaler import AutoScaler

@pytest.fixture
def sample_data():
    """Create sample data with different distributions."""
    np.random.seed(42)
    n_samples = 100
    
    return pd.DataFrame({
        'normal': np.random.normal(loc=0, scale=1, size=n_samples),
        'uniform': np.random.uniform(low=-10, high=10, size=n_samples),
        'skewed': np.exp(np.random.normal(loc=0, scale=1, size=n_samples))
    })

def test_init_valid():
    """Test valid initialization."""
    scaler = AutoScaler(force_method='minmax')
    assert scaler.force_method == 'minmax'
    assert not scaler.fitted

def test_init_invalid():
    """Test invalid initialization."""
    with pytest.raises(ValueError, match="force_method must be one of"):
        AutoScaler(force_method='invalid')

def test_input_validation():
    """Test input validation."""
    scaler = AutoScaler()
    
    # Test non-DataFrame input
    with pytest.raises(TypeError, match="must be a pandas DataFrame"):
        scaler.fit(np.array([[1, 2], [3, 4]]))
    
    # Test non-numeric data
    data = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
    with pytest.raises(ValueError, match="must be numeric"):
        scaler.fit(data)
    
    # Test missing values
    data = pd.DataFrame({'a': [1, np.nan]})
    with pytest.raises(ValueError, match="contains missing values"):
        scaler.fit(data)

def test_scaler_selection(sample_data):
    """Test automatic scaler selection."""
    scaler = AutoScaler()
    scaler.fit(sample_data)
    methods = scaler.get_feature_scalers()
    
    # Normal data should use standard scaling
    assert methods['normal'] == 'standard'
    # Uniform data should use minmax scaling
    assert methods['uniform'] == 'minmax'
    # Skewed data should use robust scaling
    assert methods['skewed'] == 'robust'

def test_force_method(sample_data):
    """Test forcing a specific scaling method."""
    scaler = AutoScaler(force_method='minmax')
    scaler.fit(sample_data)
    methods = scaler.get_feature_scalers()
    
    assert all(method == 'minmax' for method in methods.values())

def test_transform_shape(sample_data):
    """Test that transform preserves shape and columns."""
    scaler = AutoScaler()
    transformed = scaler.fit_transform(sample_data)
    
    assert transformed.shape == sample_data.shape
    assert all(transformed.columns == sample_data.columns)

def test_scaling_ranges(sample_data):
    """Test that scaled values are in reasonable ranges."""
    scaler = AutoScaler()
    transformed = scaler.fit_transform(sample_data)
    
    # Most values should be within [-3, 3] for standard scaling
    assert (transformed['normal'].abs() <= 3).mean() >= 0.99
    
    # MinMax scaled values should be within [0, 1]
    scaler = AutoScaler(force_method='minmax')
    transformed = scaler.fit_transform(sample_data)
    assert transformed.min().min() >= -0.001  # Allow for minor numerical errors
    assert transformed.max().max() <= 1.001

def test_inverse_transform(sample_data):
    """Test that inverse transform recovers original data."""
    scaler = AutoScaler()
    transformed = scaler.fit_transform(sample_data)
    recovered = scaler.inverse_transform(transformed)
    
    # Check if recovered data is close to original
    np.testing.assert_array_almost_equal(
        recovered.values,
        sample_data.values,
        decimal=10  # High precision since we're not clipping
    )

def test_partial_transform():
    """Test transforming subset of original features."""
    train_data = pd.DataFrame({
        'a': np.random.normal(size=100),
        'b': np.random.normal(size=100)
    })
    
    scaler = AutoScaler()
    scaler.fit(train_data)
    
    # Transform only one column
    test_data = pd.DataFrame({'a': np.random.normal(size=50)})
    transformed = scaler.transform(test_data)
    
    assert 'a' in transformed.columns
    assert 'b' not in transformed.columns
    assert len(transformed) == 50

def test_fit_transform_equivalence(sample_data):
    """Test that fit_transform is equivalent to fit().transform()."""
    scaler1 = AutoScaler()
    scaler2 = AutoScaler()
    
    # Using fit().transform()
    result1 = scaler1.fit(sample_data).transform(sample_data)
    
    # Using fit_transform()
    result2 = scaler2.fit_transform(sample_data)
    
    np.testing.assert_array_equal(result1.values, result2.values)

def test_unfit_operations(sample_data):
    """Test operations before fitting."""
    scaler = AutoScaler()
    
    with pytest.raises(ValueError, match="must be fitted"):
        scaler.transform(sample_data)
        
    with pytest.raises(ValueError, match="must be fitted"):
        scaler.inverse_transform(sample_data)
        
    with pytest.raises(ValueError, match="must be fitted"):
        scaler.get_feature_scalers() 