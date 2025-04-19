import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock
from automl.evaluator import Evaluator

@pytest.fixture
def mock_classification_model():
    """Create mock classification model"""
    model = Mock()
    model.predict_proba.return_value = np.array([
        [0.8, 0.2],
        [0.3, 0.7],
        [0.9, 0.1]
    ])
    return model

@pytest.fixture
def mock_regression_model():
    """Create mock regression model"""
    model = Mock()
    model.predict.return_value = np.array([1.5, 2.5, 3.5])
    return model

@pytest.fixture
def mock_test_transformer():
    """Create mock test transformer"""
    transformer = Mock()
    transformer.transform.return_value = (
        pd.DataFrame(np.random.rand(3, 2)),  # X_test_transformed
        pd.Series([0, 1, 0])  # y_test_transformed
    )
    transformer.inverse_transform_target.return_value = pd.Series([0, 1, 0])
    return transformer

def test_init_valid():
    """Test valid initialization"""
    evaluator = Evaluator('classification', Mock())
    assert evaluator.problem_type == 'classification'
    assert evaluator.metrics == {}

def test_init_invalid_problem_type():
    """Test initialization with invalid problem type"""
    with pytest.raises(ValueError):
        Evaluator('invalid_type', Mock())

def test_evaluate_classification(mock_classification_model, mock_test_transformer):
    """Test classification evaluation"""
    evaluator = Evaluator('classification', mock_test_transformer)
    
    metrics = evaluator.evaluate(
        mock_classification_model,
        pd.DataFrame({'a': [1, 2, 3]}),  # X_train
        pd.DataFrame({'a': [4, 5, 6]}),  # X_val
        pd.DataFrame({'a': [7, 8, 9]}),  # X_test
        pd.Series([0, 1, 0])  # y_test
    )
    
    assert isinstance(metrics, dict)
    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'f1' in metrics
    assert 'roc_auc' in metrics
    assert 'log_loss' in metrics
    assert 'confusion_matrix' in metrics
    assert 'predictions' in metrics

def test_evaluate_regression(mock_regression_model, mock_test_transformer):
    """Test regression evaluation"""
    evaluator = Evaluator('regression', mock_test_transformer)
    
    metrics = evaluator.evaluate(
        mock_regression_model,
        pd.DataFrame({'a': [1, 2, 3]}),  # X_train
        pd.DataFrame({'a': [4, 5, 6]}),  # X_val
        pd.DataFrame({'a': [7, 8, 9]}),  # X_test
        pd.Series([1.0, 2.0, 3.0])  # y_test
    )
    
    assert isinstance(metrics, dict)
    assert 'mse' in metrics
    assert 'rmse' in metrics
    assert 'mae' in metrics
    assert 'r2' in metrics
    assert 'explained_variance' in metrics
    assert 'predictions' in metrics

def test_get_metrics_without_evaluation():
    """Test getting metrics without running evaluation"""
    evaluator = Evaluator('classification', Mock())
    with pytest.raises(ValueError):
        evaluator.get_metrics()

def test_print_report_classification(mock_classification_model, mock_test_transformer, capsys):
    """Test printing classification report"""
    evaluator = Evaluator('classification', mock_test_transformer)
    evaluator.evaluate(
        mock_classification_model,
        pd.DataFrame({'a': [1, 2, 3]}),
        pd.DataFrame({'a': [4, 5, 6]}),
        pd.DataFrame({'a': [7, 8, 9]}),
        pd.Series([0, 1, 0])
    )
    
    evaluator.print_report()
    captured = capsys.readouterr()
    assert "Classification Metrics:" in captured.out
    assert "Accuracy:" in captured.out
    assert "Confusion Matrix:" in captured.out

def test_print_report_regression(mock_regression_model, mock_test_transformer, capsys):
    """Test printing regression report"""
    evaluator = Evaluator('regression', mock_test_transformer)
    evaluator.evaluate(
        mock_regression_model,
        pd.DataFrame({'a': [1, 2, 3]}),
        pd.DataFrame({'a': [4, 5, 6]}),
        pd.DataFrame({'a': [7, 8, 9]}),
        pd.Series([1.0, 2.0, 3.0])
    )
    
    evaluator.print_report()
    captured = capsys.readouterr()
    assert "Regression Metrics:" in captured.out
    assert "MSE:" in captured.out
    assert "R² Score:" in captured.out

def test_print_report_without_metrics(capsys):
    """Test printing report without metrics"""
    evaluator = Evaluator('classification', Mock())
    evaluator.print_report()
    captured = capsys.readouterr()
    assert captured.out == ""  # Should print nothing 