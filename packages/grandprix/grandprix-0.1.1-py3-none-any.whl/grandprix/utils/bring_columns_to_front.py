import pandas as pd
from functools import wraps

def bring_columns_to_front(df: pd.DataFrame, columns: list[str]):
    """Reorders DataFrame columns to bring specified columns to the front.

    Args:
        df (pd.DataFrame): The DataFrame to reorder.
        columns (list[str]): List of column names to bring to the front.

    Returns:
        pd.DataFrame: DataFrame with reordered columns.
    """
    return df[[*columns, *[col for col in df.columns if col not in columns]]]

def must_have_columns(*args, bring_to_front: bool = True):
    """Decorator to ensure a function returns a DataFrame with required columns.

    Args:
        *args: Column names that must be present in the DataFrame.
        bring_to_front (bool, optional): Whether to bring the specified columns to the front
            of the DataFrame. Defaults to True.

    Returns:
        function: Decorated function that validates column presence.

    Raises:
        TypeError: If the decorated function doesn't return a DataFrame.
        KeyError: If any required columns are missing from the DataFrame.
    """
    # Flatten args in case of single list or multiple strings
    if len(args) == 1 and isinstance(args[0], list):
        columns = args[0]
    else:
        columns = list(args)

    def decorator(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            result = func(*func_args, **func_kwargs)
            if not isinstance(result, pd.DataFrame):
                raise TypeError("Function must return a pandas DataFrame.")
            missing = set(columns) - set(result.columns)
            if missing:
                raise KeyError(f"Missing columns: {missing}")
            if bring_to_front:
                return bring_columns_to_front(result, columns=columns)
            return result
        return wrapper
    return decorator
