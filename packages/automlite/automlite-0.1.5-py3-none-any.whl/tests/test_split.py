import pytest
import pandas as pd
import numpy as np
from automl.split import Split

@pytest.fixture
def classification_data():
    """Create a sample classification dataset"""
    np.random.seed(42)
    n_samples = 100
    data = {
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples),
        'target': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])  # Imbalanced classes
    }
    return pd.DataFrame(data)

@pytest.fixture
def regression_data():
    """Create a sample regression dataset"""
    np.random.seed(42)
    n_samples = 100
    data = {
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(0, 1, n_samples),
        'target': np.random.normal(0, 1, n_samples)
    }
    return pd.DataFrame(data)

@pytest.fixture
def time_series_data():
    """Create a sample time series dataset"""
    np.random.seed(42)
    n_samples = 100
    dates = pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
    data = {
        'timestamp': dates,
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.sin(np.linspace(0, 4*np.pi, n_samples)) + np.random.normal(0, 0.1, n_samples),
        'target': np.random.normal(0, 1, n_samples)
    }
    return pd.DataFrame(data)

def test_xy_split_classification(classification_data):
    """Test X/y split for classification data"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(classification_data, 'target')
    
    # Check shapes
    assert X.shape[0] == y.shape[0]
    assert X.shape[1] == 2  # Two features
    assert 'target' not in X.columns
    assert y.name == 'target'

def test_xy_split_invalid_target():
    """Test X/y split with invalid target column"""
    splitter = Split(random_state=42)
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    
    with pytest.raises(ValueError):
        X, y = splitter.X_y_split(df, 'nonexistent_target')

def test_train_val_split_classification(classification_data):
    """Test train/val split for classification data"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(classification_data, 'target')
    X_train, X_val, y_train, y_val = splitter.train_val_split(
        X, y, val_size=0.2, stratify=True, problem_type='classification'
    )
    
    # Check shapes
    assert len(X_train) == 80  # 80% of data
    assert len(X_val) == 20   # 20% of data
    assert len(y_train) == 80
    assert len(y_val) == 20
    
    # Check stratification
    train_class_ratio = y_train.mean()
    val_class_ratio = y_val.mean()
    assert abs(train_class_ratio - val_class_ratio) < 0.1  # Class ratios should be similar

def test_train_val_split_regression(regression_data):
    """Test train/val split for regression data"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(regression_data, 'target')
    X_train, X_val, y_train, y_val = splitter.train_val_split(
        X, y, val_size=0.2, stratify=False, problem_type='regression'
    )
    
    # Check shapes
    assert len(X_train) == 80
    assert len(X_val) == 20
    assert len(y_train) == 80
    assert len(y_val) == 20

def test_invalid_val_size():
    """Test train/val split with invalid validation size"""
    splitter = Split(random_state=42)
    df = pd.DataFrame({'A': [1, 2], 'target': [0, 1]})
    X, y = splitter.X_y_split(df, 'target')
    
    with pytest.raises(ValueError):
        splitter.train_val_split(X, y, val_size=1.5)

def test_create_folds_classification(classification_data):
    """Test fold creation for classification data"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(classification_data, 'target')
    X_folded, y_folded = splitter.create_folds(
        X, y, n_splits=5, stratify=True, problem_type='classification'
    )
    
    # Check fold column exists
    assert 'fold' in X_folded.columns
    
    # Check number of folds
    assert len(X_folded['fold'].unique()) == 5
    
    # Check stratification
    fold_class_ratios = []
    for fold in range(5):
        fold_mask = X_folded['fold'] == fold
        fold_ratio = y_folded[fold_mask].mean()
        fold_class_ratios.append(fold_ratio)
    
    # Check if class ratios are similar across folds
    max_ratio_diff = max(fold_class_ratios) - min(fold_class_ratios)
    assert max_ratio_diff < 0.15  # Allow some variation but not too much

def test_create_folds_regression(regression_data):
    """Test fold creation for regression data"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(regression_data, 'target')
    X_folded, y_folded = splitter.create_folds(
        X, y, n_splits=5, stratify=False, problem_type='regression'
    )
    
    # Check fold column exists
    assert 'fold' in X_folded.columns
    
    # Check number of folds
    assert len(X_folded['fold'].unique()) == 5
    
    # Check fold sizes are approximately equal
    fold_sizes = X_folded['fold'].value_counts()
    assert max(fold_sizes) - min(fold_sizes) <= 1  # Folds should be balanced

def test_time_split(time_series_data):
    """Test time-based train/validation split"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(time_series_data, 'target')
    
    # Test basic split
    X_train, X_val, y_train, y_val = splitter.time_split(
        X, y, time_column='timestamp', val_size=0.2
    )
    
    # Check shapes
    assert len(X_train) == 80  # 80% of data
    assert len(X_val) == 20   # 20% of data
    assert len(y_train) == 80
    assert len(y_val) == 20
    
    # Check temporal ordering
    assert X_train['timestamp'].max() < X_val['timestamp'].min()
    
    # Test with gap
    X_train_gap, X_val_gap, y_train_gap, y_val_gap = splitter.time_split(
        X, y, time_column='timestamp', val_size=0.2, gap=5
    )
    
    # Check gap
    last_train_time = X_train_gap['timestamp'].max()
    first_val_time = X_val_gap['timestamp'].min()
    gap_days = (first_val_time - last_train_time).days
    assert gap_days > 1  # Should have at least one day gap

def test_time_split_invalid_params(time_series_data):
    """Test time split with invalid parameters"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(time_series_data, 'target')
    
    # Test invalid time column
    with pytest.raises(ValueError):
        splitter.time_split(X, y, time_column='nonexistent')
    
    # Test invalid val_size
    with pytest.raises(ValueError):
        splitter.time_split(X, y, time_column='timestamp', val_size=1.5)
    
    # Test negative gap
    with pytest.raises(ValueError):
        splitter.time_split(X, y, time_column='timestamp', gap=-1)

def test_time_series_cv(time_series_data):
    """Test time series cross-validation"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(time_series_data, 'target')
    
    # Test basic CV
    splits = splitter.time_series_cv(
        X, y, time_column='timestamp', n_splits=3, min_train_size=0.5
    )
    
    # Check number of splits
    assert len(splits) == 3
    
    # Check each split
    for train_idx, test_idx in splits:
        # Check indices are valid
        assert all(idx < len(X) for idx in train_idx)
        assert all(idx < len(X) for idx in test_idx)
        
        # Check no overlap between train and test
        assert len(set(train_idx) & set(test_idx)) == 0
        
        # Check temporal ordering
        train_max_time = X.iloc[train_idx]['timestamp'].max()
        test_min_time = X.iloc[test_idx]['timestamp'].min()
        assert train_max_time < test_min_time

def test_time_series_cv_invalid_params(time_series_data):
    """Test time series CV with invalid parameters"""
    splitter = Split(random_state=42)
    X, y = splitter.X_y_split(time_series_data, 'target')
    
    # Test invalid time column
    with pytest.raises(ValueError):
        splitter.time_series_cv(X, y, time_column='nonexistent')
    
    # Test invalid min_train_size
    with pytest.raises(ValueError):
        splitter.time_series_cv(X, y, time_column='timestamp', min_train_size=1.5)
    
    # Test negative gap
    with pytest.raises(ValueError):
        splitter.time_series_cv(X, y, time_column='timestamp', gap=-1) 