from typing import List

import psycopg2

from noticov.backend.base import BaseConnection
from noticov.backend.tables import Table
from noticov.covidstats.data import CovidData, CovidDataAttr
from noticov.logging import make_logger


class PostgreSQLConnection(BaseConnection):
    connection = "postgresql"
    logger = make_logger("psql")

    def __init__(self, destination: str = None):
        super().__init__()
        self.conn = psycopg2.connect(destination)
        self.logger.info("Connection to postgresql database successful")
        self.initialize()

    def initialize(self):
        with self.conn.cursor() as cur:
            for table in Table:
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS {table} ("
                    f"{CovidDataAttr.ID} INT PRIMARY KEY, "
                    f"{CovidDataAttr.TIMESTAMP} INT, "
                    f"{CovidDataAttr.DEATHS} INT, "
                    f"{CovidDataAttr.TOTAL_CASES} INT, "
                    f"{CovidDataAttr.DISCHARGED} INT, "
                    f"{CovidDataAttr.LOCATION} VARCHAR(50), "
                    f")"
                )

    def add_data(self, data: CovidData):
        with self.conn.cursor() as cur:
            for table in Table:
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS {table} ("
                    f"{CovidDataAttr.ID} INT PRIMARY KEY, "
                    f"{CovidDataAttr.TIMESTAMP} INT, "
                    f"{CovidDataAttr.DEATHS} INT, "
                    f"{CovidDataAttr.TOTAL_CASES} INT, "
                    f"{CovidDataAttr.DISCHARGED} INT, "
                    f"{CovidDataAttr.LOCATION} VARCHAR(50), "
                    f")"
                )

    def add_multiple_data(self, data_sequence: List[CovidData]):
        # TODO: Improve the performance by doing only a single request
        for data in data_sequence:
            self.add_data(data)

    def get_all_covid_data(self, table: Table, location: str):
        with self.conn.cursor() as cur:
            # Check the current balance.
            cur.execute(f"SELECT "
                        f"{CovidDataAttr.TOTAL_CASES}, "
                        f"{CovidDataAttr.DEATHS}, "
                        f"{CovidDataAttr.DISCHARGED} FROM {table} "
                        f"WHERE {CovidDataAttr.LOCATION} = \"{location}\"")

