class CovidData:
    def __init__(
            self,
            location: str = None,
            current_active_cases: int = None,
            current_deaths: int = None,
    ):
        self.location = location
        self.current_active_cases = current_active_cases
        self.current_deaths = current_deaths

    def __repr__(self):
        return "CovidData(location={}, {}, {})".format(self.location, self.current_active_cases, self.current_deaths)