import pandas as pd
import numpy as np
from automl.preprocessor import Preprocessor
import logging
import os
import pytest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Test.Preprocessor')

def create_synthetic_data():
    """Create synthetic data with various types of missing values."""
    np.random.seed(42)
    n_samples = 1000
    
    # Create a DataFrame with different types of features
    df = pd.DataFrame({
        # Numeric features
        'id': range(n_samples),  # ID column
        'normal_dist': np.random.normal(0, 1, n_samples),  # Normal distribution
        'skewed_dist': np.random.exponential(2, n_samples),  # Skewed distribution
        'ordinal': np.random.randint(1, 6, n_samples),  # Ordinal (1-5)
        
        # Categorical features
        'category_few': np.random.choice(['A', 'B', 'C'], n_samples),
        'category_many': np.random.choice(list('ABCDEFGHIJ'), n_samples),
        
        # DateTime feature
        'date': pd.date_range('2023-01-01', periods=n_samples).astype(str)
    })
    
    # Introduce missing values with different patterns
    # 40% missing (should be dropped)
    df.loc[np.random.choice([True, False], n_samples, p=[0.4, 0.6]), 'normal_dist'] = np.nan
    
    # 15% missing (should use KNN)
    df.loc[np.random.choice([True, False], n_samples, p=[0.15, 0.85]), 'skewed_dist'] = np.nan
    
    # 3% missing (should use statistical methods)
    df.loc[np.random.choice([True, False], n_samples, p=[0.03, 0.97]), 'ordinal'] = np.nan
    df.loc[np.random.choice([True, False], n_samples, p=[0.03, 0.97]), 'category_few'] = np.nan
    
    # Custom null values
    df.loc[np.random.choice(n_samples, 50), 'category_many'] = 'NULL'
    df.loc[np.random.choice(n_samples, 50), 'date'] = 'MISSING'
    
    return df

def test_with_synthetic_data():
    """Test preprocessor with synthetic data."""
    logger.info("Testing with synthetic data...")
    
    # Create synthetic data
    df = create_synthetic_data()
    
    logger.info("\nOriginal data info:")
    logger.info(f"Shape: {df.shape}")
    logger.info("\nMissing values:")
    logger.info(df.isnull().sum())
    
    # Initialize preprocessor with default parameters
    preprocessor = Preprocessor()
    
    # Process data
    df_processed = preprocessor.fill_null(df, null_character='NULL')
    
    logger.info("\nProcessed data info:")
    logger.info(f"Shape: {df_processed.shape}")
    logger.info("\nRemaining missing values:")
    logger.info(df_processed.isnull().sum())
    
    # Verify results
    assert df_processed.isnull().sum().sum() == 0, "There should be no missing values"
    assert 'normal_dist' not in df_processed.columns, "Column with >30% missing should be dropped"

def test_with_titanic_data():
    """Test preprocessor with Titanic dataset."""
    logger.info("\nTesting with Titanic data...")
    
    # Load Titanic data
    data_path = os.path.join('data', 'classification_train.csv')
    df = pd.read_csv(data_path)
    
    logger.info("\nOriginal Titanic data info:")
    logger.info(f"Shape: {df.shape}")
    logger.info("\nMissing values:")
    logger.info(df.isnull().sum())
    
    # Initialize preprocessor with custom parameters
    preprocessor = Preprocessor(
        drop_threshold=70.0,  # More lenient drop threshold
        knn_threshold=10.0,   # More aggressive KNN usage
        ordinal_ratio=0.1     # More lenient ordinal detection
    )
    
    # Process data
    df_processed = preprocessor.fill_null(df)
    
    logger.info("\nProcessed Titanic data info:")
    logger.info(f"Shape: {df_processed.shape}")
    logger.info("\nRemaining missing values:")
    logger.info(df_processed.isnull().sum())
    
    # Verify results
    assert df_processed.isnull().sum().sum() == 0, "There should be no missing values"
    assert 'Cabin' not in df_processed.columns, "Cabin should be dropped due to too many missing values"

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    np.random.seed(42)
    df = pd.DataFrame({
        'normal_dist': np.random.normal(0, 1, 100),
        'skewed_dist': np.random.exponential(1, 100),
        'ordinal': np.random.choice([1, 2, 3, 4, 5, np.nan], 100),
        'category': np.random.choice(['A', 'B', 'C', None], 100),
        'binary': np.random.choice(['Yes', 'No', None], 100),
        'id': range(1, 101)
    })
    return df

@pytest.fixture
def preprocessor():
    """Create a preprocessor instance for testing."""
    return Preprocessor(drop_threshold=0.5, knn_threshold=0.3, ordinal_ratio=0.8)

def test_initialization(preprocessor):
    """Test preprocessor initialization."""
    assert preprocessor.drop_threshold == 0.5
    assert preprocessor.knn_threshold == 0.3
    assert preprocessor.ordinal_ratio == 0.8

def test_generate_descriptor(preprocessor, sample_df):
    """Test descriptor generation."""
    descriptor = preprocessor.generate_descriptor(sample_df)
    assert isinstance(descriptor, pd.DataFrame)
    assert 'null_count' in descriptor.columns
    assert 'null_percentage' in descriptor.columns
    assert len(descriptor) == len(sample_df.columns)

