import numpy as np
import pandas as pd
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
import logging
from typing import Dict, List, Optional, Set, Tuple, Union
from automl.utils import DataFrameAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AutoML.OutlierHandler')

class OutlierHandler:
    """
    A class for detecting and handling outliers using multiple methods.
    
    Methods:
    1. Modified Z-score (for normal distributions)
    2. IQR method (for any distribution)
    3. Isolation Forest (for high-dimensional data)
    4. Local Outlier Factor (for density-based detection)
    5. Elliptic Envelope (for Gaussian distributions)
    
    Features:
    - Voting system to combine multiple methods
    - Distribution-aware method selection
    - Configurable sensitivity/aggression level
    - Multiple handling strategies (removal or capping)
    """
    
    def __init__(
        self, 
        X_train: pd.DataFrame,
        X_val: Optional[pd.DataFrame] = None,
        y_train: Optional[pd.Series] = None,
        y_val: Optional[pd.Series] = None,
        problem_type: str = "classification",
        sensitivity: float = 20.0,
        random_state: int = 42
    ):
        """
        Initialize OutlierHandler.
        
        Parameters
        ----------
        X_train : pd.DataFrame
            Training features
        X_val : pd.DataFrame, optional
            Validation features
        y_train : pd.Series, optional
            Training target
        y_val : pd.Series, optional
            Validation target
        problem_type : str, default="classification"
            Type of problem - "classification" or "regression"
        sensitivity : float, default=20.0
            Controls how aggressive outlier detection should be (1-100)
            Higher values = more aggressive detection
        random_state : int, default=42
            Random state for reproducibility
        """
        self.X_train = X_train.copy()
        self.X_val = X_val.copy() if X_val is not None else None
        self.y_train = y_train.copy() if y_train is not None else None
        self.y_val = y_val.copy() if y_val is not None else None
        
        self.X = pd.concat([self.X_train, self.X_val]) if X_val is not None else self.X_train
        self.analyzer = DataFrameAnalyzer()
        
        if not (0 < sensitivity <= 100):
            raise ValueError("sensitivity must be between 1 and 100")
        self.sensitivity = sensitivity
        
        if problem_type not in ["classification", "regression"]:
            raise ValueError("problem_type must be 'classification' or 'regression'")
        self.problem_type = problem_type
        
        # More votes needed for classification to avoid removing important minority classes
        self.vote_threshold = 2 if problem_type == "classification" else 1
        
        self.random_state = random_state
        self.outliers: Dict[str, Set[int]] = {}  # Maps features to outlier indices
        self.outlier_indexes: Dict[str, Dict[int, List[str]]] = {
            "X_train": {},
            "X_val": {} if X_val is not None else None
        }
        
        logger.info(f"Initialized OutlierHandler with sensitivity={sensitivity}")
        logger.info(f"Problem type: {problem_type} | Vote threshold: {self.vote_threshold}")
        logger.info(f"Combined data shape: {self.X.shape}")
        
    def _get_sensitivity_params(self) -> Tuple[float, float, float]:
        """Get sensitivity-adjusted parameters for outlier detection."""
        # Z-score threshold decreases as sensitivity increases
        z_threshold = 3 / (1 + np.log1p(self.sensitivity))
        
        # IQR multiplier increases with sensitivity
        iqr_multiplier = 1.5 * (1 + (self.sensitivity ** 0.3))
        
        # Contamination rate for Isolation Forest/LOF increases with sensitivity
        contamination_rate = min(0.05 + (self.sensitivity / 200), 0.25)
        
        return z_threshold, iqr_multiplier, contamination_rate
        
    def _detect_zscore_outliers(self, series: pd.Series, z_threshold: float) -> Set[int]:
        """Detect outliers using modified z-score method."""
        if series.std() < 1e-8:  # Constant or near-constant series
            return set()
            
        z_scores = np.abs(zscore(series.dropna()))
        outliers = set(series.dropna().index[z_scores > z_threshold])
        
        if outliers:
            logger.debug(
                f"Z-score outliers found: {len(outliers)}\n"
                f"Mean: {series.mean():.2f}, Std: {series.std():.2f}\n"
                f"Threshold: {z_threshold:.2f}"
            )
            
        return outliers
        
    def _detect_iqr_outliers(self, series: pd.Series, iqr_multiplier: float) -> Set[int]:
        """Detect outliers using IQR method."""
        Q1, Q3 = np.percentile(series.dropna(), [25, 75])
        IQR = Q3 - Q1
        
        if IQR == 0:  # Handle series with very low variance
            return set()
            
        lower_bound = Q1 - iqr_multiplier * IQR
        upper_bound = Q3 + iqr_multiplier * IQR
        
        outliers = set(series.index[
            (series < lower_bound) | (series > upper_bound)
        ])
        
        if outliers:
            logger.debug(
                f"IQR outliers found: {len(outliers)}\n"
                f"Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}\n"
                f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]"
            )
            
        return outliers
        
    def _detect_iforest_outliers(
        self, 
        feature: str, 
        contamination: float
    ) -> Set[int]:
        """Detect outliers using Isolation Forest."""
        clf = IsolationForest(
            contamination=contamination,
            random_state=self.random_state
        )
        preds = clf.fit_predict(self.X[[feature]])
        return set(self.X.index[preds == -1])
        
    def _detect_lof_outliers(
        self, 
        feature: str, 
        contamination: float
    ) -> Set[int]:
        """Detect outliers using Local Outlier Factor."""
        X_feat = self.X[[feature]].dropna()
        
        # LOF needs at least 2 samples
        if X_feat.shape[0] < 2:
            logger.warning(f"Skipping LOF for '{feature}' due to insufficient samples.")
            return set()

        try:
            lof = LocalOutlierFactor(
                contamination=contamination,
                novelty=False,
                n_neighbors=min(20, len(X_feat) - 1)
            )
            preds = lof.fit_predict(X_feat)
            return set(X_feat.index[preds == -1])
        except Exception as e:
            logger.warning(f"LOF failed for '{feature}' due to: {e}")
            return set()

        
    def _detect_gaussian_outliers(
        self, 
        feature: str, 
        contamination: float
    ) -> Set[int]:
        """Detect outliers using Elliptic Envelope (for Gaussian data)."""
        series = self.X[feature]
        
        # Skip if data is constant or near-constant
        if series.std() < 1e-8:
            return set()
            
        # Skip if too few samples for covariance estimation
        if len(series) < 5:
            return set()
            
        try:
            ee = EllipticEnvelope(
                contamination=contamination,
                random_state=self.random_state,
                support_fraction=0.8  # More robust estimation
            )
            preds = ee.fit_predict(series.values.reshape(-1, 1))
            return set(series.index[preds == -1])
        except ValueError:
            # If covariance estimation fails, fall back to z-score
            logger.warning(
                f"Elliptic Envelope failed for feature '{feature}', "
                "falling back to z-score method"
            )
            return self._detect_zscore_outliers(series, 3.0)
        
    def detect_outliers(self) -> Dict[str, Dict[int, List[str]]]:
        """
        Detect outliers in all numeric features using multiple methods.
        
        Returns
        -------
        Dict[str, Dict[int, List[str]]]
            Nested dictionary mapping dataset ('X_train'/'X_val') to 
            outlier indices and their corresponding features
        """
        logger.info("\nStarting outlier detection...")
        
        # Get sensitivity-adjusted parameters
        z_threshold, iqr_multiplier, contamination = self._get_sensitivity_params()
        logger.debug(
            f"Parameters:\n"
            f"Z-score threshold: {z_threshold:.2f}\n"
            f"IQR multiplier: {iqr_multiplier:.2f}\n"
            f"Contamination rate: {contamination:.2f}"
        )
        
        numeric_features = self.analyzer.get_numeric_columns(self.X)
        logger.debug(f"Numeric features to analyze: {numeric_features}")
        
        # Store IQR bounds for each feature
        self.feature_bounds = {}
        
        for feature in numeric_features:
            if self.analyzer.is_id_column(self.X[feature]):
                logger.info(f"Skipping ID column: {feature}")
                continue
                
            # Calculate IQR bounds first
            Q1 = self.X[feature].quantile(0.25)
            Q3 = self.X[feature].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - iqr_multiplier * IQR
            upper_bound = Q3 + iqr_multiplier * IQR
            self.feature_bounds[feature] = (lower_bound, upper_bound)
                
            distribution = self.analyzer.check_distribution(self.X[feature])
            logger.info(f"\nAnalyzing feature: '{feature}' | Distribution: {distribution}")
            
            # Initialize outlier sets
            outlier_sets = []
            
            # Always apply IQR method as it works for any distribution
            iqr_outliers = self._detect_iqr_outliers(self.X[feature], iqr_multiplier)
            if iqr_outliers:
                outlier_sets.append(iqr_outliers)
                logger.info(f"IQR outliers: {sorted(iqr_outliers)}")
            
            # Apply z-score and Gaussian methods for normal distributions
            if distribution == 'normal':
                zscore_outliers = self._detect_zscore_outliers(self.X[feature], z_threshold)
                if zscore_outliers:
                    outlier_sets.append(zscore_outliers)
                    logger.info(f"Z-score outliers: {sorted(zscore_outliers)}")
                
                gaussian_outliers = self._detect_gaussian_outliers(feature, contamination)
                if gaussian_outliers:
                    outlier_sets.append(gaussian_outliers)
                    logger.info(f"Gaussian outliers: {sorted(gaussian_outliers)}")
            
            # Apply Isolation Forest for high-dimensional or skewed data
            if distribution == 'skewed' or len(numeric_features) > 10:
                iforest_outliers = self._detect_iforest_outliers(feature, contamination)
                if iforest_outliers:
                    outlier_sets.append(iforest_outliers)
                    logger.info(f"Isolation Forest outliers: {sorted(iforest_outliers)}")
            
            # Apply LOF for density-based detection if enough samples
            if len(self.X) >= 20:
                lof_outliers = self._detect_lof_outliers(feature, contamination)
                if lof_outliers:
                    outlier_sets.append(lof_outliers)
                    logger.info(f"LOF outliers: {sorted(lof_outliers)}")
            
            if not outlier_sets:
                logger.info(f"No outliers detected for feature '{feature}'")
                continue
            
            # Count votes for each index
            vote_counts = {}
            for outlier_set in outlier_sets:
                for idx in outlier_set:
                    vote_counts[idx] = vote_counts.get(idx, 0) + 1
            
            # Get indices that meet the vote threshold
            final_outliers = {
                idx for idx, votes in vote_counts.items() 
                if votes >= self.vote_threshold
            }
            
            if final_outliers:
                logger.info(
                    f"Final outliers for '{feature}': {sorted(final_outliers)} "
                    f"(vote threshold: {self.vote_threshold})"
                )
                self.outliers[feature] = final_outliers
                
                # Update outlier_indexes for both train and validation sets
                train_mask = self.X_train.index.isin(final_outliers)
                if train_mask.any():
                    train_outliers = self.X_train.index[train_mask]
                    for idx in train_outliers:
                        if idx not in self.outlier_indexes["X_train"]:
                            self.outlier_indexes["X_train"][idx] = []
                        self.outlier_indexes["X_train"][idx].append(feature)
                
                if self.X_val is not None:
                    val_mask = self.X_val.index.isin(final_outliers)
                    if val_mask.any():
                        val_outliers = self.X_val.index[val_mask]
                        for idx in val_outliers:
                            if idx not in self.outlier_indexes["X_val"]:
                                self.outlier_indexes["X_val"][idx] = []
                            self.outlier_indexes["X_val"][idx].append(feature)
        
        logger.info("\nOutlier detection completed.")
        return self.outlier_indexes
    
    def handle_outliers(self, strategy="clip", keep_indices=None):
        """
        Handle outliers in the data using the specified strategy.

        Parameters
        ----------
        strategy : str, optional (default="clip")
            The strategy to handle outliers:
            - "clip": Clip outlier values to the IQR boundaries
            - "remove": Remove outlier rows
        keep_indices : list, optional (default=None)
            List of indices to keep even if they are outliers

        Returns
        -------
        tuple
            (X_train_new, X_val_new, y_train_new, y_val_new)
        """
        if not self.outlier_indexes:
            logger.warning("No outliers detected. Returning original data.")
            return self.X_train, self.X_val, self.y_train, self.y_val

        X_train_new = self.X_train.copy()
        y_train_new = self.y_train.copy() if self.y_train is not None else None
        X_val_new = self.X_val.copy() if self.X_val is not None else None
        y_val_new = self.y_val.copy() if self.y_val is not None else None

        # Filter out indices that should be kept
        keep_indices = set(keep_indices or [])
        train_outliers = {
            idx: cols for idx, cols in self.outlier_indexes["X_train"].items()
            if idx not in keep_indices
        }
        val_outliers = {
            idx: cols for idx, cols in self.outlier_indexes.get("X_val", {}).items()
            if idx not in keep_indices
        }

        if strategy == "clip":
            # Handle training data
            for col in self.outliers.keys():
                lower_bound, upper_bound = self.feature_bounds[col]
                
                # Only clip values for identified outliers
                for idx, cols in train_outliers.items():
                    if col in cols:
                        value = X_train_new.at[idx, col]
                        if value < lower_bound:
                            X_train_new.at[idx, col] = lower_bound
                        elif value > upper_bound:
                            X_train_new.at[idx, col] = upper_bound

            # Handle validation data if it exists
            if X_val_new is not None and val_outliers:
                for col in self.outliers.keys():
                    lower_bound, upper_bound = self.feature_bounds[col]
                    
                    # Only clip values for identified outliers
                    for idx, cols in val_outliers.items():
                        if col in cols:
                            value = X_val_new.at[idx, col]
                            if value < lower_bound:
                                X_val_new.at[idx, col] = lower_bound
                            elif value > upper_bound:
                                X_val_new.at[idx, col] = upper_bound

        elif strategy == "remove":
            # Remove outliers from training data
            train_indices_to_remove = list(train_outliers.keys())
            if train_indices_to_remove:
                X_train_new = X_train_new.drop(index=train_indices_to_remove)
                if y_train_new is not None:
                    y_train_new = y_train_new[~y_train_new.index.isin(train_indices_to_remove)]

            # Remove outliers from validation data if it exists
            if X_val_new is not None:
                val_indices_to_remove = list(val_outliers.keys())
                if val_indices_to_remove:
                    X_val_new = X_val_new.drop(index=val_indices_to_remove)
                    if y_val_new is not None:
                        y_val_new = y_val_new[~y_val_new.index.isin(val_indices_to_remove)]
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        return X_train_new, X_val_new, y_train_new, y_val_new 