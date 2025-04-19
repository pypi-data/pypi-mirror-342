import pytest
import pandas as pd
import numpy as np
from automl.encoder import InputEncoder, OutputEncoder, Encoder

@pytest.fixture
def sample_classification_data():
    """Create sample classification data with mixed types."""
    X = pd.DataFrame({
        'numeric': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'categorical': ['A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B'],
        'category_few': ['X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y']
    })
    y = pd.Series(['pos', 'neg', 'pos', 'neg', 'pos', 'neg', 'pos', 'neg', 'pos', 'neg'])
    return X, y

@pytest.fixture
def sample_regression_data():
    """Create sample regression data with mixed types."""
    X = pd.DataFrame({
        'numeric': [1.5, 2.5, 3.5, 4.5, 5.5],
        'categorical': ['A', 'B', 'C', 'A', 'B'],
        'category_few': ['X', 'Y', 'X', 'Y', 'X']
    })
    y = pd.Series([10.5, 20.5, 30.5, 40.5, 50.5])
    return X, y

@pytest.fixture
def sample_data():
    """Create sample data with different types of categorical features"""
    np.random.seed(42)
    n_samples = 100
    
    # Create DataFrame with:
    # - low cardinality categorical (3 categories)
    # - high cardinality categorical (15 categories)
    # - numeric feature
    data = {
        'low_card': np.random.choice(['A', 'B', 'C'], n_samples),
        'high_card': np.random.choice([f'cat_{i}' for i in range(15)], n_samples),
        'numeric': np.random.normal(0, 1, n_samples)
    }
    return pd.DataFrame(data)

class TestInputEncoder:
    def test_init(self):
        """Test InputEncoder initialization."""
        encoder = InputEncoder(n_splits=3, random_state=42)
        assert encoder.n_splits == 3
        assert encoder.random_state == 42
        assert not encoder.fitted
        assert encoder.target_features is None
        assert encoder.global_encoder is None

    def test_fit_transform_classification(self, sample_classification_data):
        """Test fit_transform with classification data."""
        X, y = sample_classification_data
        encoder = InputEncoder()
        X_encoded = encoder.fit_transform(X, y)
        
        # Check that numeric columns are unchanged
        pd.testing.assert_series_equal(X_encoded['numeric'], X['numeric'])
        
        # Check that categorical columns are encoded
        assert 'categorical' in encoder.target_features
        assert 'category_few' in encoder.target_features
        assert X_encoded['categorical'].dtype == float
        assert X_encoded['category_few'].dtype == float
        
        # Check that encoded values are within reasonable range
        assert X_encoded['categorical'].between(0, 1).all()
        assert X_encoded['category_few'].between(0, 1).all()

    def test_fit_transform_regression(self, sample_regression_data):
        """Test fit_transform with regression data."""
        X, y = sample_regression_data
        encoder = InputEncoder()
        X_encoded = encoder.fit_transform(X, y)
        
        # Check that numeric columns are unchanged
        pd.testing.assert_series_equal(X_encoded['numeric'], X['numeric'])
        
        # Check that categorical columns are encoded
        assert X_encoded['categorical'].dtype == float
        assert X_encoded['category_few'].dtype == float

    def test_transform_without_fit(self, sample_classification_data):
        """Test transform without fitting first."""
        X, _ = sample_classification_data
        encoder = InputEncoder()
        with pytest.raises(ValueError, match="must be fitted"):
            encoder.transform(X)

    def test_transform_missing_features(self, sample_classification_data):
        """Test transform with missing categorical features."""
        X, y = sample_classification_data
        encoder = InputEncoder()
        encoder.fit(X, y)
        
        # Remove a categorical column
        X_missing = X.drop('categorical', axis=1)
        with pytest.raises(ValueError, match="missing some categorical features"):
            encoder.transform(X_missing)

    def test_no_categorical_features(self):
        """Test with dataset containing no categorical features."""
        X = pd.DataFrame({
            'numeric1': [1, 2, 3],
            'numeric2': [4.0, 5.0, 6.0]
        })
        y = pd.Series([1, 0, 1])
        
        encoder = InputEncoder()
        X_encoded = encoder.fit_transform(X, y)
        
        # Should return unchanged DataFrame
        pd.testing.assert_frame_equal(X_encoded, X)
        assert not encoder.target_features

class TestOutputEncoder:
    def test_init(self):
        """Test OutputEncoder initialization."""
        encoder = OutputEncoder()
        assert not encoder.fitted
        assert encoder.encoding_map == {}

    def test_fit_transform_classification(self):
        """Test fit_transform with classification data."""
        y = pd.Series(['cat', 'dog', 'cat', 'bird', 'dog'])
        encoder = OutputEncoder()
        y_encoded = encoder.fit_transform(y)
        
        # Check that encoding is consistent
        assert len(encoder.encoding_map) == 3
        assert (y_encoded == encoder.transform(y)).all()
        
        # Check inverse transform
        y_original = encoder.inverse_transform(y_encoded)
        pd.testing.assert_series_equal(y_original, y)

    def test_fit_transform_regression(self):
        """Test fit_transform with regression data."""
        y = pd.Series([1.5, 2.5, 3.5, 4.5, 5.5])
        encoder = OutputEncoder()
        y_encoded = encoder.fit_transform(y)
        
        # Should return unchanged for numeric data
        pd.testing.assert_series_equal(y_encoded, y)
        assert not encoder.fitted

    def test_transform_without_fit(self):
        """Test transform without fitting first."""
        y = pd.Series(['A', 'B', 'C'])
        encoder = OutputEncoder()
        # Should return unchanged when not fitted
        pd.testing.assert_series_equal(encoder.transform(y), y)

    def test_inverse_transform_without_fit(self):
        """Test inverse_transform without fitting first."""
        y = pd.Series([0, 1, 2])
        encoder = OutputEncoder()
        with pytest.raises(ValueError, match="must be fitted"):
            encoder.inverse_transform(y)

    def test_encoding_map(self):
        """Test get_encoding_map functionality."""
        y = pd.Series(['cat', 'dog', 'bird'])
        encoder = OutputEncoder()
        encoder.fit(y)
        
        encoding_map = encoder.get_encoding_map()
        assert len(encoding_map) == 3
        assert set(encoding_map.keys()) == {'cat', 'dog', 'bird'}
        assert set(encoding_map.values()) == {0, 1, 2}

    def test_categorical_dtype(self):
        """Test with categorical dtype."""
        y = pd.Series(['A', 'B', 'A', 'C']).astype('category')
        encoder = OutputEncoder()
        y_encoded = encoder.fit_transform(y)
        
        assert encoder.fitted
        assert len(encoder.encoding_map) == 3
        assert y_encoded.dtype == np.int64

