import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional
import logging
from scipy.stats import shapiro, ks_2samp, norm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AutoML.Utils')

class DataFrameAnalyzer:
    """
    Utility class for analyzing pandas DataFrames and generating data quality reports.
    Provides methods for:
    - Basic data profiling
    - Column type detection
    - Missing value analysis
    - Distribution analysis
    """
    
    def __init__(self):
        """Initialize the DataFrameAnalyzer."""
        self.categorical_threshold = 10  # Max unique values for categorical
        self.datetime_formats = [
            '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M:%S'
        ]
    
    def check_distribution(self, series: pd.Series) -> str:
        """
        Check if a numeric series follows a normal distribution.
        Uses skewness for quick check, then Shapiro-Wilk or KS test based on sample size.
        
        Parameters:
        -----------
        series : pandas.Series
            The numeric series to check
            
        Returns:
        --------
        str
            'normal' or 'skewed'
        """
        if not is_numeric_dtype(series.dtype):
            return "skewed"
            
        # Quick check using skewness
        if abs(series.skew()) < 0.5:
            return "normal"
            
        # For larger samples, use KS test instead of Shapiro
        if series.shape[0] < 5000:
            stat, p = shapiro(series)
        else:
            mu, sigma = series.mean(), series.std()
            stat, p = ks_2samp(series, norm.rvs(loc=mu, scale=sigma, size=len(series)))
            
        return "normal" if p > 0.05 else "skewed"
    
    def get_column_types(
        self, 
        df: pd.DataFrame, 
        categorical_threshold: Optional[int] = None,
        exclude_columns: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Categorize columns by their data types.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input dataframe
        categorical_threshold : int, optional
            Maximum number of unique values for a numeric column to be considered categorical
        exclude_columns : List[str], optional
            Columns to exclude from analysis
            
        Returns:
        --------
        Dict[str, List[str]]
            Dictionary with column types as keys and lists of column names as values
        """
        if categorical_threshold is None:
            categorical_threshold = self.categorical_threshold
            
        exclude_columns = exclude_columns or []
        columns = [col for col in df.columns if col not in exclude_columns]
        
        column_types = {
            'numeric': [],
            'categorical': [],
            'datetime': [],
            'text': []
        }
        
        for column in columns:
            # Skip excluded columns
            if column in exclude_columns:
                continue
                
            # Get series
            series = df[column]
            dtype = series.dtype
            
            # Check for ID columns first
            if self.is_id_column(series):
                # Add ID columns to categorical type
                if column != 'id':  # Exclude the primary 'id' column
                    column_types['categorical'].append(column)
                continue
            
            # Check for datetime
            if dtype == 'datetime64[ns]':
                column_types['datetime'].append(column)
                continue
                
            if dtype == 'object':
                # Try to convert to datetime
                is_datetime = False
                if series.notna().any():
                    sample = series[series.notna()].iloc[0]
                    for date_format in self.datetime_formats:
                        try:
                            pd.to_datetime(sample, format=date_format)
                            is_datetime = True
                            break
                        except (ValueError, TypeError):
                            continue
                
                if is_datetime:
                    column_types['datetime'].append(column)
                    continue
                
                # Check if text
                if series.str.len().max() > 50:
                    column_types['text'].append(column)
                else:
                    column_types['categorical'].append(column)
                continue
            
            # Handle numeric types
            if np.issubdtype(dtype, np.number):
                unique_count = series.nunique()
                if unique_count <= categorical_threshold:
                    column_types['categorical'].append(column)
                else:
                    column_types['numeric'].append(column)
                continue
            
            # Default to categorical
            column_types['categorical'].append(column)
        
        return column_types
    
    def generate_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate a comprehensive summary of the dataframe.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input dataframe
            
        Returns:
        --------
        Dict
            Dictionary containing various summary statistics and information
        """
        summary = {
            'basic_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
            },
            'missing_data': {
                'total_missing': df.isnull().sum().sum(),
                'columns_with_missing': df.isnull().sum()[df.isnull().sum() > 0].to_dict()
            },
            'column_types': self.get_column_types(df),
            'numeric_stats': {},
            'categorical_stats': {}
        }
        
        # Get numeric and categorical columns
        numeric_cols = summary['column_types']['numeric']
        categorical_cols = summary['column_types']['categorical']
        
        # Generate numeric statistics
        for col in numeric_cols:
            summary['numeric_stats'][col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'skew': df[col].skew(),
                'unique_values': df[col].nunique(),
                'distribution': self.check_distribution(df[col])
            }
        
        # Generate categorical statistics
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            summary['categorical_stats'][col] = {
                'unique_values': len(value_counts),
                'top_values': value_counts.head(5).to_dict(),
                'null_count': df[col].isnull().sum()
            }
        
        return summary
    
    def is_id_column(self, series: pd.Series) -> bool:
        """
        Check if a series is likely to be an ID column.
        
        Parameters:
        -----------
        series : pandas.Series
            The series to check
            
        Returns:
        --------
        bool
            True if the series is likely an ID column
        """
        # Check column name first
        col_name = series.name.lower() if series.name else ""
        common_id_names = ['id', 'key', 'num', 'code', 'emp', 'user', 'cust']
        if any(id_name in col_name for id_name in common_id_names):
            # For numeric columns with ID in name, check uniqueness
            if is_numeric_dtype(series.dtype):
                return series.nunique() == len(series)
            # For string columns with ID in name, check pattern consistency
            elif series.dtype == 'object':
                if series.notna().all():  # All values should be non-null
                    # Check if all values follow a consistent pattern (e.g., EMP0001, EMP0002)
                    pattern_match = series.str.match(r'^[A-Za-z]+\d+$').all()
                    if pattern_match:
                        return True
        
        # For numeric columns without ID in name
        if is_numeric_dtype(series.dtype):
            # Check if it's a sequence of unique values
            if series.nunique() == len(series) and series.is_monotonic_increasing:
                return True
        
        return False

def is_numeric_dtype(dtype) -> bool:
    """Check if a dtype is numeric."""
    return np.issubdtype(dtype, np.number)

def is_datetime_dtype(dtype) -> bool:
    """Check if a dtype is datetime."""
    return np.issubdtype(dtype, np.datetime64)

def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Get list of numeric columns in a dataframe."""
    return df.select_dtypes(include=[np.number]).columns.tolist()

def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Get list of categorical columns in a dataframe."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def is_id_column(series: pd.Series) -> bool:
    """
    Check if a series is likely an ID column based on uniqueness and sequence.
    
    Parameters:
    -----------
    series : pandas.Series
        Input series to check
        
    Returns:
    --------
    bool
        True if the series appears to be an ID column
    """
    # Check if numeric
    if not is_numeric_dtype(series.dtype):
        return False
    
    # Check uniqueness
    if series.nunique() != len(series):
        return False
    
    # Check if values form a sequence
    sorted_values = sorted(series.dropna())
    if len(sorted_values) < 2:
        return False
        
    # Check if values form an arithmetic sequence
    diffs = np.diff(sorted_values)
    return len(set(diffs)) <= 2  # Allow for at most 2 different steps 