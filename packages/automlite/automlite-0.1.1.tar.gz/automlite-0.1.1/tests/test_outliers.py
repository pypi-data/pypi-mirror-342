import pytest
import numpy as np
import pandas as pd
from automl.outliers import OutlierHandler

@pytest.fixture
def sample_data():
    """Create sample data with known outliers."""
    np.random.seed(42)
    
    # Create normal data
    X_train = pd.DataFrame({
        'normal': np.random.normal(0, 1, 100),
        'skewed': np.random.exponential(2, 100),
        'id': range(100),
        'constant': np.ones(100)
    })
    
    # Add outliers
    X_train.loc[0, 'normal'] = 10  # Extreme outlier
    X_train.loc[1, 'normal'] = -8  # Extreme outlier
    X_train.loc[2, 'skewed'] = 20  # Extreme outlier
    
    X_val = pd.DataFrame({
        'normal': np.random.normal(0, 1, 20),
        'skewed': np.random.exponential(2, 20),
        'id': range(100, 120),
        'constant': np.ones(20)
    })
    
    # Add outlier to validation
    X_val.loc[0, 'normal'] = 12  # Extreme outlier
    
    y_train = pd.Series(np.random.randint(0, 2, 100))
    y_val = pd.Series(np.random.randint(0, 2, 20))
    
    return X_train, X_val, y_train, y_val

def test_initialization(sample_data):
    """Test OutlierHandler initialization."""
    X_train, X_val, y_train, y_val = sample_data
    
    # Test valid initialization
    handler = OutlierHandler(X_train, X_val, y_train, y_val)
    assert handler.problem_type == "classification"
    assert handler.sensitivity == 20.0
    assert handler.vote_threshold == 2
    
    # Test without validation data
    handler = OutlierHandler(X_train)
    assert handler.X_val is None
    assert handler.y_val is None
    
    # Test invalid problem type
    with pytest.raises(ValueError):
        OutlierHandler(X_train, problem_type="invalid")
    
    # Test invalid sensitivity
    with pytest.raises(ValueError):
        OutlierHandler(X_train, sensitivity=0)
    with pytest.raises(ValueError):
        OutlierHandler(X_train, sensitivity=101)

def test_sensitivity_params():
    """Test sensitivity parameter effects."""
    X = pd.DataFrame({'feature': np.random.normal(0, 1, 100)})
    
    # Low sensitivity
    handler_low = OutlierHandler(X, sensitivity=1.0)
    z1, iqr1, cont1 = handler_low._get_sensitivity_params()
    
    # High sensitivity
    handler_high = OutlierHandler(X, sensitivity=100.0)
    z2, iqr2, cont2 = handler_high._get_sensitivity_params()
    
    # Higher sensitivity should result in:
    # 1. Lower z-score threshold (more aggressive)
    assert z2 < z1
    # 2. Higher IQR multiplier (more aggressive)
    assert iqr2 > iqr1
    # 3. Higher contamination rate (more aggressive)
    assert cont2 > cont1

def test_outlier_detection_methods(sample_data):
    """Test individual outlier detection methods."""
    X_train, _, _, _ = sample_data
    handler = OutlierHandler(X_train)
    
    series = X_train['normal']
    z_threshold, iqr_multiplier, contamination = handler._get_sensitivity_params()
    
    # Test Z-score detection
    z_outliers = handler._detect_zscore_outliers(series, z_threshold)
    assert len(z_outliers) > 0
    assert 0 in z_outliers  # Known outlier
    assert 1 in z_outliers  # Known outlier
    
    # Test IQR detection
    iqr_outliers = handler._detect_iqr_outliers(series, iqr_multiplier)
    assert len(iqr_outliers) > 0
    assert 0 in iqr_outliers  # Known outlier
    assert 1 in iqr_outliers  # Known outlier
    
    # Test constant series
    constant_series = pd.Series(np.ones(100))
    assert len(handler._detect_zscore_outliers(constant_series, z_threshold)) == 0
    assert len(handler._detect_iqr_outliers(constant_series, iqr_multiplier)) == 0

