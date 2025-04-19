import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import logging
import copy

from automl.preprocessor import Preprocessor
from automl.outliers import OutlierHandler
from automl.encoder import InputEncoder
from automl.encoder import OutputEncoder
from automl.scaler import AutoScaler
from automl.feature_selection import FeatureSelector
from automl.dimensionality_reduction import DimensionalityReducer
from automl.model_selection import ModelSelector
from automl.evaluator import Evaluator
from automl.test_transformer import TestTransformer
from automl.feature_importance import FeatureImportance

logger = logging.getLogger(__name__)

class AutoML:
    def __init__(self, target_column: str, test_size: float = 0.2, random_state: int = 42):
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.problem_type = None
        self.test_transformer = None

    def fit(self, df_train: pd.DataFrame, df_test: pd.DataFrame = None, n_trials: int = 30):
        if self.target_column not in df_train.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in training data.")

        X_trainval = df_train.drop(columns=[self.target_column])
        y_trainval = df_train[self.target_column]

        # Task inference
        if self.problem_type is None:
            self.problem_type = 'classification' if y_trainval.nunique() < 10 else 'regression'

        X_test, y_test = None, None
        if df_test is not None:
            if self.target_column in df_test.columns:
                # Case 1: test set has target => use for evaluation
                X_train, y_train = X_trainval, y_trainval
                X_val = df_test.drop(columns=[self.target_column])
                y_val = df_test[self.target_column]
                X_trainval = pd.concat([X_train, X_val], ignore_index=True)
                y_trainval = pd.concat([y_train, y_val], ignore_index=True)
                X_test, y_test = X_val.copy(), y_val.copy()
            else:
                # Case 2: test set has no target => keep for prediction only
                X_train, X_val, y_train, y_val = train_test_split(
                    X_trainval, y_trainval,
                    test_size=self.test_size,
                    stratify=y_trainval if self.problem_type == 'classification' else None,
                    random_state=self.random_state
                )
                X_test = df_test.copy()
        else:
            # Case 3: no test set provided
            X_train, X_val, y_train, y_val = train_test_split(
                X_trainval, y_trainval,
                test_size=self.test_size,
                stratify=y_trainval if self.problem_type == 'classification' else None,
                random_state=self.random_state
            )

        # === PIPELINE ===
        preprocessor = Preprocessor()
        X_train_cleaned = preprocessor.fit_transform(X_train)
        
        outlier_handler = OutlierHandler(X_train_cleaned, X_val, y_train, y_val, self.problem_type)
        X_train_handled, X_val_handled, y_train_handled, y_val_handled = outlier_handler.handle_outliers()

        input_encoder = InputEncoder(encoding_method='auto')
        X_train_encoded = input_encoder.fit_transform(X_train_handled)
        
        output_encoder = OutputEncoder()
        y_train_encoded = output_encoder.fit_transform(y_train_handled)
        
        scaler = AutoScaler()
        X_train_scaled = scaler.fit_transform(X_train_encoded)
        
        feature_selector = FeatureSelector(self.problem_type)
        X_train_selected = feature_selector.fit_transform(X_train_scaled, y_train_encoded)
        
        dim_reducer = DimensionalityReducer(task_type=self.problem_type)
        X_train_final = dim_reducer.fit_transform(X_train_selected, y_train_encoded)
        print(X_train_final.columns)

        # === MODEL SELECTION ===
        model_selector = ModelSelector(problem_type=self.problem_type)
        model_selector.optimize(X_train_final, y_train_encoded, n_trials=n_trials)

        self.model, self.best_params = model_selector.get_best_pipeline()

        # === TEST TRANSFORMATION ===
        self.test_transformer = TestTransformer(
            preprocessor, input_encoder, output_encoder,
            scaler, feature_selector, dim_reducer,
            problem_type=self.problem_type
        )

        self.X_train = X_train
        self.X_val = X_val
        self.X_test = X_test
        self.y_test = y_test

        # === EVALUATION ===
        self.evaluator = Evaluator(self.problem_type, self.test_transformer)
        if y_test is not None:
            self.metrics = self.evaluator.evaluate(self.model, X_train, X_test, y_test)
        else:
            self.metrics = self.evaluator.evaluate(self.model, X_train, X_val, y_val)

        # === FEATURE IMPORTANCE ===
        X_trainval_cleaned = preprocessor.fill_null(X_trainval)
        X_encoded_trainval = input_encoder.transform(X_trainval_cleaned)
        X_scaled_trainval = scaler.transform(X_encoded_trainval)
        X_selected_trainval = feature_selector.transform(X_scaled_trainval)

        # Use a cloned model for feature importance to avoid mutating the real one
        shap_model = copy.deepcopy(self.model)

        self.feature_importance = FeatureImportance(shap_model, self.problem_type)
        self.feature_importance.fit(X_selected_trainval, y_trainval)
        self.importance_df = self.feature_importance.compute_importance(X_selected_trainval)

        self.metrics["feature_importance"] = self.importance_df

        return self

    def predict(self, X_new: pd.DataFrame) -> np.ndarray:
        X_new_transformed, _ = self.test_transformer.transform(
            self.X_train, X_new, None
        )
        return self.model.predict(X_new_transformed)

    def evaluate(self):
        return self.metrics

    def plot_feature_importance(self):
        return self.feature_importance.plot_importance()

    def print_report(self):
        self.evaluator.print_report()

    def create_csv(self, df_original: pd.DataFrame, predictions, columns_to_include: list, output_path: str, include_index: bool = False):
        """
        Generate a CSV file with selected columns from df_original and the predictions.

        Parameters:
            df_original (pd.DataFrame): Original test dataframe
            predictions (array-like): Predictions to add
            columns_to_include (list): List of column names from df_original to include
            output_path (str): Path to save the CSV file
            include_index (bool): Whether to include the index in the CSV
        """
        result_df = df_original[columns_to_include].copy()
        result_df[self.target_column] = predictions
        result_df.to_csv(output_path, index=include_index)
        print(f"\n✅ Predictions saved to {output_path}")
