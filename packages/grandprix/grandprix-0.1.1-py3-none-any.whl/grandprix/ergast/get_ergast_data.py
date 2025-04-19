import pandas as pd
import numpy as np
from typing import Optional, List

from .json import (
    get_season_schedule_json,
    get_race_results_json,
    get_qualifying_results_json,
    get_driver_standings_json,
    get_constructor_standings_json,
    get_lap_times_json,
    get_pit_stop_times_json,
    get_fastest_laps_json,
    get_drivers_json
)

from .df import (
    convert_season_schedule_json_to_df,
    convert_race_results_json_to_df,
    convert_qualifying_results_json_to_df,
    convert_driver_standings_json_to_df,
    convert_constructor_standings_json_to_df,
    convert_lap_times_json_to_df,
    convert_pit_stop_times_json_to_df,
    convert_fastest_laps_json_to_df,
    convert_drivers_json_to_df
)

from .get_num_rounds import get_num_rounds

_metadata_cache = {}

def _bring_columns_to_front(df: pd.DataFrame, columns: list[str]):
    return df[[*columns, *[col for col in df.columns if col not in columns]]]

def _must_have_columns(df: pd.DataFrame, columns: list[str]):
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def get_race_metadata(year: int = 2024) -> dict[int, dict]:
    if year in _metadata_cache:
        return _metadata_cache[year]
    races = get_season_schedule_json(year)
    _metadata_cache[year] = {
        int(r["round"]): {
            "race_date": r["date"],
            "race_name": r["raceName"],
            "circuit": r["Circuit"]["circuitName"],
            "country": r["Circuit"]["Location"]["country"],
            "city": r["Circuit"]["Location"]["locality"]
        }
        for r in races
    }
    return _metadata_cache[year]

def get_drivers(year: Optional[int] = None):
    if year is not None:
        json = get_drivers_json(year)
        df = convert_drivers_json_to_df(json)
        df['year'] = year
        _must_have_columns(df, columns=["year", "driver_id", "first_name", "last_name", "full_name", "nationality", "date_of_birth", "url"])
        return _bring_columns_to_front(df, columns=["year", "driver_id", "first_name", "last_name", "full_name", "nationality", "date_of_birth", "url"])
    
    else:
        all_years = list(range(1950, pd.Timestamp.now().year + 1))
        df_list = []
        for y in all_years:
            df = get_drivers(year=y)
            if not df.empty:
                df_list.append(df)
        return pd.concat(df_list, ignore_index=True)
    
def get_drivers_range(start_year: int, end_year: int):
    df_list = []
    for year in range(start_year, end_year + 1):
        df_list.append(get_drivers(year))
    result = pd.concat(df_list, ignore_index=True)
    _must_have_columns(result, columns=["year", "driver_id", "first_name", "last_name", "full_name", "nationality", "date_of_birth", "url"])
    # aggregate year to max and min by driver_id
    return (
        result
        .groupby('driver_id', as_index=False)
        .agg(
            year_min=('year', 'min'),
            year_max=('year', 'max'),
            first_name=('first_name', 'last'),
            last_name=('last_name', 'last'),
            full_name=('full_name', 'last'),
            nationality=('nationality', 'last'),
            date_of_birth=('date_of_birth', 'last'),
            url=('url', 'last')
        )
    )

def get_driver_metadata(year: int = 2024) -> dict[int, dict]:
    drivers = get_drivers_json(year)
    return {d["driverId"]: {
        "first_name": d["givenName"],
        "last_name": d["familyName"],
        "full_name": f"{d['givenName']} {d['familyName']}",
        "nationality": d["nationality"],
        'date_of_birth': d['dateOfBirth'],
        'url': d['url'],
    } for d in drivers}

def get_schedule(year: Optional[int] = None):
    if year is not None:
        schedule = get_season_schedule_json(year=year)
        df = convert_season_schedule_json_to_df(schedule).assign(year=year)
        df['year'] = year
        _must_have_columns(df, columns=["year", "round", "race_name", "circuit", "race_date", "country", "city"])
        return _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "race_date", "country", "city"])

    else:
        all_years = list(range(1950, pd.Timestamp.now().year + 1))
        df_list = []
        for y in all_years:
            schedule = get_season_schedule_json(year=y)
            df = convert_season_schedule_json_to_df(schedule)
            if not df.empty:
                df["year"] = y
                df_list.append(df)
        return pd.concat(df_list, ignore_index=True)


def _add_race_metadata(df: pd.DataFrame, year: Optional[int] = None, round_num: Optional[int] = None):
    if year is not None and round_num is not None:
        df = df.copy()
        metadata = get_race_metadata(year)
        df["year"] = year
        df["round"] = round_num
        df["race_name"] = metadata[round_num]["race_name"]
        df["circuit"] = metadata[round_num]["circuit"]
        df["race_date"] = metadata[round_num]["race_date"]
        df["country"] = metadata[round_num]["country"]
        df["city"] = metadata[round_num]["city"]
        return df
    
    schedule = get_schedule(year=year)
    _must_have_columns(schedule, columns=["year", "round", "race_name", "circuit", "race_date", "country", "city"])
    df = pd.merge(df, schedule, on=["year", "round"], how="left")
    return df

