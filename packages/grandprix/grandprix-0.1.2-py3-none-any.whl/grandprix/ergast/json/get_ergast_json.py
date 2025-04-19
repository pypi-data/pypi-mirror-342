import requests

BASE_URL = "https://ergast.com/api/f1"

_cache = {}

def get_ergast_json(path: str, params: dict = None):
    url = f"{BASE_URL}/{path}.json"
    if url in _cache:
        return _cache[url]
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()["MRData"]
    _cache[url] = data
    return data


def get_season_schedule_json(year: int = 2024):
    return get_ergast_json(f"{year}")["RaceTable"]["Races"]


def get_race_results_json(year: int, round_num: int):
    races = get_ergast_json(f"{year}/{round_num}/results")["RaceTable"]["Races"]
    return races[0]["Results"] if races else []


def get_qualifying_results_json(year: int, round_num: int):
    races = get_ergast_json(f"{year}/{round_num}/qualifying")["RaceTable"]["Races"]
    return races[0]["QualifyingResults"] if races else []


def get_driver_standings_json(year: int, round_num: int = None):
    path = f"{year}/driverStandings" if round_num is None else f"{year}/{round_num}/driverStandings"
    lists = get_ergast_json(path)["StandingsTable"]["StandingsLists"]
    return lists[0]["DriverStandings"] if lists else []


def get_constructor_standings_json(year: int, round_num: int = None):
    path = f"{year}/constructorStandings" if round_num is None else f"{year}/{round_num}/constructorStandings"
    lists = get_ergast_json(path)["StandingsTable"]["StandingsLists"]
    return lists[0]["ConstructorStandings"] if lists else []


def get_lap_times_json(year: int, round_num: int, driver_id: str):
    races = get_ergast_json(f"{year}/{round_num}/drivers/{driver_id}/laps")["RaceTable"]["Races"]
    return races[0]["Laps"] if races else []


def get_pit_stop_times_json(year: int, round_num: int, driver_id: str):
    path = f"{year}/{round_num}/drivers/{driver_id}/pitstops" if driver_id else f"{year}/{round_num}/pitstops"
    races = get_ergast_json(path)["RaceTable"]["Races"]
    return races[0]["PitStops"] if races else []


def get_fastest_laps_json(year: int, round_num: int):
    results = get_race_results_json(year, round_num)
    return [r for r in results if "FastestLap" in r]

def get_drivers_json(year: int):
    data = get_ergast_json(f"{year}/drivers")
    return data["DriverTable"]["Drivers"]
