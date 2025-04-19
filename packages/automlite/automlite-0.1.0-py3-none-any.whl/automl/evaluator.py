import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, mean_squared_error,
    mean_absolute_error, r2_score, log_loss, explained_variance_score
)
import logging
from automl.test_transformer import TestTransformer

# Configure logging
logger = logging.getLogger(__name__)

class Evaluator:
    """Class for evaluating model performance.
    
    This class handles both classification and regression tasks, providing
    appropriate metrics for each case. It works with the TestTransformer
    to ensure consistent data handling.
    
    Attributes:
        problem_type (str): Type of problem ('classification' or 'regression')
        test_transformer (TestTransformer): Instance of TestTransformer for data handling
        metrics (dict): Dictionary to store computed metrics
        
    Note:
        Feature importance is not calculated here as the models operate on
        transformed features (PCA/LDA). For feature importance, use the
        FeatureSelector class which operates on original features.
    """
    
    def __init__(self, problem_type, test_transformer):
        """Initialize the Evaluator.
        
        Args:
            problem_type (str): Type of problem ('classification' or 'regression')
            test_transformer (TestTransformer): Instance of TestTransformer
            
        Raises:
            ValueError: If problem_type is not 'classification' or 'regression'
        """
        if problem_type not in ['classification', 'regression']:
            raise ValueError("problem_type must be 'classification' or 'regression'")
        
        self.problem_type = problem_type
        self.test_transformer = test_transformer
        self.metrics = {}
        logger.info(f"Initialized Evaluator for {problem_type} task")
    
    def evaluate(self, model, X_train, X_test, y_test=None):
        """Evaluate model performance on test data or just generate predictions."""

        logger.info("Starting model evaluation")
        
        X_test_transformed, y_test_transformed = self.test_transformer.transform(
            X_train, X_test, y_test
        )
        
        # Get predictions
        if self.problem_type == 'classification':
            y_pred_proba = model.predict_proba(X_test_transformed)
            y_pred = np.argmax(y_pred_proba, axis=1)
            
            if y_test_transformed is not None:
                self._compute_classification_metrics(y_test_transformed, y_pred, y_pred_proba)
        else:
            y_pred = model.predict(X_test_transformed)
            
            if y_test_transformed is not None:
                self._compute_regression_metrics(y_test_transformed, y_pred)

        # Always return predictions (even if metrics skipped)
        # self.metrics['predictions'] = self.test_transformer.inverse_transform_target(
        #     pd.Series(y_pred)
        # )

        return self.metrics


    def predict(self, model, X_train, X_val, X_test) -> pd.Series:
        """Return test predictions without computing metrics."""
        logger.info("Generating predictions without evaluation")
        X_test_transformed, _ = self.test_transformer.transform(
            X_train, X_val, X_test
        )
        y_pred = model.predict(X_test_transformed)
        return self.test_transformer.inverse_transform_target(pd.Series(y_pred))
    
    def _compute_classification_metrics(self, y_true, y_pred, y_pred_proba):
        """Compute classification metrics.
        
        Args:
            y_true (array-like): True labels
            y_pred (array-like): Predicted labels
            y_pred_proba (array-like): Predicted probabilities
        """
        # For binary classification, use probability of positive class
        # For multiclass, use OvR strategy with all probabilities
        if y_pred_proba.shape[1] == 2:
            y_score = y_pred_proba[:, 1]  # Probability of positive class
            multi_class = 'raise'  # Binary classification
        else:
            y_score = y_pred_proba  # Use all probabilities for multiclass
            multi_class = 'ovr'  # One-vs-Rest for multiclass
            
        self.metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted'),
            'roc_auc': roc_auc_score(y_true, y_score, multi_class=multi_class),
            'log_loss': log_loss(y_true, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
    
    def _compute_regression_metrics(self, y_true, y_pred):
        """Compute regression metrics.
        
        Args:
            y_true (array-like): True values
            y_pred (array-like): Predicted values
        """
        self.metrics = {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2': r2_score(y_true, y_pred),
            'explained_variance': explained_variance_score(y_true, y_pred)
        }
    
    def get_metrics(self):
        """Get computed metrics.
        
        Returns:
            dict: Dictionary containing computed metrics
            
        Raises:
            ValueError: If no metrics are available
        """
        if not self.metrics:
            raise ValueError("No metrics available. Run evaluate() first.")
        return self.metrics
    
    def print_report(self):
        """Print formatted evaluation report."""
        if not self.metrics or not isinstance(self.metrics, dict):
            logger.warning("No metrics available for report")
            print("No evaluation metrics were computed.")
            return

        print("\n=== Model Evaluation Report ===\n")

        if self.problem_type == 'classification':
            if all(metric in self.metrics for metric in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc', 'log_loss']):
                print("Classification Metrics:")
                print(f"Accuracy: {self.metrics['accuracy']:.4f}")
                print(f"Precision: {self.metrics['precision']:.4f}")
                print(f"Recall: {self.metrics['recall']:.4f}")
                print(f"F1 Score: {self.metrics['f1']:.4f}")
                print(f"ROC AUC: {self.metrics['roc_auc']:.4f}")
                print(f"Log Loss: {self.metrics['log_loss']:.4f}")
                print("\nConfusion Matrix:")
                print(np.array(self.metrics['confusion_matrix']))
            else:
                print("Test labels not available — skipping classification metric reporting.")
        else:
            if all(metric in self.metrics for metric in ['mse', 'rmse', 'mae', 'r2', 'explained_variance']):
                print("Regression Metrics:")
                print(f"MSE: {self.metrics['mse']:.4f}")
                print(f"RMSE: {self.metrics['rmse']:.4f}")
                print(f"MAE: {self.metrics['mae']:.4f}")
                print(f"R² Score: {self.metrics['r2']:.4f}")
                print(f"Explained Variance: {self.metrics['explained_variance']:.4f}")
            else:
                print("Test labels not available — skipping regression metric reporting.")

        if 'predictions' in self.metrics:
            print("\nPredictions are available in metrics['predictions']")
