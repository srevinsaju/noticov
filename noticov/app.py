import os
import time

from dotenv import load_dotenv

from noticov.backend.base import BaseConnection
from noticov.backend.postgresql import PostgreSQLConnection
from noticov.covidstats.india import IndiaDistrictsCovidApi
from noticov.exceptions import DBStringNotFound


class NotiCovBackend:
    def __init__(
        self,
        connection: BaseConnection = None,
        sleep: int = 60 * 60,
    ):
        self.sleep = sleep
        self.conn = connection
        if connection is None:
            raise ConnectionError("BaseConnection failed to initialize..")

    def loop(self):
        """
        Something which will be run
        :return:
        :rtype:
        """
        ind_covid_api = IndiaDistrictsCovidApi()

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
