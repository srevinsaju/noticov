from noticov.covidstats.data import CovidData


class CourierNotifier:
    def __init__(self, token: str = None):
        if token is None:
            raise RuntimeError("$COURIER_AUTH_TOKEN environment variable is not defined. Please include that too")

    def notify(self, data: CovidData):
        pass
