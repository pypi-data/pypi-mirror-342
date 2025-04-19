
from .main import AutoML

"""
AutoML package for automated machine learning tasks.
"""

__version__ = "0.1.6"

# Only import essential shared utilities here
from automlite.utils import DataFrameAnalyzer, is_numeric_dtype, is_datetime_dtype
from automlite.preprocessor import Preprocessor

__all__ = [
    'DataFrameAnalyzer',
    'Preprocessor',
    'is_numeric_dtype',
    'is_datetime_dtype'
]
