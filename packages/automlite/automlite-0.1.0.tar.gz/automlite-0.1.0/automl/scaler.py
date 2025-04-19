import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from scipy.stats import shapiro

class AutoScaler:
    """
    Automatically select and apply the most appropriate scaler for each feature.
    Assumes input data is:
    - All numerical
    - No missing values
    - Outliers already handled
    """

    def __init__(self, force_method=None):
        self.VALID_METHODS = {'standard', 'minmax', 'robust'}

        if force_method is not None and force_method not in self.VALID_METHODS:
            raise ValueError(f"force_method must be one of {self.VALID_METHODS}")
        
        self.force_method = force_method
        self.fitted = False
        self.scalers = {}
        self.feature_methods = {}

    def _verify_input(self, X):
        """Helper function to validate the input DataFrame."""
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
        if not all(pd.api.types.is_numeric_dtype(X[col]) for col in X.columns):
            raise ValueError("All features must be numeric")
        if X.isnull().values.any():
            raise ValueError("Data contains missing values")

    def _select_scaler(self, series: pd.Series) -> str:
        """Helper function to select appropriate scaler based on feature distribution."""
        if self.force_method:
            return self.force_method

        # If constant feature, skip Shapiro (it fails)
        if series.nunique() == 1:
            return 'standard'

        # Normal distribution check
        try:
            _, p = shapiro(series)
        except ValueError:  # Handle exception for Shapiro test specifically
            p = 0

        if p > 0.05:
            return 'standard'

        iqr = np.percentile(series, 75) - np.percentile(series, 25)
        total_range = series.max() - series.min()

        # Histogram-based uniformity score
        hist, _ = np.histogram(series, bins='auto')
        uniformity = 1 - (np.std(hist) / np.mean(hist)) if np.mean(hist) != 0 else 0

        if uniformity > 0.5:
            return 'minmax'

        return 'robust'

    def _check_fitted(self):
        """Utility function to check if the model has been fitted."""
        if not self.fitted:
            raise ValueError("Scaler must be fitted before calling this method")

    def fit(self, X: pd.DataFrame):
        """Fit the scalers to each feature."""
        self._verify_input(X)

        for col in X.columns:
            method = self._select_scaler(X[col])
            self.feature_methods[col] = method

            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            else:
                scaler = RobustScaler()

            scaler.fit(X[[col]])
            self.scalers[col] = scaler

        self.fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform the features using the fitted scalers."""
        self._verify_input(X)
        self._check_fitted()

        missing = set(self.scalers) - set(X.columns)
        if missing:
            raise ValueError(f"Test data missing features: {missing}")

        return pd.DataFrame({
            col: self.scalers[col].transform(X[[col]]).flatten()
            for col in self.scalers if col in X.columns
        }, index=X.index)

    def inverse_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Inverse transform the features using the fitted scalers."""
        self._verify_input(X)
        self._check_fitted()

        return pd.DataFrame({
            col: self.scalers[col].inverse_transform(X[[col]]).flatten()
            for col in self.scalers if col in X.columns
        }, index=X.index)

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Fit and then transform the data in one step."""
        return self.fit(X).transform(X)

    def get_scaling_strategies(self):
        """Return the scaling strategies for each feature."""
        self._check_fitted()
        return self.feature_methods.copy()
