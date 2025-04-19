import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
from scipy.spatial.distance import cdist
import math
import logging
import warnings
from typing import Dict, Optional, Union, List
from automl.utils import DataFrameAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AutoML.Preprocessor')

class Preprocessor:
    """
    A class for handling missing values in a DataFrame using various strategies.
    
    Strategies:
    1. Drop features with too many nulls (>30% by default)
    2. KNN imputation for features with moderate nulls (5-30% by default)
    3. Statistical imputation for features with few nulls (<5% by default)
        - Mode for categorical and ordinal features
        - Mean for normal numerical features
        - Median for skewed numerical features
    """
    
    def __init__(self, drop_threshold: float = 30.0, knn_threshold: float = 5.0, 
                 ordinal_ratio: float = 0.05, keep: str = 'first'):
        """
        Initialize the Preprocessor.
        
        Parameters:
        -----------
        drop_threshold : float, default=30.0
            Percentage of nulls above which to drop a feature
        knn_threshold : float, default=5.0
            Percentage of nulls above which to use KNN imputation
        ordinal_ratio : float, default=0.05
            Maximum ratio of unique values to total values for a numeric feature 
            to be considered ordinal
        keep : str, default='first'
            Which duplicates to keep {'first', 'last', False}
            - 'first': Keep first occurrence of duplicate
            - 'last': Keep last occurrence of duplicate
            - False: Drop all duplicates
        """
        self.descriptor = None
        self.drop_threshold = drop_threshold
        self.knn_threshold = knn_threshold
        self.ordinal_ratio = ordinal_ratio
        self.keep = keep
        self.analyzer = DataFrameAnalyzer()
        logger.info(f"Initialized Preprocessor with drop_threshold={drop_threshold}, "
                   f"knn_threshold={knn_threshold}, ordinal_ratio={ordinal_ratio}, "
                   f"keep={keep}")
        self.df = None
    
    def generate_descriptor(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a descriptor DataFrame containing information about null values 
        and feature types.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input DataFrame
            
        Returns:
        --------
        pandas.DataFrame
            Descriptor DataFrame with columns:
            - null_count: Number of null values
            - null_percentage: Percentage of null values
            - is_numeric: Whether the feature is numeric
        """
        descriptor = pd.DataFrame({
            'null_count': df.isnull().sum(),
            'null_percentage': round(df.isnull().sum() / len(df) * 100, 2),
            'is_numeric': [np.issubdtype(dtype, np.number) for dtype in df.dtypes]
        })
        return descriptor
    
    def knn_impute(self, df: pd.DataFrame, feature: str) -> None:
        """
        Impute missing values using KNN based on other complete numeric features.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame to impute
        feature : str
            Feature name to impute
        """
        # Get numeric features with no nulls (excluding IDs)
        neighbor_features = [
            col for col in df.columns 
            if col != feature 
            and self.descriptor.loc[col, 'null_count'] == 0
            and self.descriptor.loc[col, 'is_numeric']
            and not self.analyzer.is_id_column(df[col])
        ]
        
        if not neighbor_features:
            logger.warning(f"No suitable neighbor features found for KNN imputation of {feature}. "
                         "Falling back to mode imputation.")
            df[feature] = df[feature].fillna(df[feature].mode().iloc[0])
            return
            
        # Prepare data for KNN
        neighbor_df = df[neighbor_features]
        non_null_mask = df[feature].notna()
        non_null = neighbor_df[non_null_mask]
        null = neighbor_df[~non_null_mask]
        
        # Normalize features
        norm_min = neighbor_df.min()
        norm_range = neighbor_df.max() - neighbor_df.min()
        norm_range = norm_range.replace(0, 1e-9)  # Avoid division by zero
        
        non_null_norm = (non_null - norm_min) / norm_range
        null_norm = (null - norm_min) / norm_range
        
        # Calculate distances and find k nearest neighbors
        distances = pd.DataFrame(cdist(null_norm, non_null_norm, metric='euclidean'))
        k = min(int(math.ceil(math.sqrt(len(non_null)))), len(non_null))
        k_nearest = pd.DataFrame(np.argsort(distances, axis=1)).iloc[:, :k]
        
        # Impute values
        for null_idx, df_idx in enumerate(null.index):
            neighbor_indices = non_null.iloc[k_nearest.iloc[null_idx]].index
            neighbor_values = df.loc[neighbor_indices, feature]
            
            # Use mean for continuous numeric, mode for categorical/ordinal
            if (self.descriptor.loc[feature, 'is_numeric'] and 
                df[feature].nunique() / len(df) > self.ordinal_ratio):
                df.loc[df_idx, feature] = neighbor_values.mean()
            else:
                df.loc[df_idx, feature] = neighbor_values.mode().iloc[0]
    
    def replace_by_null(self, df: pd.DataFrame, null_character: Union[str, int, Dict[str, Union[str, int]]]) -> pd.DataFrame:
        """
        Replace specified null character(s) with NaN.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input DataFrame
        null_character : str, int, or dict
            Character(s) to replace with NaN. Can be:
            - A single value (str or int) to use for all columns
            - A dictionary mapping column names to their specific null characters
            
        Returns:
        --------
        pandas.DataFrame
            DataFrame with null character(s) replaced by NaN
        """
        df = df.copy()
        
        if isinstance(null_character, dict):
            # Handle dictionary of null characters
            for col, null_val in null_character.items():
                if col in df.columns:
                    if isinstance(null_val, str):
                        df[col] = df[col].replace(null_val, np.nan)
                    else:
                        try:
                            df[col] = df[col].replace(float(null_val), np.nan)
                        except (ValueError, TypeError):
                            # Skip if we can't convert the null_character to float
                            continue
        else:
            # Handle single null character for all columns
            for feature in df.columns:
                if isinstance(null_character, str):
                    df[feature] = df[feature].replace(null_character, np.nan)
                else:
                    try:
                        df[feature] = df[feature].replace(float(null_character), np.nan)
                    except (ValueError, TypeError):
                        # Skip if we can't convert the null_character to float
                        continue
        return df
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from the DataFrame.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input DataFrame
        subset : list of str, optional
            Column labels to consider for identifying duplicates. 
            If None, use all columns.
            
        Returns:
        --------
        pandas.DataFrame
            DataFrame with duplicates removed
        """
        initial_rows = len(df)
        df = df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=subset, keep=self.keep)
        
        # Log results
        removed_rows = initial_rows - len(df)
        if removed_rows > 0:
            if subset:
                logger.info(f"Removed {removed_rows} duplicate rows based on columns: {subset}")
            else:
                logger.info(f"Removed {removed_rows} exact duplicate rows")
        else:
            logger.info("No duplicates found")
            
        return df
    
    def fill_null(self, df: pd.DataFrame, null_character: Optional[Union[str, int]] = None) -> pd.DataFrame:
        """
        Fill null values in the DataFrame using various strategies.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input DataFrame
        null_character : str or int, optional
            Character to be treated as null
            
        Returns:
        --------
        pandas.DataFrame
            DataFrame with null values handled and optionally duplicates removed
        """
        df = df.copy()
        if null_character is not None:
            df = self.replace_by_null(df, null_character)
        
        self.descriptor = self.generate_descriptor(df)
        logger.info(f"Starting null value handling for {len(df.columns)} features")

        # Set the instance df attribute
        self.df = df

        # Get the graphs of missing values
        self.get_graphs()

        # First identify columns to drop
        columns_to_drop = []
        for feature in self.descriptor.index:
            null_pct = self.descriptor.loc[feature, 'null_percentage']
            if null_pct > self.drop_threshold:
                logger.info(f"Dropping feature '{feature}' with {null_pct:.1f}% nulls")
                columns_to_drop.append(feature)
        
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            self.descriptor = self.generate_descriptor(df)
        
        # Then handle remaining nulls
        for feature in self.descriptor.index:
            null_pct = self.descriptor.loc[feature, 'null_percentage']
            
            # Skip features with no nulls
            if null_pct == 0:
                continue
                
            logger.info(f"Handling nulls in feature '{feature}' ({null_pct:.1f}%)")
            
            # Use KNN for moderate number of nulls
            if null_pct > self.knn_threshold:
                logger.info(f"Using KNN imputation for '{feature}'")
                self.knn_impute(df, feature)
                
            # Use statistical methods for few nulls
            else:
                if self.descriptor.loc[feature, 'is_numeric']:
                    # Check if ordinal
                    if df[feature].nunique() / len(df) < self.ordinal_ratio:
                        logger.info(f"Using mode imputation for ordinal feature '{feature}'")
                        df[feature] = df[feature].fillna(df[feature].mode().iloc[0])
                    # Check distribution
                    elif self.analyzer.check_distribution(df[feature].dropna()) == 'normal':
                        logger.info(f"Using mean imputation for normal feature '{feature}'")
                        df[feature] = df[feature].fillna(df[feature].mean())
                    else:
                        logger.info(f"Using median imputation for skewed feature '{feature}'")
                        df[feature] = df[feature].fillna(df[feature].median())
                else:
                    logger.info(f"Using mode imputation for categorical feature '{feature}'")
                    df[feature] = df[feature].fillna(df[feature].mode().iloc[0])
        
        # Final check for nulls
        remaining_nulls = df.isnull().sum().sum()
        if remaining_nulls > 0:
            logger.warning(f"There are still {remaining_nulls} null values in the dataset")
        else:
            logger.info("Successfully handled all null values")
    
        return df

    def get_graphs(self, show: bool = True) -> None:
        """
        Generate graphs to visualize missing values and distributions of features.
        
        Parameters:
        -----------
        show : bool, default=True
            Whether to display the graphs or not

        Returns:
        --------
        None
        """
        df = self.df  # Access df from instance attribute

        # Plotting missing values as heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Values Heatmap')
        if show:
            plt.show()

        # Plotting missing values by feature
        null_percentage = df.isnull().mean() * 100
        null_percentage = null_percentage[null_percentage > 0].sort_values(ascending=False)

        if null_percentage.empty:
            logger.info("No missing values to plot.")
            return

        plt.figure(figsize=(12, 6))
        null_percentage.plot(kind='bar', color='lightblue')
        plt.title('Missing Values Percentage by Feature')
        plt.xlabel('Features')
        plt.ylabel('Percentage of Missing Values')
        if show:
            plt.show()


        # Plotting distribution of numerical features with null values
        numeric_features = df.select_dtypes(include=[np.number]).columns
        for feature in numeric_features:
            if df[feature].isnull().sum() > 0:
                plt.figure(figsize=(12, 6))
                sns.histplot(df[feature].dropna(), kde=True, color='blue')
                plt.title(f'Distribution of {feature}')
                plt.xlabel(feature)
                plt.ylabel('Frequency')
                if show:
                    plt.show()

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fit and transform the DataFrame in one step.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input DataFrame
        
        Returns:
        --------
        pd.DataFrame
            Cleaned DataFrame
        """
        self.df = df
        return self.fill_null(df)
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Concatenating train, validation, and test data")
        full_df = pd.concat(
            [self.df, df],
            axis=0
        ).reset_index(drop=True)
        
        # Step 2: Apply preprocessing
        logger.info("Applying preprocessing to concatenated data")
        full_df_cleaned = self.fill_null(full_df)
        
        # Step 3: Extract cleaned test data
        logger.info("Extracting cleaned test data")
        total_train_len = len(self.df)
        X_test_cleaned = full_df_cleaned.iloc[total_train_len:].reset_index(drop=True)
        return X_test_cleaned
