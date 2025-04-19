"""Aggregation module for flexible DataFrame operations.

This module provides a comprehensive set of tools for performing aggregations
on pandas DataFrames. It includes:

1. A flexible aggregation function that supports named aggregations
2. Various aggregation classes for different statistical operations:
   - Basic statistics: Mean, Min, Max, Median, Mode
   - Advanced statistics: SD, Variance, Skewness, Kurtosis
   - Special operations: First, Last, Random, CountDistinct
   - Custom operations: Percentile

The module is designed to provide a clean and intuitive interface for
performing complex aggregations while maintaining type safety and
flexibility.
"""

from .aggregate import aggregate
from .Agg import *

__all__ = [
    "aggregate", "Mean", "Min", "Max", "First", "Last", "Median", 
    "Mode", "Sum", "Count", "SD", "Variance", "Skewness", "Kurtosis", 
    "CountDistinct", "Random", "Percentile"
]
