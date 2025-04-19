import pandas as pd

def dict_of_dicts_to_df(data: dict, index_column_name: str) -> pd.DataFrame:
    """
    Convert a dictionary of dictionaries to a DataFrame.

    Args:
        data: A dictionary where each value is a dictionary of attributes.
        index_column_name: The name for the column representing the outer dictionary's keys.

    Returns:
        A pandas DataFrame where each row corresponds to an inner dictionary,
        and the outer dictionary's keys are in a named column.
    """
    df = pd.DataFrame.from_dict(data, orient="index")
    df.reset_index(inplace=True)
    df = df.rename(columns={"index": index_column_name})
    return df
