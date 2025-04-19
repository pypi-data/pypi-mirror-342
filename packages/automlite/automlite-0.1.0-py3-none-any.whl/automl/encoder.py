import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import logging

# Configure logging
logger = logging.getLogger(__name__)

class InputEncoder:
    def __init__(self, encoding_method='auto', max_categories=10, random_state=42):
        self.encoding_method = encoding_method
        self.max_categories = max_categories
        self.random_state = random_state
        self.fitted = False
        self.encoders = {}
        self.categorical_columns = []
        self.target_features = None

    def _get_encoder(self, col_name, n_unique):
        if self.encoding_method == 'label':
            return LabelEncoder()
        elif self.encoding_method == 'onehot':
            return OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        else:
            if n_unique <= self.max_categories:
                return OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            return LabelEncoder()

    def fit(self, X, y=None):
        self.categorical_columns = []
        self.encoders = {}
        self.target_features = []

        for col in X.columns:
            if pd.api.types.is_object_dtype(X[col]) or isinstance(X[col].dtype, pd.CategoricalDtype):
                self.categorical_columns.append(col)
                self.target_features.append(col)
                n_unique = X[col].nunique()
                encoder = self._get_encoder(col, n_unique)
                if isinstance(encoder, OneHotEncoder):
                    encoder.fit(X[[col]])
                else:
                    encoder.fit(X[col])
                self.encoders[col] = encoder
                logger.info(f"Encoding feature '{col}' using {'OneHotEncoder' if isinstance(encoder, OneHotEncoder) else 'LabelEncoder'}")

        self.fitted = True
        return self

    def transform(self, X):
        if not self.fitted:
            raise ValueError("Encoder must be fitted before transform")

        missing = set(self.target_features or []) - set(X.columns)
        if missing:
            raise ValueError(f"Input data is missing some categorical features: {missing}")

        X_encoded = X.copy()

        for col in self.categorical_columns:
            encoder = self.encoders[col]

            if isinstance(encoder, OneHotEncoder):
                encoded = encoder.transform(X[[col]])
                feature_names = [f"{col}_{val}" for val in encoder.categories_[0]]
                encoded_df = pd.DataFrame(encoded, columns=feature_names, index=X.index)

                # Add missing columns (in test) as zeros
                for feature in self.encoders[col].categories_[0]:
                    name = f"{col}_{feature}"
                    if name not in encoded_df.columns:
                        encoded_df[name] = 0

                # Ensure order of columns is consistent
                encoded_df = encoded_df[[f"{col}_{val}" for val in encoder.categories_[0]]]

                X_encoded = X_encoded.drop(columns=[col])
                X_encoded = pd.concat([X_encoded, encoded_df], axis=1)

            else:  # LabelEncoder
                def safe_transform(val):
                    return encoder.transform([val])[0] if val in encoder.classes_ else -1
                X_encoded[col] = X_encoded[col].map(safe_transform)

        return X_encoded

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


class OutputEncoder:
    def __init__(self, task_type='classification'):
        self.task_type = task_type
        self.fitted = False
        self.encoder = None
        self.encoding_map = {}

    def fit(self, y):
        y = pd.Series(y)
        if self.task_type == 'classification' and not pd.api.types.is_numeric_dtype(y):
            self.encoder = LabelEncoder()
            self.encoder.fit(y)
            self.encoding_map = dict(zip(self.encoder.classes_, self.encoder.transform(self.encoder.classes_)))
        self.fitted = True
        return self

    def transform(self, y):
        y = pd.Series(y)
        if not self.fitted:
            return y

        if self.task_type == 'classification' and self.encoder:
            def safe_transform(val):
                return self.encoder.transform([val])[0] if val in self.encoder.classes_ else -1
            return y.map(safe_transform).astype(np.int64)

        return y

    def inverse_transform(self, y):
        y = pd.Series(y)
        if not self.fitted:
            raise ValueError("Encoder must be fitted before inverse_transform")
        if self.task_type == 'classification' and self.encoder:
            return pd.Series(self.encoder.inverse_transform(y), index=y.index)
        return y

    def get_encoding_map(self):
        if not self.fitted:
            raise ValueError("Encoder must be fitted before getting encoding map")
        return self.encoding_map.copy()

    def fit_transform(self, y):
        self.fit(y)
        return self.transform(y)
