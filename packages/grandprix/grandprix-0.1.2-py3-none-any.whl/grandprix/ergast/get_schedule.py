from typing import Optional, Union
import pandas as pd

from .json import get_season_schedule_json, convert_season_schedule_json_to_df
from ..utils import must_have_columns, join, Filter
from .START_YEAR import START_YEAR

_schedule_cache = {}

@must_have_columns("year", "round", "race_name", "circuit", "race_date", "country", "city")
def _get_uncached_schedule(year: int) -> pd.DataFrame:
    schedule = get_season_schedule_json(year)
    df = convert_season_schedule_json_to_df(schedule)
    df['year'] = year
    return df

@must_have_columns("year", "round", "race_name", "circuit", "race_date", "country", "city")
def get_schedule(year: Optional[Union[int, Filter]] = None, use_cache: bool = True) -> pd.DataFrame:

    if isinstance(year, Filter):
        filter = year
        del year
        if filter.single_value():
            year = filter.value
        else:
            df = get_schedule(year=None, use_cache=use_cache)
            return filter.apply(df)

    if year is not None:
        if use_cache:
            if year in _schedule_cache:
                return _schedule_cache[year]
            _schedule_cache[year] = _get_uncached_schedule(year)
            return _schedule_cache[year]
        else:
            return _get_uncached_schedule(year)

    else:
        all_years = list(range(START_YEAR, pd.Timestamp.now().year + 1))
        df_list = []
        for y in all_years:
            schedule = get_schedule(year=y, use_cache=use_cache)
            if not schedule.empty:
                df_list.append(schedule)
        return pd.concat(df_list, ignore_index=True)
    
@must_have_columns("year", "round", "race_name", "circuit", "race_date", "country", "city")
def add_race_metadata(df: pd.DataFrame, use_cache: bool = True) -> pd.DataFrame:
    years = df['year'].unique()
    if len(years) == 1:
        year = years[0]
        schedule_df = get_schedule(year, use_cache=use_cache)
        return join(df, schedule_df, on=["year", "round"])
    else:
        schedule_df = get_schedule(use_cache=use_cache)
        return join(df, schedule_df, on=["year", "round"])
