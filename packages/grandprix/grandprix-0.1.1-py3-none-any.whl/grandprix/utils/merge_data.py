import pandas as pd
import numpy as np
from typing import Optional, Union, List
from .dict_of_dicts_to_df import dict_of_dicts_to_df


def join(
        df1: pd.DataFrame, df2: pd.DataFrame, how: str = "left", 
        on: Optional[Union[str, List[str]]] = None
    ) -> pd.DataFrame:
    """
    Merge two dataframes.

    Args:
        df1: The first dataframe to merge.
        df2: The second dataframe to merge.
        how: The type of merge to perform.
        on: The column(s) to merge on.
    Returns:
        The merged dataframe.
    """

    # for columns that are in both dataframes but no in on, combine them
    if on is None:
        on = df1.columns.intersection(df2.columns).tolist()

    if isinstance(on, str):
        on = [on]

    shared_columns = df1.columns.intersection(df2.columns)
    combine_columns = set(shared_columns) - set(on)

    if combine_columns:
        df1 = df1.rename(columns={col: f'{col}_1' for col in combine_columns})
        df2 = df2.rename(columns={col: f'{col}_2' for col in combine_columns})

    on = [col for col in on if col not in combine_columns]

    merged = pd.merge(df1, df2, how=how, on=on)

    for col in combine_columns:
        merged[col] = np.where(merged[f'{col}_1'].isna(), merged[f'{col}_2'], merged[f'{col}_1'])
        merged = merged.drop(columns=[f'{col}_1', f'{col}_2'])

    return merged

def join_with_dict(
        df: pd.DataFrame,
        dict_data: dict,
        on_column: Optional[str] = None
    ) -> pd.DataFrame:
    """
    Merge a dataframe with a dictionary.

    Args:
        df: The dataframe to merge.
        dict_data: The dictionary to merge with.
        on_column: The column to merge on. 
            If None, each key will be a new column and its value will be the dictionary value.
            Else, the dictionary is a dictionary of dictionaries where the key is the value of the on_column.
    Returns:
        The merged dataframe.
    """

    if on_column is None:
        df = df.copy()
        for key, value in dict_data.items():
            df[key] = value
        return df
    else:
        dict_df = dict_of_dicts_to_df(dict_data, index_column_name=on_column)
        return pd.merge(df, dict_df, on=on_column, how='left')
        
