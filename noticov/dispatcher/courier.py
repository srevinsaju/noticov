from trycourier import Courier

from noticov.covidstats.data import CovidData
from noticov.logging import make_logger


class CourierNotifier:
    logger = make_logger("courier")

    def __init__(self, token: str = None):
        if token is None:
            raise RuntimeError(
                "$COURIER_AUTH_TOKEN environment variable is not defined. Please include that too"
            )

        self.client = Courier(auth_token=token)

    def notify(self, data: CovidData, old_data: CovidData):
        current_cases = data.total_cases
        if data.total_cases is not None and old_data.total_cases is not None:
            current_cases = data.total_cases - old_data.total_cases
        resp = self.client.send(
            event="T5VSYRFG3FMQCZQN481A671QK86A",
            recipient="ae918498-110c-463a-bed2-f6d8529e4348",
            profile={"discord": {"channel_id": "760033237422309419"}},
            data={
                "current_cases": str(current_cases),
                "deaths": str(data.deaths),
                "additional_message": "Stay safe, friend!",
                "location": str(data.location),
            },
        )

        self.logger.info(
            f"Sending courier notification, with message id {resp.get('message_id')}"
        )

    def notify_deaths_changed(self, data: CovidData):
        raise NotImplementedError

    def notify_total_cases_changed(self, data: CovidData):
        raise NotImplementedError