def test_initialization():
    """Test encoder initialization with different parameters"""
    # Test default initialization
    encoder = Encoder()
    assert encoder.strategy == 'auto'
    assert encoder.cardinality_threshold == 10
    
    # Test custom initialization
    encoder = Encoder(strategy='onehot', cardinality_threshold=15)
    assert encoder.strategy == 'onehot'
    assert encoder.cardinality_threshold == 15
    
    # Test invalid strategy
    with pytest.raises(ValueError):
        Encoder(strategy='invalid')

def test_fit_transform_auto(sample_data):
    """Test automatic encoding strategy"""
    encoder = Encoder(strategy='auto')
    
    # Test with tree-based model
    encoder.fit(sample_data, model_type='tree')
    transformed = encoder.transform(sample_data)
    
    # Check that low cardinality was one-hot encoded
    assert 'low_card_A' in transformed.columns
    assert 'low_card_B' in transformed.columns
    assert 'low_card_C' in transformed.columns
    
    # Check that high cardinality was label encoded
    assert 'high_card' in transformed.columns
    assert transformed['high_card'].dtype in [np.int32, np.int64]
    
    # Check numeric feature was preserved
    assert 'numeric' in transformed.columns
    assert transformed['numeric'].equals(sample_data['numeric'])

def test_fit_transform_onehot(sample_data):
    """Test forced one-hot encoding"""
    encoder = Encoder(strategy='onehot')
    encoder.fit(sample_data)
    transformed = encoder.transform(sample_data)
    
    # Check all categorical features were one-hot encoded
    assert 'low_card_A' in transformed.columns
    assert 'high_card_cat_0' in transformed.columns
    
    # Count total number of categorical columns
    n_cat_cols = sum(1 for col in transformed.columns if col.startswith(('low_card_', 'high_card_')))
    assert n_cat_cols == 18  # 3 for low_card + 15 for high_card

def test_fit_transform_label(sample_data):
    """Test forced label encoding"""
    encoder = Encoder(strategy='label')
    encoder.fit(sample_data)
    transformed = encoder.transform(sample_data)
    
    # Check all categorical features were label encoded
    assert 'low_card' in transformed.columns
    assert 'high_card' in transformed.columns
    assert transformed['low_card'].dtype in [np.int32, np.int64]
    assert transformed['high_card'].dtype in [np.int32, np.int64]

def test_handle_unseen_categories(sample_data):
    """Test handling of unseen categories"""
    encoder = Encoder(strategy='label')
    encoder.fit(sample_data)
    
    # Create new data with unseen categories
    new_data = sample_data.copy()
    new_data.loc[0, 'low_card'] = 'unseen_category'
    new_data.loc[1, 'high_card'] = 'unseen_category'
    
    transformed = encoder.transform(new_data)
    
    # Check that unseen categories were handled
    assert transformed['low_card'].notna().all()
    assert transformed['high_card'].notna().all()

def test_model_type_encoding(sample_data):
    """Test encoding strategy based on model type"""
    encoder = Encoder(strategy='auto')
    
    # Test with tree-based model
    encoder.fit(sample_data, model_type='tree')
    tree_transformed = encoder.transform(sample_data)
    
    # Test with linear model
    encoder = Encoder(strategy='auto')
    encoder.fit(sample_data, model_type='linear')
    linear_transformed = encoder.transform(sample_data)
    
    # Linear model should use one-hot encoding for all categorical features
    assert 'high_card' not in linear_transformed.columns
    assert any(col.startswith('high_card_') for col in linear_transformed.columns)

def test_no_categorical_features():
    """Test behavior with no categorical features"""
    # Create numeric-only data
    data = pd.DataFrame({
        'num1': np.random.normal(0, 1, 100),
        'num2': np.random.normal(0, 1, 100)
    })
    
    encoder = Encoder()
    encoder.fit(data)
    transformed = encoder.transform(data)
    
    # Check that data is unchanged
    assert transformed.equals(data)
    assert len(encoder.categorical_features) == 0

def test_feature_names_consistency(sample_data):
    """Test consistency of feature names between fit and transform"""
    encoder = Encoder(strategy='auto')
    encoder.fit(sample_data)
    
    # Get feature names after fit
    feature_names = encoder.encoded_features
    
    # Transform data
    transformed = encoder.transform(sample_data)
    
    # Check column order matches feature names
    assert list(transformed.columns) == feature_names 