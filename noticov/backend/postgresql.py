import psycopg2

from noticov.backend.base import BaseConnection
from noticov.backend.tables import Table
from noticov.covidstats.data import CovidData


class PostgreSQLConnection(BaseConnection):
    connection = "postgresql"

    def __init__(self, destination: str = None):
        super().__init__()
        self.conn = psycopg2.connect(destination)

    def initialize(self):
        with self.conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {Table.INDIA} (id INT PRIMARY KEY, balance INT)"
            )
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {Table.WORLD} (id INT PRIMARY KEY, balance INT)"
            )

    def add_data(self, data: CovidData):
        pass



