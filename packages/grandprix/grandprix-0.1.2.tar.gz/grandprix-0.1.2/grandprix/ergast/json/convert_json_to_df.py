import pandas as pd

def convert_season_schedule_json_to_df(races):
    flat = [{
        "round": race["round"],
        "race_name": race["raceName"],
        "circuit": race["Circuit"]["circuitName"],
        "country": race["Circuit"]["Location"]["country"],
        "city": race["Circuit"]["Location"]["locality"],
        "date": race["date"]
    } for race in races]
    return pd.DataFrame(flat)


def convert_race_results_json_to_df(results):
    if not results:
        return pd.DataFrame()
    flat = [{
        "position": r.get("position"),
        "driver_id": r["Driver"]["driverId"],
        "full_name": f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
        "constructor": r["Constructor"]["name"],
        "grid": r.get("grid"),
        "status": r.get("status"),
        "finish_time": r.get("Time", {}).get("time")
    } for r in results]
    return pd.DataFrame(flat)


def convert_qualifying_results_json_to_df(results):
    if not results:
        return pd.DataFrame()
    flat = [{
        "position": r["position"],
        "driver": f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
        "constructor": r["Constructor"]["name"],
        "q1_time": r.get("Q1"),
        "q2_time": r.get("Q2"),
        "q3_time": r.get("Q3")
    } for r in results]
    return pd.DataFrame(flat)


def convert_driver_standings_json_to_df(drivers):
    if not drivers:
        return pd.DataFrame()
    flat = [{
        "position": d["position"],
        "driver": f"{d['Driver']['givenName']} {d['Driver']['familyName']}",
        "points": d["points"],
        "wins": d["wins"],
        "constructor": d["Constructors"][0]["name"]
    } for d in drivers]
    return pd.DataFrame(flat)


def convert_constructor_standings_json_to_df(constructors):
    if not constructors:
        return pd.DataFrame()
    flat = [{
        "position": c["position"],
        "constructor": c["Constructor"]["name"],
        "points": c["points"],
        "wins": c["wins"]
    } for c in constructors]
    return pd.DataFrame(flat)


def convert_lap_times_json_to_df(laps):
    if not laps:
        return pd.DataFrame()
    flat = [{
        "lap": lap["number"],
        "position": timing["position"],
        "lap_time": timing["time"],
        "driver_id": timing["driverId"]
    } for lap in laps for timing in lap["Timings"]]
    return pd.DataFrame(flat)


def convert_pit_stop_times_json_to_df(stops):
    if not stops:
        return pd.DataFrame()
    flat = [{
        "driver_id": s["driverId"],
        "lap": s["lap"],
        "stop_number": s["stop"],
        "duration": s["duration"],
        "pit_time": s["time"]
    } for s in stops]
    return pd.DataFrame(flat)


def convert_fastest_laps_json_to_df(results):
    if not results:
        return pd.DataFrame()
    flat = [{
        "position": r["position"],
        "driver": f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
        "constructor": r["Constructor"]["name"],
        "fastest_lap_rank": r["FastestLap"]["rank"],
        "fastest_lap_time": r["FastestLap"]["Time"]["time"],
        "fastest_lap_speed": r["FastestLap"]["AverageSpeed"]["speed"]
    } for r in results if "FastestLap" in r]
    return pd.DataFrame(flat)


def convert_drivers_json_to_df(drivers):
    if not drivers:
        return pd.DataFrame()
    flat = [{
        "driver_id": d["driverId"],
        "first_name": d["givenName"],
        "last_name": d["familyName"],
        "full_name": f"{d['givenName']} {d['familyName']}",
        "nationality": d["nationality"],
        'date_of_birth': d['dateOfBirth'],
        'url': d['url'],
    } for d in drivers]
    return pd.DataFrame(flat)
