import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, r2_score, roc_auc_score,
    mean_squared_error, log_loss, mean_absolute_error
)
from typing import List, Dict, Union, Optional, Tuple
import logging
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
import shap
from sklearn.base import clone, BaseEstimator

logger = logging.getLogger(__name__)

class FeatureImportance:
    """Class for computing feature importance using SHAP values.
    
    This class uses SHAP (SHapley Additive exPlanations) to determine feature
    importance. It works directly with the best model from model selection,
    applying it to the preprocessed data (after encoding, scaling, etc.)
    but before dimensionality reduction.
    
    The class handles:
    - Encoded categorical features (one-hot/label)
    - Scaled numerical features
    - Imputed missing values
    - Feature engineered columns
    
    Attributes:
        model: Best model from model selection
        problem_type (str): Type of problem ('classification' or 'regression')
        feature_groups (dict): Mapping of original features to their transformed columns
    """
    
    def __init__(self, model: BaseEstimator, problem_type: str):
        """
        Initialize the FeatureImportance class.
        
        Args:
            model: A fitted sklearn-compatible model
            problem_type: Type of problem - either 'classification' or 'regression'
        
        Raises:
            ValueError: If problem_type is not 'classification' or 'regression'
        """
        if problem_type not in ['classification', 'regression']:
            raise ValueError("Problem type must be either 'classification' or 'regression'")
        
        self.model = model
        self.problem_type = problem_type
        self._importance_df = None
        self._shap_values = None
        self._feature_names = None
        self.explainer = None
        self.original_features = None
        
        logger.info(f"Initialized FeatureImportance for {problem_type}")
    
    def _aggregate_feature_importance(
        self,
        importance_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Aggregate importance scores for transformed features back to original features.
        
        Args:
            importance_df: DataFrame with importance scores for transformed features
            
        Returns:
            pd.DataFrame: Aggregated importance scores for original features
        """
        if self.original_features is None:
            return importance_df
            
        aggregated_scores = []
        
        for orig_feature in self.original_features:
            # Get scores for all transformed versions of this feature
            feature_scores = importance_df.loc[orig_feature]
            
            # Aggregate scores (sum for one-hot encoded, mean for scaled)
            agg_mean = feature_scores['importance_mean'].sum()
            # For std, use root of sum of squares
            agg_std = np.sqrt((feature_scores['importance_std'] ** 2).sum())
            
            aggregated_scores.append({
                'feature': orig_feature,
                'importance_mean': agg_mean,
                'importance_std': agg_std
            })
        
        # Create DataFrame and sort
        results = pd.DataFrame(aggregated_scores)
        return results.sort_values(
            'importance_mean', ascending=False
        ).set_index('feature')
    
    def fit(
        self,
        X: pd.DataFrame,
        y: Optional[np.ndarray] = None,
        background_data: Optional[pd.DataFrame] = None
    ) -> 'FeatureImportance':
        """Fit the model and create SHAP explainer.
        
        Args:
            X: Training data
            y: Target values (optional if model is already fitted)
            background_data: Background data for SHAP explainer.
                If None, uses training data.
                
        Returns:
            self: The fitted instance
        """
        # Store feature names
        self._feature_names = list(X.columns)
        
        # Fit model if y is provided
        if y is not None:
            self.model.fit(X, y)
        
        # Create SHAP explainer
        if background_data is None:
            background_data = X
            
        try:
            # Try Tree explainer first (faster for tree-based models)
            self.explainer = shap.TreeExplainer(self.model, background_data)
        except:
            try:
                # Fall back to Kernel explainer
                predict_fn = self.model.predict_proba if self.problem_type == 'classification' else self.model.predict
                self.explainer = shap.KernelExplainer(predict_fn, background_data)
            except Exception as e:
                logger.error(f"Failed to create SHAP explainer: {str(e)}")
                raise
        
        logger.info("SHAP explainer created successfully")
        return self
    
    def compute_importance(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Compute feature importance using SHAP values.
        
        Args:
            X: Input features as a pandas DataFrame
            
        Returns:
            DataFrame containing feature importance values
        """
        self._feature_names = list(X.columns)
        
        # Initialize the SHAP explainer based on model type
        if hasattr(self.model, 'predict_proba'):
            explainer = shap.TreeExplainer(self.model) if hasattr(self.model, 'estimators_') else shap.KernelExplainer(self.model.predict_proba, X)
        else:
            explainer = shap.TreeExplainer(self.model) if hasattr(self.model, 'estimators_') else shap.KernelExplainer(self.model.predict, X)
        
        # Compute SHAP values
        self._shap_values = explainer.shap_values(X)
        
        # Handle multi-class classification case
        if isinstance(self._shap_values, list):
            # For multi-class, take mean absolute SHAP value across all classes
            importance_values = np.mean([np.mean(np.abs(sv), axis=0) for sv in self._shap_values], axis=0)
        else:
            importance_values = np.mean(np.abs(self._shap_values), axis=0)
        
        # Ensure importance_values is 1-dimensional
        importance_values = np.ravel(importance_values)
        
        # Create list of tuples with feature names and importance values
        feature_importance = list(zip(self._feature_names, importance_values))
        
        # Create DataFrame and sort by importance
        self._importance_df = pd.DataFrame(
            feature_importance,
            columns=['feature', 'importance_value']
        ).sort_values('importance_value', ascending=False)
        
        return self._importance_df
    
    def plot_importance(self, 
                       top_n: Optional[int] = None,
                       figsize: tuple = (10, 6),
                       title: str = 'Feature Importance',
                       xlabel: str = 'Importance Value',
                       ylabel: str = 'Features') -> plt.Figure:
        """
        Plot feature importance.
        
        Args:
            top_n: Number of top features to plot
            figsize: Figure size as (width, height)
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            
        Returns:
            matplotlib Figure object
            
        Raises:
            ValueError: If importance hasn't been computed yet
        """
        if self._importance_df is None:
            raise ValueError("Feature importance has not been computed yet")
        
        # Select top N features if specified
        plot_df = self._importance_df.head(top_n) if top_n else self._importance_df
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create horizontal bar plot
        ax.barh(plot_df['feature'], plot_df['importance_value'])
        
        # Customize plot
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Reverse y-axis to show most important features at top
        ax.invert_yaxis()
        
        plt.tight_layout()
        return fig
    
    def plot_dependence(
        self,
        feature: str,
        interaction_feature: Optional[str] = None,
        X: Optional[pd.DataFrame] = None
    ) -> plt.Figure:
        """Plot dependence plot for a feature.
        
        Args:
            feature: Feature to plot
            interaction_feature: Feature to use for interaction effects
            X: Data to use for plotting. If None, uses data from last
               compute_importance call.
               
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        if self._shap_values is None:
            raise ValueError("Must call compute_importance() before plot_dependence()")
            
        plt.figure()
        shap.dependence_plot(
            feature,
            self._shap_values,
            X if X is not None else self._feature_names,
            interaction_index=interaction_feature,
            show=False
        )
        return plt.gcf() 