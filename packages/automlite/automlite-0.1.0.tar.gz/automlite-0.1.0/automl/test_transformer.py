import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TestTransformer:
    """
    A class to handle test data transformation through the entire AutoML pipeline.
    
    This transformer ensures that test data goes through the same preprocessing steps
    as training data, while preventing data leakage. It handles:
    1. Concatenated preprocessing for consistent null handling
    2. Encoding using global encoders
    3. Scaling with fitted scalers
    4. Feature selection using training features
    5. Dimensionality reduction using learned components
    
    Attributes
    ----------
    preprocessor : Preprocessor
        Preprocessor instance fitted on training data
    input_encoder : InputEncoder
        Input encoder instance fitted on training data
    output_encoder : OutputEncoder
        Output encoder instance fitted on training data
    scaler : AutoScaler
        Scaler instance fitted on training data
    feature_selector : FeatureSelector
        Feature selector instance fitted on training data
    dim_reducer : DimensionalityReducer
        Dimensionality reducer instance fitted on training data
    problem_type : str
        Type of problem ('classification' or 'regression')
    """
    
    def __init__(
        self,
        preprocessor,
        input_encoder,
        output_encoder,
        scaler,
        feature_selector,
        dim_reducer,
        problem_type: str
    ):
        """
        Initialize the TestTransformer.
        
        Parameters
        ----------
        preprocessor : Preprocessor
            Fitted preprocessor instance
        input_encoder : InputEncoder
            Fitted input encoder instance
        output_encoder : OutputEncoder
            Fitted output encoder instance
        scaler : AutoScaler
            Fitted scaler instance
        feature_selector : FeatureSelector
            Fitted feature selector instance
        dim_reducer : DimensionalityReducer
            Fitted dimensionality reducer instance
        problem_type : str
            Type of problem ('classification' or 'regression')
        """
        self.preprocessor = preprocessor
        self.input_encoder = input_encoder
        self.output_encoder = output_encoder
        self.scaler = scaler
        self.feature_selector = feature_selector
        self.dim_reducer = dim_reducer
        self.problem_type = problem_type.lower()
        
        logger.info(
            f"Initialized TestTransformer for {self.problem_type} problem"
        )
        
    def transform(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_test: Optional[pd.Series] = None
    ) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """
        Transform test data using fitted pipeline components.
        
        Parameters
        ----------
        X_train : pd.DataFrame
            Training features used to fit the pipeline
        
        X_test : pd.DataFrame
            Test features to transform
        y_test : pd.Series, optional
            Test target values if available
            
        Returns
        -------
        Tuple[pd.DataFrame, Optional[pd.Series]]
            X_test_transformed : Transformed test features
            y_test_transformed : Transformed test target (if provided)
            
        Notes
        -----
        The transformation process:
        1. Concatenates train and test data for consistent preprocessing
        2. Applies preprocessing (null handling, etc.)
        3. Extracts cleaned test data
        4. Applies remaining transformations using test_transform methods
        """
        logger.info("Starting test data transformation")
        
        # Verify input data types
        if not isinstance(X_test, pd.DataFrame):
            raise TypeError("X_test must be a pandas DataFrame")
        if y_test is not None and not isinstance(y_test, pd.Series):
            raise TypeError("y_test must be a pandas Series")
            
        # Step 1: Concatenate all data
        logger.info("Concatenating train and test data")
        full_df = pd.concat(
            [X_train, X_test],
            axis=0
        ).reset_index(drop=True)
        
        # Step 2: Apply preprocessing
        logger.info("Applying preprocessing to concatenated data")
        full_df_cleaned = self.preprocessor.fill_null(full_df)
        
        # Step 3: Extract cleaned test data
        logger.info("Extracting cleaned test data")
        total_train_len = len(X_train)
        X_test_cleaned = full_df_cleaned.iloc[total_train_len:].reset_index(drop=True)
        
        # Step 4: Apply input encoding
        logger.info("Applying input encoding to test data")
        X_test_encoded = self.input_encoder.transform(X_test_cleaned)
        
        # Step 5: Apply scaling
        logger.info("Applying scaling to test data")
        X_test_scaled = self.scaler.transform(X_test_encoded)
        
        # Step 6: Apply feature selection
        logger.info("Applying feature selection to test data")
        X_test_selected = self.feature_selector.transform(X_test_scaled)
        
        # Step 7: Apply dimensionality reduction
        logger.info("Applying dimensionality reduction to test data")
        X_test_final = self.dim_reducer.transform(X_test_selected)
        
        # Handle test target if provided
        y_test_transformed = None
        if y_test is not None:
            if self.problem_type == 'classification':
                logger.info("Transforming test target variable")
                y_test_transformed = self.output_encoder.transform(y_test)
            else:
                logger.info("Skipping target transformation for regression")
            
        logger.info("Test data transformation completed")
        return X_test_final, y_test_transformed
        
    def inverse_transform_target(self, y_pred: np.ndarray) -> pd.Series:
        """
        Convert encoded predictions back to original target format.
        
        Parameters
        ----------
        y_pred : np.ndarray
            Encoded predictions from the model
            
        Returns
        -------
        pd.Series
            Predictions in original target format
            
        Raises
        ------
        ValueError
            If problem is classification but output encoder not fitted
        """
        if self.problem_type == 'classification':
            logger.info("Converting predictions to original target format")
            return self.output_encoder.inverse_transform(y_pred)
        else:
            logger.info("Returning predictions as is for regression")
            return pd.Series(y_pred)
