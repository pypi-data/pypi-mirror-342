from ..utils import Filters
from typing import Union, List, Tuple, Set
from .get_drivers import get_drivers, add_driver_metadata
from .get_schedule import get_schedule
import pandas as pd

class Ergast:
    def __init__(
            self,
            years: Union[int, List[int], Tuple[int, int], Set[int], range, None] = None,
            rounds: Union[int, List[int], Tuple[int, int], Set[int], range, None] = None,
            drivers: Union[str, List[str], Set[str], None] = None,
            circuits: Union[str, List[str], Set[str], None] = None,
            teams: Union[str, List[str], Set[str], None] = None
    ):
        self.filters = {
            "year": Filters.from_any("year", values=years),
            "round": Filters.from_any("round", values=rounds),
            "driver": Filters.from_any("driver", values=drivers),
            "circuit": Filters.from_any("circuit", values=circuits),
            "team": Filters.from_any("team", values=teams)
        }

    def _apply_filters(self, df: pd.DataFrame, exclude: Union[str, List[str], None] = None):
        if exclude is None:
            exclude = set()
        elif isinstance(exclude, str):
            exclude = {exclude}
        else:
            exclude = set(exclude)

        for filter_name, filter in self.filters.items():
            if filter_name not in exclude:
                df = filter.apply(df)
        return df

    @property
    def schedule(self):
        df = get_schedule(years=self.filters["year"])
        return self._apply_filters(df, exclude=["year"])

    @property
    def drivers(self):
        df = get_drivers(drivers=self.filters["driver"])
        return self._apply_filters(df, exclude=["driver"])

    @property
    def circuits(self):
        return get_circuits(circuits=self.circuit_filter)

    @property
