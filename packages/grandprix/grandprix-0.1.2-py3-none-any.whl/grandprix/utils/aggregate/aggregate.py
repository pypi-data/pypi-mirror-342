import pandas as pd
from typing import Union, List
from .Agg import *

def aggregate(df: pd.DataFrame, group_by: Union[str, List[str]], **kwargs) -> pd.DataFrame:
    """Perform named aggregation using aggregation classes.

    This function provides a flexible way to perform aggregations on a DataFrame using
    the aggregation classes defined in the Agg module. It supports various aggregation
    methods including statistical functions (mean, min, max, etc.) and special operations
    (first, last, random, etc.).

    Args:
        df (pd.DataFrame): The input DataFrame to aggregate.
        group_by (Union[str, List[str]]): Column(s) to group by. Can be a single column
            name or a list of column names.
        **kwargs: Named arguments where:
            - The key is the output column name
            - The value is an aggregation instruction (e.g., Mean("points"))

    Returns:
        pd.DataFrame: Aggregated DataFrame with one row per group and columns as specified
            in the kwargs.

    Examples:
        >>> df = pd.DataFrame({
        ...     'team': ['A', 'A', 'B', 'B'],
        ...     'points': [10, 20, 15, 25]
        ... })
        >>> result = aggregate(
        ...     df,
        ...     group_by='team',
        ...     avg_points=Mean('points'),
        ...     max_points=Max('points')
        ... )
        >>> print(result)
          team  avg_points  max_points
        0    A        15.0         20
        1    B        20.0         25

    Raises:
        ValueError: If an unsupported aggregation type is provided.
    """
    group_by = [group_by] if isinstance(group_by, str) else group_by
    agg_dict = {}

    for out_col, agg_spec in kwargs.items():
        col = agg_spec.column
        na = getattr(agg_spec, 'drop_na', True)

        if isinstance(agg_spec, Mean):
            agg_dict[out_col] = (col, "mean")
        elif isinstance(agg_spec, Min):
            agg_dict[out_col] = (col, "min")
        elif isinstance(agg_spec, Max):
            agg_dict[out_col] = (col, "max")
        elif isinstance(agg_spec, Sum):
            agg_dict[out_col] = (col, "sum")
        elif isinstance(agg_spec, Count):
            agg_dict[out_col] = (col, "count")
        elif isinstance(agg_spec, CountDistinct):
            agg_dict[out_col] = (col, lambda x: x.nunique(dropna=na))
        elif isinstance(agg_spec, SD):
            agg_dict[out_col] = (col, "std")
        elif isinstance(agg_spec, Variance):
            agg_dict[out_col] = (col, "var")
        elif isinstance(agg_spec, Skewness):
            agg_dict[out_col] = (col, lambda x: x.dropna().skew())
        elif isinstance(agg_spec, Kurtosis):
            agg_dict[out_col] = (col, lambda x: x.dropna().kurt())
        elif isinstance(agg_spec, Median):
            agg_dict[out_col] = (col, lambda x: x.dropna().median())
        elif isinstance(agg_spec, Mode):
            agg_dict[out_col] = (col, lambda x: x.dropna().mode().iloc[0] if not x.dropna().empty else None)
        elif isinstance(agg_spec, Percentile):
            p = agg_spec.percentile
            agg_dict[out_col] = (col, lambda x: x.dropna().quantile(p / 100.0))
        elif isinstance(agg_spec, First):
            agg_dict[out_col] = (col, lambda x: x.dropna().iloc[0] if na else x.iloc[0])
        elif isinstance(agg_spec, Last):
            agg_dict[out_col] = (col, lambda x: x.dropna().iloc[-1] if na else x.iloc[-1])
        elif isinstance(agg_spec, Random):
            agg_dict[out_col] = (col, lambda x: x.dropna().sample(n=1).iloc[0] if na else x.sample(n=1).iloc[0])
        else:
            raise ValueError(f"Unsupported aggregation: {agg_spec}")

    return df.groupby(group_by, as_index=False).agg(**agg_dict)