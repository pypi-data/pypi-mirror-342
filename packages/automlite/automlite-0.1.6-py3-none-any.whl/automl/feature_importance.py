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
        self._is_fit = hasattr(model, 'predict')
        self._background_needed = True
        self._background_data = None
        self._sanitized_to_original = {}  # Mapping from sanitized to original feature names
        
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
    
    def fit(self, X: pd.DataFrame, y: Optional[Union[pd.Series, np.ndarray]] = None):
        """
        Fit the model to the data if y is provided.
        
        Args:
            X: Features DataFrame
            y: Target variable (optional, only needed if model is not already fit)
            
        Returns:
            self
        """
        # Store original feature names for mapping back later
        self._feature_names = list(X.columns)
        
        # Create a copy with sanitized column names for XGBoost compatibility
        X_sanitized = X.copy()
        
        # Check if it's a model with strict feature name requirements
        model_name = type(self.model).__name__
        if 'XGB' in model_name or 'xgb' in model_name:
            # Sanitize column names
            sanitized_columns = {}
            for col in X.columns:
                # Replace any problematic characters
                sanitized_col = col.replace('[', '_').replace(']', '_').replace('<', '_').replace('>', '_')
                if sanitized_col != col:
                    sanitized_columns[col] = sanitized_col
                    self._sanitized_to_original[sanitized_col] = col
            
            # If we need to rename columns, do it
            if sanitized_columns:
                X_sanitized = X.rename(columns=sanitized_columns)
                logger.info(f"Sanitized {len(sanitized_columns)} column names for compatibility")
            
            # Handle early stopping parameters for XGBoost models
            if y is not None and hasattr(self.model, 'get_params'):
                params = self.model.get_params()
                if 'early_stopping_rounds' in params and params['early_stopping_rounds'] is not None:
                    # Create a temporary model without early stopping for feature importance
                    logger.info("Creating temporary model without early stopping for feature importance")
                    temp_model = clone(self.model)
                    temp_model.set_params(early_stopping_rounds=None)
                    try:
                        temp_model.fit(X_sanitized, y)
                        self.model = temp_model  # Replace with fitted model without early stopping
                        self._is_fit = True
                        return self
                    except Exception as e:
                        logger.warning(f"Failed to fit without early stopping: {e}")
                        # Continue with original approach if this fails
        
        # Store the model if not already set
        # Fit the model if target values are provided
        if y is not None:
            try:
                self.model.fit(X_sanitized, y)
                self._is_fit = True
            except Exception as e:
                logger.error(f"Error fitting model in FeatureImportance: {e}")
                raise
        
        # If model requires background data for explanations, store it
        if self._background_needed:
            # Keep a small sample to avoid memory issues
            if len(X_sanitized) > 100:
                self._background_data = X_sanitized.sample(100, random_state=42)
            else:
                self._background_data = X_sanitized
                
        return self
    
    def compute_importance(self, X: pd.DataFrame, sample_size: int = 1000, n_jobs: int = -1) -> pd.DataFrame:
        """
        Compute feature importance using SHAP values with optimizations for large datasets.
        
        Args:
            X: Input features as a pandas DataFrame
            sample_size: Maximum number of samples to use for SHAP calculation
                         (improves speed for large datasets)
            n_jobs: Number of jobs for parallel computation (-1 means use all cores)
            
        Returns:
            DataFrame containing feature importance values
        """
        # Store original feature names for mapping back later
        original_feature_names = list(X.columns)
        self._feature_names = original_feature_names
        
        # Create a copy with sanitized column names for XGBoost compatibility
        X_sanitized = X.copy()
        sanitized_to_original = {}  # Mapping from sanitized names to original names
        
        # Check if it's a model with strict feature name requirements
        model_name = type(self.model).__name__
        if 'XGB' in model_name or 'xgb' in model_name:
            # Sanitize column names
            sanitized_columns = {}
            for col in X.columns:
                # Replace any problematic characters
                sanitized_col = col.replace('[', '_').replace(']', '_').replace('<', '_').replace('>', '_')
                if sanitized_col != col:
                    sanitized_columns[col] = sanitized_col
                    sanitized_to_original[sanitized_col] = col
            
            # If we need to rename columns, do it
            if sanitized_columns:
                X_sanitized = X.rename(columns=sanitized_columns)
                logger.info(f"Sanitized {len(sanitized_columns)} column names for compatibility")
        
        # Sample data if it's too large (significantly improves performance)
        if len(X_sanitized) > sample_size:
            logger.info(f"Sampling {sample_size} rows from {len(X_sanitized)} for faster SHAP calculation")
            X_sample = X_sanitized.sample(sample_size, random_state=42)
        else:
            X_sample = X_sanitized
        
        # Determine the best explainer based on the model type
        # Tree-based models can use the much faster TreeExplainer
        is_tree_based = hasattr(self.model, 'estimators_') or type(self.model).__name__ in [
            'RandomForestClassifier', 'RandomForestRegressor', 
            'XGBClassifier', 'XGBRegressor', 
            'LGBMClassifier', 'LGBMRegressor',
            'CatBoostClassifier', 'CatBoostRegressor'
        ]
        
        try:
            if is_tree_based:
                logger.info("Using TreeExplainer for SHAP calculation")
                explainer = shap.TreeExplainer(self.model)
                # For tree-based models we can calculate SHAP values faster
                self._shap_values = explainer.shap_values(X_sample)
            else:
                logger.info("Using KernelExplainer for SHAP calculation")
                # Use a much smaller background dataset for KernelExplainer
                background = shap.kmeans(X_sample, min(50, len(X_sample)))
                
                # Select appropriate prediction function
                if hasattr(self.model, 'predict_proba') and self.problem_type == 'classification':
                    predict_fn = self.model.predict_proba
                else:
                    predict_fn = self.model.predict
                
                explainer = shap.KernelExplainer(predict_fn, background)
                
                # Use nsamples parameter to speed up KernelExplainer
                self._shap_values = explainer.shap_values(
                    X_sample, 
                    nsamples=100,  # Reduce for even faster calculation
                    l1_reg="aic"   # Use AIC for automatic regularization
                )
        except Exception as e:
            logger.error(f"SHAP calculation failed: {e}")
            # Fallback to basic feature importance if SHAP fails
            logger.info("Falling back to model's feature_importances_ attribute")
            if hasattr(self.model, 'feature_importances_'):
                importance_values = self.model.feature_importances_
                # Create DataFrame and return
                feature_names = X_sanitized.columns
                
                # Map sanitized names back to original if needed
                if sanitized_to_original:
                    feature_names = [sanitized_to_original.get(col, col) for col in feature_names]
                
                self._importance_df = pd.DataFrame(
                    list(zip(feature_names, importance_values)),
                    columns=['feature', 'importance_value']
                ).sort_values('importance_value', ascending=False)
                return self._importance_df
            else:
                # If all else fails, return a DataFrame with zeros
                self._importance_df = pd.DataFrame(
                    list(zip(original_feature_names, np.zeros(len(original_feature_names)))),
                    columns=['feature', 'importance_value']
                )
                return self._importance_df
        
        # Handle multi-class classification case
        if isinstance(self._shap_values, list):
            # For multi-class, take mean absolute SHAP value across all classes
            importance_values = np.mean([np.mean(np.abs(sv), axis=0) for sv in self._shap_values], axis=0)
        else:
            importance_values = np.mean(np.abs(self._shap_values), axis=0)
        
        # Ensure importance_values is 1-dimensional
        importance_values = np.ravel(importance_values)
        
        # Get correct feature names (original or sanitized)
        feature_names = X_sanitized.columns
        
        # Map sanitized names back to original if needed
        if sanitized_to_original:
            feature_names = [sanitized_to_original.get(col, col) for col in feature_names]
        
        # Create DataFrame and sort by importance
        self._importance_df = pd.DataFrame(
            list(zip(feature_names, importance_values)),
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
        plt.show()
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