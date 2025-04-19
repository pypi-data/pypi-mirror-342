import numpy as np
import pandas as pd
import copy
import optuna
import logging
from typing import Dict, Optional, Tuple

from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import f1_score, mean_squared_error
from sklearn.base import BaseEstimator

from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor
import lightgbm

# Configure logging
logger = logging.getLogger(__name__)

class ModelSelector:
    def __init__(
        self,
        problem_type: str,
        fixed_model: Optional[str] = None,
        n_splits: int = 5,
        n_jobs: int = -1
    ):
        self.problem_type = problem_type.lower()
        if self.problem_type not in ['classification', 'regression']:
            raise ValueError("problem_type must be either 'classification' or 'regression'")

        self.fixed_model = fixed_model
        self.n_splits = n_splits
        self.n_jobs = n_jobs  # For parallel processing

        self.best_model = None
        self.best_params = None
        self.best_score = None
        self.model_scores = {}
        self.feature_importance = pd.DataFrame()

        # Prioritize tree-based models first as they usually perform better
        self.tree_based_models = {
            'classification': ['RandomForest', 'XGBoost', 'LightGBM'],  # Removed CatBoost which is slower
            'regression': ['RandomForestRegressor', 'XGBRegressor', 'LGBMRegressor']
        }

        self.linear_models = {
            'classification': ['LogisticRegression'],  # Removed SVM which is slower
            'regression': ['LinearRegression']
        }

    def _get_model(self, trial: optuna.Trial, model_type: str) -> BaseEstimator:
        n_samples = self.X.shape[0]
        # Choose model parameters based on data size for faster training
        small_data = n_samples < 1000
        is_large_data = n_samples > 10000
        
        # Reduced estimator ranges for faster training
        est_range = (20, 100) if small_data else (50, 150)
        if is_large_data:
            est_range = (20, 80)  # Even fewer estimators for large datasets
            
        # Reduced depth ranges for faster training
        depth_range = (2, 6) if small_data else (3, 8)
        if is_large_data:
            depth_range = (2, 5)  # Smaller trees for large datasets
        
        # Add early stopping for iterative models
        early_stopping_rounds = 10

        if model_type == "LogisticRegression":
            return LogisticRegression(C=trial.suggest_float("lr_C", 0.01, 10, log=True), 
                                       max_iter=500, 
                                       n_jobs=self.n_jobs)
        elif model_type == "RandomForest":
            return RandomForestClassifier(n_estimators=trial.suggest_int("rf_n_estimators", *est_range),
                                           max_depth=trial.suggest_int("rf_max_depth", *depth_range), 
                                           min_samples_split=trial.suggest_int("rf_min_samples_split", 2, 10),
                                           random_state=42,
                                           n_jobs=self.n_jobs)
        elif model_type == "XGBoost":
            return XGBClassifier(n_estimators=trial.suggest_int("xgb_n_estimators", *est_range),
                                  learning_rate=trial.suggest_float("xgb_learning_rate", 0.01, 0.3, log=True),
                                  max_depth=trial.suggest_int("xgb_max_depth", *depth_range),
                                  use_label_encoder=False, 
                                  eval_metric='logloss', 
                                  random_state=42, 
                                  verbosity=0,
                                  n_jobs=self.n_jobs,
                                  early_stopping_rounds=early_stopping_rounds)
        elif model_type == "LightGBM":
            return LGBMClassifier(n_estimators=trial.suggest_int("lgb_n_estimators", *est_range),
                                  learning_rate=trial.suggest_float("lgb_learning_rate", 0.01, 0.3, log=True),
                                  max_depth=trial.suggest_int("lgb_max_depth", *depth_range), 
                                  random_state=42, 
                                  verbosity=-1,
                                  n_jobs=self.n_jobs)
        elif model_type == "LinearRegression":
            return LinearRegression(n_jobs=self.n_jobs)
        elif model_type == "RandomForestRegressor":
            return RandomForestRegressor(n_estimators=trial.suggest_int("rfr_n_estimators", *est_range),
                                          max_depth=trial.suggest_int("rfr_max_depth", *depth_range), 
                                          min_samples_split=trial.suggest_int("rfr_min_samples_split", 2, 10),
                                          random_state=42,
                                          n_jobs=self.n_jobs)
        elif model_type == "XGBRegressor":
            return XGBRegressor(n_estimators=trial.suggest_int("xgbr_n_estimators", *est_range),
                                 learning_rate=trial.suggest_float("xgbr_learning_rate", 0.01, 0.3, log=True),
                                 max_depth=trial.suggest_int("xgbr_max_depth", *depth_range), 
                                 random_state=42, 
                                 verbosity=0,
                                 n_jobs=self.n_jobs,
                                 early_stopping_rounds=early_stopping_rounds)
        elif model_type == "LGBMRegressor":
            return LGBMRegressor(n_estimators=trial.suggest_int("lgbr_n_estimators", *est_range),
                                  learning_rate=trial.suggest_float("lgbr_learning_rate", 0.01, 0.3, log=True),
                                  max_depth=trial.suggest_int("lgbr_max_depth", *depth_range), 
                                  random_state=42, 
                                  verbosity=-1,
                                  n_jobs=self.n_jobs)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def _objective(self, trial: optuna.Trial) -> float:
        available_models = self.tree_based_models[self.problem_type] + self.linear_models[self.problem_type]
        model_type = self.fixed_model or trial.suggest_categorical("model", available_models)

        # For large datasets, use a smaller number of folds to speed up evaluation
        n_splits = min(self.n_splits, 3) if self.X.shape[0] > 10000 else self.n_splits
        
        if self.problem_type == 'classification':
            kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        else:
            kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

        scores = []
        models = []

        # For very large datasets, use a sample for faster evaluation
        X = self.X
        y = self.y
        if X.shape[0] > 50000:
            # Sample 10% or 10,000 rows, whichever is larger
            sample_size = max(10000, int(X.shape[0] * 0.1))
            logger.info(f"Sampling {sample_size} rows from {X.shape[0]} for faster model selection")
            indices = np.random.choice(X.shape[0], sample_size, replace=False)
            X = X.iloc[indices]
            y = y.iloc[indices]

        for train_idx, val_idx in kf.split(X, y):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

            model = self._get_model(trial, model_type)
            
            # Use early stopping for supported models
            if model_type in ["XGBoost", "XGBRegressor"]:
                eval_set = [(X_val, y_val)]
                model.fit(X_train, y_train, eval_set=eval_set, verbose=False)
            elif model_type in ["LightGBM", "LGBMRegressor"]:
                eval_set = [(X_val, y_val)]
                model.fit(X_train, y_train, eval_set=eval_set, callbacks=[lightgbm.early_stopping(10)])
            else:
                model.fit(X_train, y_train)
                
            y_pred = model.predict(X_val)
            models.append(copy.deepcopy(model))

            score = f1_score(y_val, y_pred, average='weighted') if self.problem_type == 'classification' else -mean_squared_error(y_val, y_pred)
            scores.append(score)

        avg_score = np.mean(scores)
        if self.best_score is None or avg_score > self.best_score:
            self.best_score = avg_score
            self.best_model = models[np.argmax(scores)]
            self.best_params = trial.params

            if hasattr(self.best_model, 'feature_importances_'):
                self.feature_importance = pd.DataFrame({
                    'Feature': self.X.columns,
                    'Importance': self.best_model.feature_importances_
                }).sort_values('Importance', ascending=False)

        self.model_scores[model_type] = {
            'mean_score': avg_score,
            'params': trial.params
        }

        return avg_score

    def optimize(self, X: pd.DataFrame, y: pd.Series, n_trials: int = 100) -> Dict:
        """
        Optimize the model selection process.
        
        Args:
            X: Feature matrix
            y: Target vector
            n_trials: Number of trials for optimization
                
        Returns:
            Dict containing best score, best parameters, and model scores
        """
        self.X = X.reset_index(drop=True)
        self.y = y.reset_index(drop=True)
        
        # Adjust number of trials based on dataset size
        if X.shape[0] > 10000 or X.shape[1] > 50:
            n_trials = min(n_trials, 30)  # Reduce trials for large datasets
            
        # Create pruner to stop unpromising trials early
        pruner = optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=5)
        
        # Use TPESampler for more efficient parameter search
        sampler = optuna.samplers.TPESampler(seed=42)
        
        study = optuna.create_study(direction='maximize', pruner=pruner, sampler=sampler)
        
        # Use timeout to limit run time for large datasets
        timeout = None
        if X.shape[0] > 50000:
            timeout = 600  # 10 minutes
        
        # Run optimization
        study.optimize(
            lambda trial: self._objective(trial), 
            n_trials=n_trials,
            timeout=timeout,
            n_jobs=1  # Use 1 here as we're parallelizing inside the models
        )

        return {
            'best_score': study.best_value,
            'best_params': study.best_params,
            'model_scores': self.model_scores
        }

    def get_best_pipeline(self) -> Tuple[BaseEstimator, Dict]:
        if self.best_model is None:
            raise RuntimeError("Call optimize() before getting the best pipeline")
        return self.best_model, self.best_params

    def get_feature_importance(self) -> pd.DataFrame:
        if self.feature_importance.empty:
            raise RuntimeError("No feature importance available for the best model")
        return self.feature_importance.copy()
