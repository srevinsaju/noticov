import psycopg2

from noticov.backend.base import BaseConnection


class PostgreSQLConnection(BaseConnection):
    connection = "postgresql"

    def __init__(self, destination: str = None):
        super().__init__()
        self.conn = psycopg2.connect(destination)

        

