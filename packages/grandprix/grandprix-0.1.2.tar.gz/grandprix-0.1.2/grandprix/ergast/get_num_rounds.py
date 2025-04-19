from .json import get_season_schedule_json, get_race_results_json

def get_num_rounds(year: int, completed_only: bool = False):
    json = get_season_schedule_json(year)
    races = json["MRData"]["RaceTable"]["Races"]

    if not completed_only:
        return len(races)

    count = 0
    for race in races:
        round_num = int(race["round"])
        results = get_race_results_json(year, round_num)
        if results["MRData"]["RaceTable"]["Races"]:
            if results["MRData"]["RaceTable"]["Races"][0].get("Results"):
                count += 1
    return count
