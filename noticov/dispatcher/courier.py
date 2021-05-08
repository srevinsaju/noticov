from trycourier import Courier

from noticov.covidstats.data import CovidData


class CourierNotifier:
    def __init__(self, token: str = None):
        if token is None:
            raise RuntimeError(
                "$COURIER_AUTH_TOKEN environment variable is not defined. Please include that too"
            )

        self.client = Courier(auth_token=token)

    def notify(self, data: CovidData):
        raise NotImplementedError
