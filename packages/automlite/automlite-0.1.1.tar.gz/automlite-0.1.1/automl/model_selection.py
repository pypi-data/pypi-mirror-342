import numpy as np
import pandas as pd
import copy
import optuna
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

class ModelSelector:
    def __init__(
        self,
        problem_type: str,
        fixed_model: Optional[str] = None,
        n_splits: int = 5
    ):
        self.problem_type = problem_type.lower()
        if self.problem_type not in ['classification', 'regression']:
            raise ValueError("problem_type must be either 'classification' or 'regression'")

        self.fixed_model = fixed_model
        self.n_splits = n_splits

        self.best_model = None
        self.best_params = None
        self.best_score = None
        self.model_scores = {}
        self.feature_importance = pd.DataFrame()

        self.tree_based_models = {
            'classification': ['RandomForest', 'XGBoost', 'LightGBM', 'CatBoost'],
            'regression': ['RandomForestRegressor', 'XGBRegressor', 'LGBMRegressor', 'CatBoostRegressor']
        }

        self.linear_models = {
            'classification': ['LogisticRegression', 'SVM'],
            'regression': ['LinearRegression', 'SVR']
        }

    def _get_model(self, trial: optuna.Trial, model_type: str) -> BaseEstimator:
        n_samples = self.X.shape[0]
        small_data = n_samples < 1000
        est_range = (50, 150) if small_data else (50, 300)
        depth_range = (3, 8) if small_data else (3, 15)

        if model_type == "LogisticRegression":
            return LogisticRegression(C=trial.suggest_float("lr_C", 0.01, 10, log=True), max_iter=1000)
        elif model_type == "RandomForest":
            return RandomForestClassifier(n_estimators=trial.suggest_int("rf_n_estimators", *est_range),
                                           max_depth=trial.suggest_int("rf_max_depth", *depth_range), random_state=42)
        elif model_type == "XGBoost":
            return XGBClassifier(n_estimators=trial.suggest_int("xgb_n_estimators", *est_range),
                                  learning_rate=trial.suggest_float("xgb_learning_rate", 0.01, 0.3, log=True),
                                  max_depth=trial.suggest_int("xgb_max_depth", *depth_range),
                                  use_label_encoder=False, eval_metric='logloss', random_state=42, verbosity=0)
        elif model_type == "LightGBM":
            return LGBMClassifier(n_estimators=trial.suggest_int("lgb_n_estimators", *est_range),
                                  learning_rate=trial.suggest_float("lgb_learning_rate", 0.01, 0.3, log=True),
                                  max_depth=trial.suggest_int("lgb_max_depth", *depth_range), random_state=42, verbosity=-1)
        elif model_type == "CatBoost":
            return CatBoostClassifier(n_estimators=trial.suggest_int("cat_n_estimators", *est_range),
                                      depth=trial.suggest_int("cat_depth", *depth_range),
                                      learning_rate=trial.suggest_float("cat_learning_rate", 0.01, 0.3, log=True),
                                      random_state=42, verbose=0)
        elif model_type == "SVM":
            return SVC(C=trial.suggest_float("svm_C", 0.01, 10, log=True), random_state=42, probability=True)
        elif model_type == "LinearRegression":
            return LinearRegression()
        elif model_type == "RandomForestRegressor":
            return RandomForestRegressor(n_estimators=trial.suggest_int("rfr_n_estimators", *est_range),
                                          max_depth=trial.suggest_int("rfr_max_depth", *depth_range), random_state=42)
        elif model_type == "XGBRegressor":
            return XGBRegressor(n_estimators=trial.suggest_int("xgbr_n_estimators", *est_range),
                                 learning_rate=trial.suggest_float("xgbr_learning_rate", 0.01, 0.3, log=True),
                                 max_depth=trial.suggest_int("xgbr_max_depth", *depth_range), random_state=42, verbosity=0)
        elif model_type == "LGBMRegressor":
            return LGBMRegressor(n_estimators=trial.suggest_int("lgbr_n_estimators", *est_range),
                                  learning_rate=trial.suggest_float("lgbr_learning_rate", 0.01, 0.3, log=True),
                                  max_depth=trial.suggest_int("lgbr_max_depth", *depth_range), random_state=42, verbosity=-1)
        elif model_type == "CatBoostRegressor":
            return CatBoostRegressor(n_estimators=trial.suggest_int("catr_n_estimators", *est_range),
                                      depth=trial.suggest_int("catr_depth", *depth_range),
                                      learning_rate=trial.suggest_float("catr_learning_rate", 0.01, 0.3, log=True),
                                      random_state=42, verbose=0)
        elif model_type == "SVR":
            return SVR(C=trial.suggest_float("svr_C", 0.01, 10, log=True))
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def _objective(self, trial: optuna.Trial) -> float:
        available_models = self.tree_based_models[self.problem_type] + self.linear_models[self.problem_type]
        model_type = self.fixed_model or trial.suggest_categorical("model", available_models)

        if self.problem_type == 'classification':
            kf = StratifiedKFold(n_splits=self.n_splits, shuffle=True, random_state=42)
        else:
            kf = KFold(n_splits=self.n_splits, shuffle=True, random_state=42)

        scores = []
        models = []

        for train_idx, val_idx in kf.split(self.X, self.y):
            X_train, X_val = self.X.iloc[train_idx], self.X.iloc[val_idx]
            y_train, y_val = self.y.iloc[train_idx], self.y.iloc[val_idx]

            model = self._get_model(trial, model_type)
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
        self.X = X.reset_index(drop=True)
        self.y = y.reset_index(drop=True)

        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: self._objective(trial), n_trials=n_trials)

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