def test_replace_by_null(preprocessor, sample_df):
    """Test null character replacement."""
    df = sample_df.copy()
    df['normal_dist'] = df['normal_dist'].replace(df['normal_dist'].iloc[0], 'NULL')
    df_cleaned = preprocessor.replace_by_null(df, null_character='NULL')
    assert pd.isna(df_cleaned['normal_dist'].iloc[0])
    assert not pd.isna(df_cleaned['normal_dist'].iloc[1])

def test_knn_impute(preprocessor, sample_df):
    """Test KNN imputation."""
    df = sample_df.copy()
    df.loc[0, 'normal_dist'] = np.nan
    # Generate descriptor first
    preprocessor.descriptor = preprocessor.generate_descriptor(df)
    preprocessor.knn_impute(df, 'normal_dist')
    assert not pd.isna(df['normal_dist'].iloc[0])

def test_fill_null(preprocessor, sample_df):
    """Test null filling with different strategies."""
    df = sample_df.copy()
    # Make ordinal column have >50% nulls
    df['ordinal'] = np.nan
    filled_df = preprocessor.fill_null(df)
    # Check if ordinal column is dropped due to excessive nulls
    assert 'ordinal' not in filled_df.columns
    # Check if remaining nulls are filled
    assert filled_df.isnull().sum().sum() == 0

def test_fill_null_with_null_character():
    """Test null handling with custom null character."""
    # Use default parameters
    preprocessor = Preprocessor()
    
    df = pd.DataFrame({
        'numeric': [1, -999, 3, 4, 5],  # Only one -999 value (20% missing)
        'category': ['A', 'MISSING', 'C', 'D', 'E']  # Only one MISSING value
    })
    
    # Log initial state
    logger.info("\nInitial data:")
    logger.info(df)
    
    # Replace nulls and check descriptor
    df_with_nulls = preprocessor.replace_by_null(df, null_character=-999)
    descriptor = preprocessor.generate_descriptor(df_with_nulls)
    logger.info("\nDescriptor after replacing -999 with NaN:")
    logger.info(descriptor)
    
    # Process data
    filled_df = preprocessor.fill_null(df, null_character=-999)
    logger.info("\nFinal data:")
    logger.info(filled_df)
    
    # Assertions
    assert filled_df.isnull().sum().sum() == 0, "There should be no missing values"
    assert 'numeric' in filled_df.columns, "Numeric column should not be dropped"
    assert -999 not in filled_df['numeric'].values, "-999 should be replaced"

def test_edge_cases(preprocessor):
    """Test edge cases."""
    # Empty DataFrame
    empty_df = pd.DataFrame()
    assert len(preprocessor.fill_null(empty_df)) == 0
    
    # Single column DataFrame with all nulls
    all_null_df = pd.DataFrame({'col': [np.nan] * 5})
    processed_df = preprocessor.fill_null(all_null_df)
    assert len(processed_df.columns) == 0  # All columns should be dropped

def test_remove_duplicates():
    """Test duplicate removal functionality."""
    # Create a DataFrame with duplicates
    df = pd.DataFrame({
        'id': [1, 2, 2, 3, 3, 4],
        'value': [10, 20, 20, 30, 30, 40],
        'category': ['A', 'B', 'B', 'C', 'C', 'E']  # Make categories match for id=3
    })
    
    # Test exact duplicates
    preprocessor = Preprocessor(keep='first')
    df_no_dups = preprocessor.remove_duplicates(df)
    assert len(df_no_dups) == 4, "Should remove exact duplicates"
    assert df_no_dups['id'].tolist() == [1, 2, 3, 4], "Should keep first occurrence"
    
    # Test keeping last occurrence
    preprocessor = Preprocessor(keep='last')
    df_last = preprocessor.remove_duplicates(df)
    assert len(df_last) == 4, "Should remove exact duplicates"
    assert df_last['category'].tolist() == ['A', 'B', 'C', 'E'], "Should keep last occurrence"
    
    # Test subset duplicates
    df_subset = preprocessor.remove_duplicates(df, subset=['value'])
    assert len(df_subset) == 4, "Should remove duplicates based on value column"
    
    # Test with null values (NaN values are considered equal in pandas)
    df_nulls = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'value': [10, np.nan, np.nan, 40],
        'category': ['A', 'B', 'C', 'D']
    })
    df_with_nulls = preprocessor.remove_duplicates(df_nulls, subset=['value'])
    assert len(df_with_nulls) == 3, "Should treat NaN values as duplicates"

def test_integrated_preprocessing():
    """Test integrated preprocessing with null handling and duplicate removal."""
    # Create a DataFrame with both nulls and duplicates
    df = pd.DataFrame({
        'id': [1, 2, 2, 3, 3, 4],
        'numeric': [10, -999, -999, 30, 30, 40],  # Renamed from 'value' to avoid confusion
        'category': ['A', 'B', 'B', 'MISSING', 'MISSING', 'E']
    })
    
    # Initialize preprocessor with higher drop threshold
    preprocessor = Preprocessor(
        drop_threshold=50.0,  # Increase threshold to prevent dropping columns
        keep='first'
    )
    
    # Process data with both null handling and duplicate removal
    processed_df = preprocessor.fill_null(
        df,
        null_character={'numeric': -999, 'category': 'MISSING'},
        remove_dups=True
    )
    
    # Verify results
    assert len(processed_df) == 4, "Should remove duplicates"
    assert processed_df.isnull().sum().sum() == 0, "Should handle null values"
    assert -999 not in processed_df['numeric'].values, "Should replace null character"
    assert 'MISSING' not in processed_df['category'].values, "Should handle string null values"

if __name__ == "__main__":
    test_preprocessor() 