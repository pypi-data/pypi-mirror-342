import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Union, Optional

class FeatureSelector(BaseEstimator, TransformerMixin):
    """
    Selects the most relevant features using a mix of strategies:
    - Removes low variance features
    - Removes highly correlated features
    - Selects top features based on combined importance (RandomForest + Mutual Info)
    """

    def __init__(
        self,
        problem_type: str,
        n_features: Union[int, float] = 0.5,
        corr_threshold: float = 0.95,
        variance_threshold: float = 0.01,
        importance_threshold: float = 0.01,
        random_state: Optional[int] = None
    ):
        if problem_type not in ['classification', 'regression']:
            raise ValueError("problem_type must be 'classification' or 'regression'")
        if isinstance(n_features, float) and not (0 < n_features <= 1.0):
            raise ValueError("If float, n_features must be > 0 and <= 1.0")
        elif isinstance(n_features, int) and n_features <= 0:
            raise ValueError("If int, n_features must be > 0")

        self.problem_type = problem_type
        self.n_features = n_features
        self.corr_threshold = corr_threshold
        self.variance_threshold = variance_threshold
        self.importance_threshold = importance_threshold
        self.random_state = random_state
        self.fitted = False

    def _validate_input(self, X: pd.DataFrame, y: np.ndarray):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame")
        if len(X) == 0:
            raise ValueError("X cannot be empty")
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")

    def _remove_low_variance(self, X: pd.DataFrame) -> List[str]:
        variances = X.var()
        return list(variances[variances > self.variance_threshold].index)

    def _remove_correlated(self, X: pd.DataFrame, features: List[str]) -> List[str]:
        corr_matrix = X[features].corr().abs()
        upper = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        to_drop = set()

        for i, j in zip(*np.where(upper & (corr_matrix > self.corr_threshold))):
            feat1, feat2 = features[i], features[j]
            if hasattr(self, 'feature_importances_'):
                if self.feature_importances_[feat1] < self.feature_importances_[feat2]:
                    to_drop.add(feat1)
                else:
                    to_drop.add(feat2)
            else:
                to_drop.add(feat2)

        return [f for f in features if f not in to_drop]

    def _get_importance_scores(self, X: pd.DataFrame, y: np.ndarray) -> pd.Series:
        if self.problem_type == 'classification':
            rf = RandomForestClassifier(n_estimators=100, random_state=self.random_state)
            mi_func = mutual_info_classif
        else:
            rf = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
            mi_func = mutual_info_regression

        rf.fit(X, y)
        rf_importance = pd.Series(rf.feature_importances_, index=X.columns)
        mi_importance = pd.Series(mi_func(X, y, random_state=self.random_state), index=X.columns)

        rf_importance = (rf_importance - rf_importance.min()) / (rf_importance.max() - rf_importance.min() + 1e-6)
        mi_importance = (mi_importance - mi_importance.min()) / (mi_importance.max() - mi_importance.min() + 1e-6)

        return (rf_importance + mi_importance) / 2

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'FeatureSelector':
        self._validate_input(X, y)
        self.feature_names_in_ = np.array(X.columns)


        self.feature_importances_ = self._get_importance_scores(X, y)
        selected = self._remove_low_variance(X)
        selected = self._remove_correlated(X, selected)

        importances = self.feature_importances_[selected]
        importances = importances[importances > self.importance_threshold]

        if isinstance(self.n_features, float):
            n = max(1, int(len(importances) * self.n_features))
        else:
            n = min(self.n_features, len(importances))

        self.selected_features_ = list(importances.nlargest(n).index)
        self.fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted:
            raise ValueError("FeatureSelector must be fitted before transform")
        missing = set(self.selected_features_) - set(X.columns)
        if missing:
            raise ValueError(f"Missing features in input: {missing}")
        return X[self.selected_features_].copy()

    def fit_transform(self, X: pd.DataFrame, y: np.ndarray) -> pd.DataFrame:
        return self.fit(X, y).transform(X)

    def get_feature_importances(self) -> pd.Series:
        if not self.fitted:
            raise RuntimeError("Feature selector must be fitted first")
        return self.feature_importances_[self.selected_features_]
