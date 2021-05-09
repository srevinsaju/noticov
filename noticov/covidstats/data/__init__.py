import time
from enum import Enum
from typing import Dict, Optional, Union


class CovidData:
    def __init__(
        self,
        location: str = None,
        total_cases: int = None,
        deaths: int = None,
        discharged: int = None,
        timestamp: int = None,
    ):
        self.location = location
        self.total_cases = total_cases
        self.deaths = deaths
        self.discharged = discharged
        if timestamp is None:
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            "timestamp": self.timestamp,
            "location": self.location,
            "total_cases": self.total_cases,
            "deaths": self.deaths,
            "discharged": self.discharged,
        }

    @property
    def new_cases_today(self):
        """
        Returns the new cases today
        :return:
        :rtype:
        """
        return self.total_cases - self.discharged

    def __repr__(self):
        return "CovidData(location={}, tc={}, dc={}, deaths={}, timestamp={})".format(
            self.location,
            self.total_cases,
            self.discharged,
            self.deaths,
            self.timestamp,
        )


class CovidDataList:
    def __init__(self):
        self._list = []

    def push(self, data: CovidData):
        assert isinstance(data, CovidData)

        self._list.append(data)

    def pop(self) -> CovidData:
        return self._list.pop()

    def count(self) -> int:
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def copy(self):
        cdl = CovidDataList()
        cdl._list = self._list.copy()
        return cdl


class CovidDataAttr(Enum):
    ID = "id"
    LOCATION = "loc"
    TIMESTAMP = "ts"
    TOTAL_CASES = "total_cases"
    DEATHS = "deaths"
    DISCHARGED = "discharged"
