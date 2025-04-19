class Agg:
    """Base class for aggregation operations.

    This class serves as a base for different types of aggregations that can be
    performed on DataFrame columns.

    Args:
        column (str): The column name to perform the aggregation on.
    """

    def __init__(self, column: str):
        """Initialize an aggregation operation.

        Args:
            column (str): The column name to perform the aggregation on.
        """
        self.column = column

class AggWithDropNa(Agg):
    """Base class for aggregations that support NA handling.

    This class extends Agg to add NA handling capabilities for aggregations
    that need to optionally drop NA values before performing the operation.

    Args:
        column (str): The column name to perform the aggregation on.
        drop_na (bool, optional): Whether to drop NA values before aggregation. Defaults to True.
    """

    def __init__(self, column: str, drop_na: bool = True):
        """Initialize an aggregation operation with NA handling.

        Args:
            column (str): The column name to perform the aggregation on.
            drop_na (bool, optional): Whether to drop NA values before aggregation. Defaults to True.
        """
        super().__init__(column)
        self.drop_na = drop_na

class Mean(Agg):
    """Aggregation class for computing mean values."""
    pass

class Min(Agg):
    """Aggregation class for computing minimum values."""
    pass

class Max(Agg):
    """Aggregation class for computing maximum values."""
    pass

class Median(Agg):
    """Aggregation class for computing median values."""
    pass

class Mode(Agg):
    """Aggregation class for computing mode values."""
    pass

class Sum(Agg):
    """Aggregation class for computing sum values."""
    pass

class Count(Agg):
    """Aggregation class for counting values."""
    pass

class SD(Agg):
    """Aggregation class for computing standard deviation."""
    pass

class Variance(Agg):
    """Aggregation class for computing variance."""
    pass

class Skewness(Agg):
    """Aggregation class for computing skewness."""
    pass

class Kurtosis(Agg):
    """Aggregation class for computing kurtosis."""
    pass

class CountDistinct(Agg):
    """Aggregation class for counting distinct values."""
    pass

class Random(Agg):
    """Aggregation class for selecting a random value."""
    pass

class First(AggWithDropNa):
    """Aggregation class for taking the first value with optional NA handling."""
    pass

class Last(AggWithDropNa):
    """Aggregation class for taking the last value with optional NA handling."""
    pass

class Percentile(Agg):
    """Aggregation class for computing percentile values.

    Args:
        column (str): The column name to perform the aggregation on.
        percentile (float): The percentile to compute (0-100).
    """

    def __init__(self, column: str, percentile: float):
        """Initialize a percentile aggregation operation.

        Args:
            column (str): The column name to perform the aggregation on.
            percentile (float): The percentile to compute (0-100).
        """
        super().__init__(column)
        self.percentile = percentile