def test_detect_outliers(sample_data):
    """Test the main outlier detection pipeline."""
    X_train, X_val, y_train, y_val = sample_data
    handler = OutlierHandler(X_train, X_val, y_train, y_val)
    
    outlier_indexes = handler.detect_outliers()
    
    # Check structure
    assert "X_train" in outlier_indexes
    assert "X_val" in outlier_indexes
    
    # Check known outliers are detected
    train_outliers = outlier_indexes["X_train"]
    assert 0 in train_outliers  # Known outlier in normal
    assert 1 in train_outliers  # Known outlier in normal
    assert 2 in train_outliers  # Known outlier in skewed
    
    # Check features marked as outliers
    assert "normal" in train_outliers[0]
    assert "normal" in train_outliers[1]
    assert "skewed" in train_outliers[2]
    
    # Verify ID column is not checked for outliers
    for outliers in train_outliers.values():
        assert "id" not in outliers
        assert "constant" not in outliers

def test_handle_outliers_clip(sample_data):
    """Test outlier handling with clipping strategy."""
    X_train, X_val, y_train, y_val = sample_data
    handler = OutlierHandler(X_train, X_val, y_train, y_val)
    
    # Detect and handle outliers
    handler.detect_outliers()
    X_train_new, X_val_new, y_train_new, y_val_new = handler.handle_outliers(strategy="clip")
    
    # Check shapes are preserved
    assert X_train_new.shape == X_train.shape
    assert X_val_new.shape == X_val.shape
    
    # Check outliers were clipped
    assert abs(X_train_new.loc[0, 'normal']) < abs(X_train.loc[0, 'normal'])
    assert abs(X_train_new.loc[1, 'normal']) < abs(X_train.loc[1, 'normal'])
    assert X_train_new.loc[2, 'skewed'] < X_train.loc[2, 'skewed']
    
    # Check non-outliers weren't modified
    normal_idx = list(set(range(3, 100)))
    pd.testing.assert_series_equal(
        X_train.loc[normal_idx, 'normal'],
        X_train_new.loc[normal_idx, 'normal']
    )

def test_handle_outliers_remove(sample_data):
    """Test outlier handling with removal strategy."""
    X_train, X_val, y_train, y_val = sample_data
    handler = OutlierHandler(X_train, X_val, y_train, y_val)
    
    # Detect and handle outliers
    handler.detect_outliers()
    X_train_new, X_val_new, y_train_new, y_val_new = handler.handle_outliers(strategy="remove")
    
    # Check outliers were removed
    assert X_train_new.shape[0] < X_train.shape[0]
    assert 0 not in X_train_new.index  # Known outlier
    assert 1 not in X_train_new.index  # Known outlier
    assert 2 not in X_train_new.index  # Known outlier
    
    # Check y was also adjusted
    assert len(y_train_new) == len(X_train_new)
    
    # Test with keep_indices
    X_train_kept, _, _, _ = handler.handle_outliers(
        strategy="remove",
        keep_indices=[0, 1]  # Keep these outliers
    )
    assert 0 in X_train_kept.index
    assert 1 in X_train_kept.index
    assert 2 not in X_train_kept.index

def test_regression_problem(sample_data):
    """Test outlier handling in regression problems."""
    X_train, X_val, _, _ = sample_data
    # Create continuous target
    y_train = pd.Series(np.random.normal(0, 1, len(X_train)))
    y_val = pd.Series(np.random.normal(0, 1, len(X_val)))
    
    handler = OutlierHandler(
        X_train, X_val, y_train, y_val,
        problem_type="regression"
    )
    
    # Regression should use lower vote threshold
    assert handler.vote_threshold == 1
    
    # Detect and handle outliers
    handler.detect_outliers()
    X_train_new, X_val_new, y_train_new, y_val_new = handler.handle_outliers()
    
    # Should detect more outliers due to lower threshold
    assert len(handler.outlier_indexes["X_train"]) > 0 