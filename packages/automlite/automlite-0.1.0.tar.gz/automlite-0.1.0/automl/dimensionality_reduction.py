import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from typing import Optional
import warnings
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DimensionalityReducer:
    def __init__(self, task_type='classification', n_components=None, variance_threshold=0.95, force_method=None):
        if task_type not in ['classification', 'regression']:
            raise ValueError("task_type must be either 'classification' or 'regression'")
        if not (0 < variance_threshold <= 1):
            raise ValueError("variance_threshold must be between 0 and 1")
        if force_method not in [None, 'pca', 'lda']:
            raise ValueError("force_method must be either 'pca', 'lda', or None")

        self.task_type = task_type
        self.n_components = n_components
        self.variance_threshold = variance_threshold
        self.force_method = force_method
        self.fitted = False
        self.feature_importance_ = pd.DataFrame()
        self.n_features_in_ = None
        self.feature_names_in_ = None

    def _validate_data(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame")
        if X.isnull().any().any():
            raise ValueError("X contains missing values")
        if np.isinf(X.values).any():
            raise ValueError("X contains infinite values")
        if self.fitted and X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X has {X.shape[1]} features, but DimensionalityReducer was trained with {self.n_features_in_} features"
            )

    def _choose_method(self, X, y):
        if self.force_method:
            logger.info(f"Using forced dimensionality reduction method: {self.force_method.upper()}")
            return self.force_method

        if self.task_type == 'classification' and y is not None:
            try:
                lda = LinearDiscriminantAnalysis()
                lda.fit(X, y)
                logger.info("Automatically selected LDA for dimensionality reduction.")
                return 'lda'
            except Exception:
                logger.warning("LDA failed; falling back to PCA.")
                return 'pca'

        logger.info("Automatically selected PCA for dimensionality reduction.")
        return 'pca'

    def fit(self, X, y=None):
        self._validate_data(X, y)
        self.n_features_in_ = X.shape[1]
        self.feature_names_in_ = X.columns.tolist()

        method = self._choose_method(X, y)
        self.selected_method_ = method  # Store method used for get_graphs()

        n_components = self.n_components or min(X.shape[1], X.shape[0])

        if method == 'lda':
            try:
                self.reducer_ = LinearDiscriminantAnalysis(n_components=min(len(np.unique(y)) - 1, n_components))
                self.reducer_.fit(X, y)
                self.feature_importance_ = pd.DataFrame({
                    'Feature': self.feature_names_in_,
                    'Discrimination Power': np.abs(self.reducer_.coef_[0])
                }).sort_values('Discrimination Power', ascending=False)
            except Exception:
                warnings.warn("LDA failed due to singular matrices", UserWarning)
                logger.warning("LDA failed; falling back to PCA.")
                self.reducer_ = PCA(n_components=n_components)
                self.reducer_.fit(X)
                self.feature_importance_ = pd.DataFrame({
                    'Feature': self.feature_names_in_,
                    '% Variance Explained': np.abs(self.reducer_.components_).mean(axis=0)
                }).sort_values('% Variance Explained', ascending=False)
                self.selected_method_ = 'pca'
        elif method == 'pca':
            self.reducer_ = PCA(n_components=n_components)
            self.reducer_.fit(X)
            self.feature_importance_ = pd.DataFrame({
                'Feature': self.feature_names_in_,
                '% Variance Explained': np.abs(self.reducer_.components_).mean(axis=0)
            }).sort_values('% Variance Explained', ascending=False)
        else:
            raise ValueError(f"Unknown method: {method}")

        n_components_learned = self.reducer_.transform(X).shape[1]
        logger.info(f"Dimensionality reduced from {self.n_features_in_} to {n_components_learned} components.")

        self.fitted = True
        return self


    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_data(X)
        if not self.fitted:
            raise RuntimeError("Call fit before transform")

        transformed = self.reducer_.transform(X)
        n_components = transformed.shape[1]
        return pd.DataFrame(
            transformed,
            columns=[f"Component_{i+1}" for i in range(n_components)],
            index=X.index
        )

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        return self.fit(X, y).transform(X)

    def get_feature_importance(self) -> pd.DataFrame:
        if self.feature_importance_.empty:
            raise RuntimeError("Call fit first to compute feature importance")
        return self.feature_importance_.copy()

    def get_graphs(self):
        """Plot feature importance graph."""
        if self.feature_importance_.empty:
            raise RuntimeError("Call fit before plotting graphs")

        importance_column = 'Discrimination Power' if self.selected_method_ == 'lda' else '% Variance Explained'
        df = self.feature_importance_.copy()

        plt.figure(figsize=(10, 6))
        plt.barh(df['Feature'], df[importance_column], color='skyblue')
        plt.xlabel(importance_column)
        plt.title(f"Feature Importance ({self.selected_method_.upper()})")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
