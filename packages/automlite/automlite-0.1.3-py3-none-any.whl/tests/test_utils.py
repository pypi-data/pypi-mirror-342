import pytest
import pandas as pd
import numpy as np
from automl.utils import DataFrameAnalyzer, is_numeric_dtype, is_datetime_dtype

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'id': range(1, 101),
        'name': [f'User_{i}' for i in range(1, 101)],
        'age': np.random.randint(18, 80, 100),
        'salary': np.random.normal(50000, 10000, 100),
        'department': np.random.choice(['HR', 'IT', 'Finance', 'Sales'], 100),
        'employee_id': [f'EMP{str(i).zfill(4)}' for i in range(1, 101)],
        'join_date': pd.date_range(start='2020-01-01', periods=100, freq='D'),
        'description': ['Long text description ' * 5 + str(i) for i in range(100)]
    })

def test_get_column_types(sample_df):
    analyzer = DataFrameAnalyzer()
    column_types = analyzer.get_column_types(sample_df)
    
    assert set(column_types.keys()) == {'numeric', 'categorical', 'datetime', 'text'}
    assert set(column_types['numeric']) == {'age', 'salary'}
    assert set(column_types['categorical']) == {'department', 'name', 'employee_id'}
    assert set(column_types['datetime']) == {'join_date'}
    assert set(column_types['text']) == {'description'}

def test_is_id_column(sample_df):
    analyzer = DataFrameAnalyzer()
    
    # Test numeric ID column
    assert analyzer.is_id_column(sample_df['id'])
    
    # Test string ID column with pattern
    assert analyzer.is_id_column(sample_df['employee_id'])
    
    # Test non-ID columns
    assert not analyzer.is_id_column(sample_df['age'])
    assert not analyzer.is_id_column(sample_df['department'])

def test_generate_summary(sample_df):
    analyzer = DataFrameAnalyzer()
    summary = analyzer.generate_summary(sample_df)
    
    # Test basic structure
    assert isinstance(summary, dict)
    assert set(summary.keys()) == {'basic_info', 'missing_data', 'column_types', 'numeric_stats', 'categorical_stats'}
    
    # Test basic info
    assert summary['basic_info']['rows'] == 100
    assert summary['basic_info']['columns'] == 8
    assert isinstance(summary['basic_info']['memory_usage'], float)
    
    # Test numeric stats
    assert set(summary['numeric_stats'].keys()) == {'age', 'salary'}
    for col in ['age', 'salary']:
        stats = summary['numeric_stats'][col]
        assert set(stats.keys()) == {'mean', 'std', 'min', 'max', 'skew', 'unique_values', 'distribution'}
    
    # Test categorical stats
    assert 'department' in summary['categorical_stats']
    dept_stats = summary['categorical_stats']['department']
    assert set(dept_stats.keys()) == {'unique_values', 'top_values', 'null_count'}
    assert dept_stats['unique_values'] == 4

def test_check_distribution(sample_df):
    analyzer = DataFrameAnalyzer()
    
    # Test normal distribution
    normal_data = pd.Series(np.random.normal(0, 1, 1000))
    assert analyzer.check_distribution(normal_data) == 'normal'
    
    # Test skewed distribution
    skewed_data = pd.Series(np.random.exponential(1, 1000))
    assert analyzer.check_distribution(skewed_data) == 'skewed'

def test_dtype_checks():
    # Test numeric dtype check
    assert is_numeric_dtype(np.dtype('int64'))
    assert is_numeric_dtype(np.dtype('float64'))
    assert not is_numeric_dtype(np.dtype('object'))
    
    # Test datetime dtype check
    assert is_datetime_dtype(np.dtype('datetime64[ns]'))
    assert not is_datetime_dtype(np.dtype('int64')) 