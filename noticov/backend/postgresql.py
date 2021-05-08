import uuid
from typing import List, Dict

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer
from sqlalchemy.sql import FromClause

from noticov.backend.base import BaseConnection
from noticov.backend.tables import Tables
from noticov.covidstats.data import CovidData, CovidDataAttr, CovidDataList
from noticov.logging import make_logger


class PostgreSQLConnection(BaseConnection):
    connection = "postgresql"
    logger = make_logger("psql")

    def __init__(self, destination: str = None):
        super().__init__()
        self.db = create_engine(destination)
        self.conn = self.db.connect()
        self.meta = MetaData(self.db)
        self.tables: Dict[Tables, Table] = dict()

        self.logger.info("Connection to postgresql database successful")
        self.initialize()

    def initialize(self):
        for table in Tables:
            self.tables[table] = _table = Table(
                Tables.INDIA,
                self.meta,
                Column(CovidDataAttr.ID, String),
                Column(CovidDataAttr.LOCATION, String),
                Column(CovidDataAttr.TOTAL_CASES, Integer),
                Column(CovidDataAttr.DISCHARGED, Integer),
                Column(CovidDataAttr.DEATHS, Integer),
                Column(CovidDataAttr.TIMESTAMP, Integer),
            )

            _table.create()

    def add_data(self, data: CovidData, table: Tables):
        self.conn.execute(
            self.tables[table]
            .insert()
            .values(
                (
                    (CovidDataAttr.ID, uuid.uuid4()),
                    (CovidDataAttr.TIMESTAMP, data.timestamp),
                    (CovidDataAttr.DEATHS, data.deaths),
                    (CovidDataAttr.TOTAL_CASES, data.total_cases),
                    (CovidDataAttr.DISCHARGED, data.discharged),
                    (CovidDataAttr.LOCATION, data.location),
                )
            )
        )
        self.conn.commit()

    def add_multiple_data(self, data_sequence: CovidDataList, table: Tables):
        # TODO: Improve the performance by doing only a single request
        for data in data_sequence:
            self.add_data(data, table)

    def get_all_covid_data(self, table: Tables, location: str):
        # TODO: looks sus.. pls fix someone 🥺🥺🥺
        where_expression = self.tables[table].c.loc == location

        resultset = self.conn.execute(
            self.tables[table].select().where(where_expression)
        )
        self.logger.debug(f"Received {len(resultset)} rows from {self.connection}")
        # TODO: fix this part, is messed up again
        return resultset

    def get_latest_covid_data(self, table: Tables, location: str):
        # TODO: looks sus.. pls fix someone 🥺🥺🥺
        where_expression = self.tables[table].c.loc == location

        resultset = self.conn.execute(
            self.tables[table]
            .select()
            .where(where_expression)
            .order_by(CovidDataAttr.TIMESTAMP)
            .limit(1)
        )
        self.logger.debug(f"Received {len(resultset)} rows from {self.connection}")
        # TODO: fix this part, is messed up again
        return resultset
