import psycopg2

from noticov.backend.base import BaseConnection
from noticov.backend.tables import Table
from noticov.covidstats.data import CovidData, CovidDataAttr


class PostgreSQLConnection(BaseConnection):
    connection = "postgresql"

    def __init__(self, destination: str = None):
        super().__init__()
        self.conn = psycopg2.connect(destination)
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
        pass



