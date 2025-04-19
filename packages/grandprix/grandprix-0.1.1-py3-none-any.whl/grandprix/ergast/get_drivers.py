from .json import get_drivers_json, convert_drivers_json_to_df
from ..utils import must_have_columns, join, join_with_dict, aggregate, bring_columns_to_front
from typing import Optional, Dict, List, Union, Tuple
import pandas as pd
from .START_YEAR import START_YEAR
from ..utils import Filter
from ..utils.aggregate import aggregate, Last, Min, Max, CountDistinct

_drivers_cache = {}

def _uncached_get_drivers(year: int) -> pd.DataFrame:
    json = get_drivers_json(year)
    df = convert_drivers_json_to_df(json)
    df['year'] = year
    return df

def get_driver_ids(year: int) -> List[str]:
    drivers = get_drivers_json(year)
    return [d["driverId"] for d in drivers]

@must_have_columns("year", "driver_id", "first_name", "last_name", "full_name", "nationality", "date_of_birth", "url")
def get_drivers(year: Optional[Union[int, Filter, Tuple[int, int]]] = None, use_cache: bool = True) -> pd.DataFrame:
    """
    Get drivers from a given year or range of years.
    If year is a tuple, it is interpreted as a range of years.
    If year is a Filter, it is interpreted as a filter on the year column.
    If year is an int, it is interpreted as a single year.
    If year is None, all years are returned.
    If multiple years are returned:
        Last values are taken for all columns except year
        Start and end year are added as first and last year columns
    Args:
        year: Optional[Union[int, Filter, Tuple[int, int]]]: The year or range of years to get drivers from.
        use_cache: bool: Whether to use the cache.
    Returns:
        pd.DataFrame: A DataFrame of drivers.
    """
    # cache is only used when year is not None

    if isinstance(year, Tuple):
        year = Filter(column="year", values=year)

    if isinstance(year, Filter):
        if year.single_value():
            year = int(year.value)

    if isinstance(year, int):
        if use_cache:
            if year in _drivers_cache:
                return _drivers_cache[year]
            _drivers_cache[year] = _uncached_get_drivers(year)
            return _drivers_cache[year]
        else:
            return _uncached_get_drivers(year)

    all_years = list(range(START_YEAR, pd.Timestamp.now().year + 1))
    years_key = 'all_years'
    if year is not None:
        all_years = year.apply(all_years)
        years_key = None

    if years_key is not None and years_key in _drivers_cache and use_cache:
        return _drivers_cache[years_key]

    df_list = []
    for y in all_years:
        df = get_drivers(year=y, use_cache=use_cache)
        if not df.empty:
            df_list.append(df)
        df_list.append(df)
    
    result = pd.concat(df_list, ignore_index=True).sort_values(by="year")

    df = aggregate(
        result, group_by="driver_id", 
        first_name=Last("first_name", drop_na=True),
        last_name=Last("last_name", drop_na=True), # full_name will be calculated from first_name and last_name
        first_year=Min("year"),
        last_year=Max("year"),
        nationality=Last("nationality", drop_na=True),
        date_of_birth=Last("date_of_birth", drop_na=True),
        url=Last("url", drop_na=True),
    )

    if "full_name" not in df.columns:
        df["full_name"] = df["first_name"] + " " + df["last_name"]

    df = bring_columns_to_front(df, ["driver_id", "first_name", "last_name", "full_name", "nationality", "date_of_birth", "url"])
        
    if use_cache and years_key is not None:
        _drivers_cache[years_key] = df

    return df
    

_driver_metadata_cache = {}

def _extract_driver_metadata(drivers) -> dict:
    return {
        d["driverId"]: {
            "first_name": d["givenName"],
            "last_name": d["familyName"],
            "full_name": f"{d['givenName']} {d['familyName']}",
            "nationality": d["nationality"],
            'date_of_birth': d['dateOfBirth'],
            'url': d['url'],
        } 
        for d in drivers
    }

def get_driver_metadata(year: int = 2024, use_cache: bool = True) -> Dict[int, dict]:
    if not use_cache:
        drivers = get_drivers_json(year)
        return _extract_driver_metadata(drivers)
    
    if year in _driver_metadata_cache:
        return _driver_metadata_cache[year]
    else:
        drivers = get_drivers_json(year)
        metadata = _extract_driver_metadata(drivers)
        _driver_metadata_cache[year] = metadata
        return metadata

@must_have_columns("year", "driver_id", 'first_name', 'last_name', 'full_name', 'nationality', 'date_of_birth', 'url')
def add_driver_metadata(df: pd.DataFrame, use_cache: bool = True) -> pd.DataFrame:
    # if only one year is in df, use that as a key
    if 'year' in df.columns:
        years = df['year'].unique()

    else:
        years = None

    if years is not None and len(years) == 1:
        year = years[0]
        metadata_dict = get_driver_metadata(year, use_cache=use_cache)
        return join_with_dict(df, dict_data=metadata_dict, on_column="driver_id")
    else:
        # join with the data from all years
        metadata_df = get_drivers(use_cache=use_cache)
        return join(df, metadata_df, on=["driver_id"])
