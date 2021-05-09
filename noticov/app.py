import os
import time

from dotenv import load_dotenv

from noticov.backend.base import BaseConnection
from noticov.backend.postgresql import PostgreSQLConnection
from noticov.backend.tables import Tables
from noticov.covidstats.india import IndiaDistrictsCovidApi
from noticov.dispatcher.courier import CourierNotifier
from noticov.exceptions import DBStringNotFound
from noticov.logging import make_logger


class NotiCovBackend:
    logger = make_logger("backend")
    def __init__(
        self,
        connection: BaseConnection = None,
        notifier: CourierNotifier = None,
        sleep: int = 60 * 30,
    ):
        self.sleep = sleep
        self.conn = connection
        self.notifier = notifier
        if notifier is None:
            self.logger.warning("No notifier passed. Notifications will be disabled.")

        if connection is None:
            raise ConnectionError("BaseConnection failed to initialize..")

    def loop(self):
        """
        Something which will be run
        :return:
        :rtype:
        """
        ind_covid_api = IndiaDistrictsCovidApi()
        data_stream = ind_covid_api.get_data()

        while data_stream.count() > 0:

            data = data_stream.pop()
            latest_stored_data = self.conn.get_latest_covid_data(table=Tables.INDIA, location=data.location)
            if latest_stored_data.deaths < data.deaths:
                if self.notifier is not None:
                    self.notifier.notify(data, old_data=latest_stored_data)
            elif latest_stored_data.total_cases < data.total_cases:
                if self.notifier is not None:
                    self.notifier.notify(data, old_data=latest_stored_data)
            elif latest_stored_data.discharged < data.discharged:
                if self.notifier is not None:
                    self.notifier.notify(data, old_data=latest_stored_data)

        self.conn.add_multiple_data(data_stream, table=Tables.INDIA)

    def start(self):
        while True:
            try:
                self.loop()
                time.sleep(self.sleep)
            except (KeyboardInterrupt, EOFError):
                return


def main():
    load_dotenv()

    db_string = os.getenv("DB_STRING")
    if not db_string:
        raise DBStringNotFound(
            "$DB_STRING is not defined in the environment. Please define it with"
            'DB_STRING="..." python3 -m noticov to run this software'
        )

    try:
        sleep_time = int(os.getenv("SLEEP_TIME") or 60 * 60)
    except ValueError:
        raise RuntimeError("$SLEEP_TIME is not valid integer")

    # initialize the psql connection
    psql = PostgreSQLConnection(destination=db_string)

    ncb = NotiCovBackend(connection=psql, sleep=sleep_time)
    ncb.start()
