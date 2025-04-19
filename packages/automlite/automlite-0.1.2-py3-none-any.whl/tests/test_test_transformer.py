import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from automl.test_transformer import TestTransformer

@pytest.fixture
def mock_components():
    """Create mock components for testing"""
    return {
        'preprocessor': Mock(),
        'input_encoder': Mock(),
        'output_encoder': Mock(),
        'scaler': Mock(),
        'feature_selector': Mock(),
        'dim_reducer': Mock()
    }

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    # Create sample training data
    X_train = pd.DataFrame({
        'num1': [1, 2, 3],
        'num2': [4, 5, 6],
        'cat1': ['A', 'B', 'C']
    })
    y_train = pd.Series([0, 1, 0], name='target')
    
    # Create sample validation data
    X_val = pd.DataFrame({
        'num1': [7, 8],
        'num2': [9, 10],
        'cat1': ['A', 'B']
    })
    y_val = pd.Series([1, 0], name='target')
    
    # Create sample test data
    X_test = pd.DataFrame({
        'num1': [11, 12],
        'num2': [13, 14],
        'cat1': ['B', 'C']
    })
    y_test = pd.Series([1, 0], name='target')
    
    return {
        'X_train': X_train,
        'y_train': y_train,
        'X_val': X_val,
        'y_val': y_val,
        'X_test': X_test,
        'y_test': y_test
    }

def test_init_valid(mock_components):
    """Test valid initialization"""
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='classification'
    )
    
    assert transformer.problem_type == 'classification'
    assert transformer.preprocessor == mock_components['preprocessor']
    assert transformer.input_encoder == mock_components['input_encoder']
    assert transformer.output_encoder == mock_components['output_encoder']
    assert transformer.scaler == mock_components['scaler']
    assert transformer.feature_selector == mock_components['feature_selector']
    assert transformer.dim_reducer == mock_components['dim_reducer']

def test_transform_classification(mock_components, sample_data):
    """Test transform method for classification problem"""
    # Setup mock returns
    mock_components['preprocessor'].fill_null.return_value = pd.concat(
        [sample_data['X_train'], sample_data['X_val'], sample_data['X_test']]
    )
    mock_components['input_encoder'].test_transform.return_value = sample_data['X_test']
    mock_components['scaler'].test_transform.return_value = sample_data['X_test']
    mock_components['feature_selector'].test_transform.return_value = sample_data['X_test']
    mock_components['dim_reducer'].test_transform.return_value = sample_data['X_test']
    mock_components['output_encoder'].test_transform.return_value = sample_data['y_test']
    
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='classification'
    )
    
    X_test_transformed, y_test_transformed = transformer.transform(
        sample_data['X_train'],
        sample_data['X_val'],
        sample_data['X_test'],
        sample_data['y_test']
    )
    
    # Verify all components were called
    mock_components['preprocessor'].fill_null.assert_called_once()
    mock_components['input_encoder'].test_transform.assert_called_once()
    mock_components['scaler'].test_transform.assert_called_once()
    mock_components['feature_selector'].test_transform.assert_called_once()
    mock_components['dim_reducer'].test_transform.assert_called_once()
    mock_components['output_encoder'].test_transform.assert_called_once()
    
    assert isinstance(X_test_transformed, pd.DataFrame)
    assert isinstance(y_test_transformed, pd.Series)

def test_transform_regression(mock_components, sample_data):
    """Test transform method for regression problem"""
    # Setup mock returns
    mock_components['preprocessor'].fill_null.return_value = pd.concat(
        [sample_data['X_train'], sample_data['X_val'], sample_data['X_test']]
    )
    mock_components['input_encoder'].test_transform.return_value = sample_data['X_test']
    mock_components['scaler'].test_transform.return_value = sample_data['X_test']
    mock_components['feature_selector'].test_transform.return_value = sample_data['X_test']
    mock_components['dim_reducer'].test_transform.return_value = sample_data['X_test']
    
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='regression'
    )
    
    X_test_transformed, y_test_transformed = transformer.transform(
        sample_data['X_train'],
        sample_data['X_val'],
        sample_data['X_test'],
        sample_data['y_test']
    )
    
    # Verify output encoder was not called for regression
    mock_components['output_encoder'].test_transform.assert_not_called()
    assert y_test_transformed is None

def test_transform_without_y_test(mock_components, sample_data):
    """Test transform method without test target"""
    # Setup mock returns
    mock_components['preprocessor'].fill_null.return_value = pd.concat(
        [sample_data['X_train'], sample_data['X_val'], sample_data['X_test']]
    )
    mock_components['input_encoder'].test_transform.return_value = sample_data['X_test']
    mock_components['scaler'].test_transform.return_value = sample_data['X_test']
    mock_components['feature_selector'].test_transform.return_value = sample_data['X_test']
    mock_components['dim_reducer'].test_transform.return_value = sample_data['X_test']
    
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='classification'
    )
    
    X_test_transformed, y_test_transformed = transformer.transform(
        sample_data['X_train'],
        sample_data['X_val'],
        sample_data['X_test']
    )
    
    assert y_test_transformed is None
    mock_components['output_encoder'].test_transform.assert_not_called()

def test_inverse_transform_target_classification(mock_components):
    """Test inverse_transform_target for classification"""
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='classification'
    )
    
    y_pred = np.array([0, 1, 0])
    mock_components['output_encoder'].inverse_transform.return_value = pd.Series(['A', 'B', 'A'])
    
    result = transformer.inverse_transform_target(y_pred)
    
    mock_components['output_encoder'].inverse_transform.assert_called_once_with(y_pred)
    assert isinstance(result, pd.Series)

def test_inverse_transform_target_regression(mock_components):
    """Test inverse_transform_target for regression"""
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='regression'
    )
    
    y_pred = np.array([1.5, 2.5, 3.5])
    result = transformer.inverse_transform_target(y_pred)
    
    mock_components['output_encoder'].inverse_transform.assert_not_called()
    assert isinstance(result, pd.Series)
    assert np.array_equal(result.values, y_pred)

def test_transform_invalid_input(mock_components):
    """Test transform method with invalid input types"""
    transformer = TestTransformer(
        preprocessor=mock_components['preprocessor'],
        input_encoder=mock_components['input_encoder'],
        output_encoder=mock_components['output_encoder'],
        scaler=mock_components['scaler'],
        feature_selector=mock_components['feature_selector'],
        dim_reducer=mock_components['dim_reducer'],
        problem_type='classification'
    )
    
    # Test with invalid X_test type
    with pytest.raises(TypeError, match="X_test must be a pandas DataFrame"):
        transformer.transform(
            pd.DataFrame({'a': [1]}),
            pd.DataFrame({'a': [1]}),
            np.array([1, 2, 3])
        )
    
    # Test with invalid y_test type
    with pytest.raises(TypeError, match="y_test must be a pandas Series"):
        transformer.transform(
            pd.DataFrame({'a': [1]}),
            pd.DataFrame({'a': [1]}),
            pd.DataFrame({'a': [1]}),
            np.array([1])
        ) 