def _add_driver_metadata(df: pd.DataFrame, year: int, driver_id: Optional[str] = None):

    if driver_id is not None and year is not None:
        df = df.copy()
        metadata = get_driver_metadata(year)
        df["driver_id"] = driver_id
        df["first_name"] = metadata[driver_id]["first_name"]
        df["last_name"] = metadata[driver_id]["last_name"]
        df["full_name"] = metadata[driver_id]["full_name"]
        return df
    
    drivers = get_drivers(year)


    df = df.copy()
    if driver_id is None:
        drivers = get_drivers(year)
        if 'full_name' in df.columns:
            df = df.rename(columns={"full_name": "full_name_2"})
        df = pd.merge(df, drivers, on="driver_id", how="left")
        df['full_name'] = np.where(df['full_name'].isna(), df['full_name_2'], df['full_name'])
        df = df.drop(columns=["full_name_2"])
        return df

    else:
        metadata = get_driver_metadata(year)
        df["driver_id"] = driver_id
        df["first_name"] = metadata[driver_id]["first_name"]
        df["last_name"] = metadata[driver_id]["last_name"]
        df["full_name"] = metadata[driver_id]["full_name"]
        df["nationality"] = metadata[driver_id]["nationality"]
        df["date_of_birth"] = metadata[driver_id]["date_of_birth"]
        df["url"] = metadata[driver_id]["url"]
        return df

def get_driver_ids(year: int) -> List[str]:
    drivers = get_drivers_json(year)
    return [d["driverId"] for d in drivers]

def get_race_results(
        year: int, add_race_metadata: bool = True, add_driver_metadata: bool = True,
        round_num: Optional[int] = None
    ):
    if round_num is None:
        num_rounds = get_num_rounds(year, completed_only=True)
        df_list = []
        for round_num in range(1, num_rounds + 1):
            df = get_race_results(year, add_race_metadata=add_race_metadata, add_driver_metadata=False, round_num=round_num)
            if df.empty:
                continue
            df_list.append(df)
        result = pd.concat(df_list, ignore_index=True)
    
    else:
        results = get_race_results_json(year, round_num)
        df = convert_race_results_json_to_df(results)
        if add_race_metadata:
            _add_race_metadata(df=df, year=year, round_num=round_num)
        
        result = _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date"])

    if add_driver_metadata:
        result = _add_driver_metadata(df=result, year=year, driver_id=None)

    return result

def get_race_results_range(start_year: int, end_year: int, add_race_metadata: bool = True, add_driver_metadata: bool = True):
    df_list = []
    for year in range(start_year, end_year + 1):
        df_list.append(get_race_results(year, add_race_metadata=add_race_metadata, add_driver_metadata=add_driver_metadata, round_num=None))
    return pd.concat(df_list, ignore_index=True)

def get_qualifying_results(
        year: int, add_race_metadata: bool = True, add_driver_metadata: bool = False, round_num: Optional[int] = None
    ):
    if round_num is None:
        num_rounds = get_num_rounds(year, completed_only=True)
        df_list = []
        for round_num in range(1, num_rounds + 1):
            df = get_qualifying_results(year, add_race_metadata=add_race_metadata, round_num=round_num, add_driver_metadata=False)
            if df.empty:
                continue
            df_list.append(df)
        result = pd.concat(df_list, ignore_index=True)
    else:
        json = get_qualifying_results_json(year, round_num)
        df = convert_qualifying_results_json_to_df(json)
        if add_race_metadata:
            _add_race_metadata(df=df, year=year, round_num=round_num)
        result = _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date"])

    if add_driver_metadata:
        drivers = get_drivers(year)
        drivers = drivers.rename(columns={"full_name": "full_name_2"})
        result = pd.merge(result, drivers, on="driver_id", how="left")
        result['full_name'] = np.where(result['full_name'].isna(), result['full_name_2'], result['full_name'])
        result = result.drop(columns=["full_name_2"])

    return result

def get_qualifying_results_range(start_year: int, end_year: int, add_race_metadata: bool = True, add_driver_metadata: bool = False):
    df_list = []    
    for year in range(start_year, end_year + 1):
        df_list.append(get_qualifying_results(year, add_race_metadata=add_race_metadata, add_driver_metadata=add_driver_metadata, round_num=None))
    return pd.concat(df_list, ignore_index=True)

def get_driver_standings(
        year: int, add_race_metadata: bool = True, add_driver_metadata: bool = False,
        round_num: Optional[int] = None
    ):
    if round_num is None:
        num_rounds = get_num_rounds(year, completed_only=True)
        df_list = []
        for round_num in range(1, num_rounds + 1):
            df = get_driver_standings(year, add_race_metadata=add_race_metadata, add_driver_metadata=False, round_num=round_num)
            if df.empty:
                continue
            df_list.append(df)
        result = pd.concat(df_list, ignore_index=True)
    
    else:
        json = get_driver_standings_json(year, round_num)
        df = convert_driver_standings_json_to_df(json)
        if add_race_metadata:
            _add_race_metadata(df=df, year=year, round_num=round_num)
        result = _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date"])

    if add_driver_metadata:
        drivers = get_drivers(year)
        drivers = drivers.rename(columns={"full_name": "full_name_2"})
        result = pd.merge(result, drivers, on="driver_id", how="left")
        result['full_name'] = np.where(result['full_name'].isna(), result['full_name_2'], result['full_name'])
        result = result.drop(columns=["full_name_2"])

    return result

def get_driver_standings_range(start_year: int, end_year: int, add_race_metadata: bool = True, add_driver_metadata: bool = False):
    df_list = []
    for year in range(start_year, end_year + 1):
        df_list.append(get_driver_standings(year, add_race_metadata=add_race_metadata, add_driver_metadata=add_driver_metadata, round_num=None))
    return pd.concat(df_list, ignore_index=True)


def get_constructor_standings(year: int, add_race_metadata: bool = True, round_num: Optional[int] = None):
    if round_num is None:
        num_rounds = get_num_rounds(year, completed_only=True)
        df_list = []
        for round_num in range(1, num_rounds + 1):
            df = get_constructor_standings(year, add_race_metadata=add_race_metadata, round_num=round_num)
            if df.empty:
                continue
            df_list.append(df)
        return pd.concat(df_list, ignore_index=True)
    
    else:
        json = get_constructor_standings_json(year, round_num)
        df = convert_constructor_standings_json_to_df(json)
        if add_race_metadata:
            _add_race_metadata(df=df, year=year, round_num=round_num)
        return _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date"])
    
def get_constructor_standings_range(start_year: int, end_year: int, add_race_metadata: bool = True):
    df_list = []
    for year in range(start_year, end_year + 1):
        df_list.append(get_constructor_standings(year, add_race_metadata=add_race_metadata, round_num=None))
    return pd.concat(df_list, ignore_index=True)

def get_lap_times(
        year: int, add_race_metadata: bool = True, add_driver_metadata: bool = False,
        round_num: Optional[int] = None, driver_id: Optional[str] = None
    ):
    if round_num is not None and driver_id is not None:
        json = get_lap_times_json(year=year, round_num=round_num, driver_id=driver_id)
        df = convert_lap_times_json_to_df(json)
        if add_race_metadata:
            _add_race_metadata(df=df, year=year, round_num=round_num)
        df["driver_id"] = driver_id
        result = _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date", "driver_id"])

    else:
        if driver_id is None:
            driver_ids = get_driver_ids(year)
        else:
            driver_ids = [driver_id]

        if round_num is None:
            round_nums = range(1, get_num_rounds(year, completed_only=True) + 1)
        else:
            round_nums = [round_num]

        df_list = []
        for round_num in round_nums:
            for driver_id in driver_ids:    
                df = get_lap_times(year=year, round_num=round_num, driver_id=driver_id, add_race_metadata=add_race_metadata, add_driver_metadata=False)
                if df.empty:
                    continue
                df_list.append(df)
        result = pd.concat(df_list, ignore_index=True)

    if add_driver_metadata:
        drivers = get_drivers(year)
        drivers = drivers.rename(columns={"full_name": "full_name_2"})
        result = pd.merge(result, drivers, on="driver_id", how="left")
        result['full_name'] = np.where(result['full_name'].isna(), result['full_name_2'], result['full_name'])
        result = result.drop(columns=["full_name_2"])

    return result

def get_pit_stop_times(
        year: int, round_num: Optional[int] = None, driver_id: Optional[str] = None
    ):
    if round_num is not None and driver_id is not None:
        json = get_pit_stop_times_json(year=year, round_num=round_num, driver_id=driver_id)
        df = convert_pit_stop_times_json_to_df(json)
        _add_race_metadata(df=df, year=year, round_num=round_num)
        df["driver_id"] = driver_id
        return _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date", "driver_id"])
    
    driver_ids = get_driver_ids(year) if driver_id is None else [driver_id]
    round_nums = range(1, get_num_rounds(year, completed_only=True) + 1) if round_num is None else [round_num]

    df_list = []
    for round_num in round_nums:
        for driver_id in driver_ids:
            df = get_pit_stop_times(year=year, round_num=round_num, driver_id=driver_id)
            if df.empty:
                continue
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)


def get_fastest_laps(year: int, round_num: Optional[int] = None):
    if round_num is not None:
        json = get_fastest_laps_json(year, round_num=round_num)
        df = convert_fastest_laps_json_to_df(json)
        _add_race_metadata(df=df, year=year, round_num=round_num)
        return _bring_columns_to_front(df, columns=["year", "round", "race_name", "circuit", "country", "city", "race_date"])
    else:
        num_rounds = get_num_rounds(year, completed_only=True)
        df_list = []
        for round_num in range(1, num_rounds + 1):
            df = get_fastest_laps(year, round_num=round_num)
            if df.empty:
                continue
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

def get_fastest_laps_range(start_year: int, end_year: int):
    df_list = []
    for year in range(start_year, end_year + 1):
        df_list.append(get_fastest_laps(year, round_num=None))
    return pd.concat(df_list, ignore_index=True)

