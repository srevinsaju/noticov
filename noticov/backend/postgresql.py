import uuid
from typing import Dict, Optional, List

from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import Table, Column, String, MetaData, Integer

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
        if destination.startswith("cockroach"):
            self.logger.info("Detected CockroachDB psql database string")

        self.conn = self.db.connect()
        self.meta = MetaData(self.db)
        self.tables: Dict[Tables, Table] = dict()

        self.logger.info("Connection to postgresql database successful")
        self.initialize()

    def initialize(self):
        for table in Tables:
            self.tables[table] = _table = Table(
                table.value,
                self.meta,
                Column(CovidDataAttr.ID.value, String),
                Column(CovidDataAttr.LOCATION.value, String),
                Column(CovidDataAttr.TOTAL_CASES.value, Integer),
                Column(CovidDataAttr.DISCHARGED.value, Integer),
                Column(CovidDataAttr.DEATHS.value, Integer),
                Column(CovidDataAttr.TIMESTAMP.value, Integer),
            )

        self.meta.create_all()

    def add_data(self, data: CovidData, table: Tables):
        self.conn.execute(
            self.tables[table]
            .insert()
            .values(
                **dict(
                    (
                        (CovidDataAttr.ID.value, uuid.uuid4().hex),
                        (CovidDataAttr.TIMESTAMP.value, data.timestamp),
                        (CovidDataAttr.DEATHS.value, data.deaths),
                        (CovidDataAttr.TOTAL_CASES.value, data.total_cases),
                        (CovidDataAttr.DISCHARGED.value, data.discharged),
                        (CovidDataAttr.LOCATION.value, data.location),
                    )
                )
            )
        )

    def add_multiple_data(self, data_sequence: CovidDataList, table: Tables):
        # TODO: Improve the performance by doing only a single request
        for data in data_sequence:
            self.add_data(data, table)

    def _parse_psql_result_set(self, resultset) -> CovidDataList:
        values = resultset.fetchall()
        self.logger.debug(f"Received {len(values)} row from {self.connection}")
        cdl = CovidDataList()
        for record in values:
            cdl.push(
                CovidData(
                    location=record[1],
                    total_cases=record[2],
                    discharged=record[3],
                    deaths=record[4],
                    timestamp=record[5],
                )
            )
        return cdl

    def get_all_covid_data(self, table: Tables, location: str) -> CovidDataList:
        # TODO: looks sus.. pls fix someone 🥺🥺🥺
        where_expression = self.tables[table].c.loc == location

        resultset = self.conn.execute(
            self.tables[table].select().where(where_expression).limit(30)
        )

        cdl = self._parse_psql_result_set(resultset)
        return cdl

    def get_top_covid_cases(self, table: Tables) -> CovidDataList:
        resultset = self.conn.execute(
            self.tables[table]
            .select()
            .where(self.tables[table].c.loc != "India")
            .order_by(desc(CovidDataAttr.TIMESTAMP.value))
            .order_by(desc(CovidDataAttr.TOTAL_CASES.value))
            .limit(7)
        )

        cdl = self._parse_psql_result_set(resultset)
        return cdl

    def get_all_latest_covid_cases(self, table: Tables) -> CovidDataList:
        resultset = self.conn.execute(
            self.tables[table]
                .select()
                .where(self.tables[table].c.loc != "India")
                .distinct(self.tables[table].c.loc)
                .order_by(desc(CovidDataAttr.TOTAL_CASES.value))
                .order_by(desc(CovidDataAttr.TOTAL_CASES.value))
                .order_by(desc(CovidDataAttr.TIMESTAMP.value))

        )

        cdl = self._parse_psql_result_set(resultset)
        return cdl

    def get_available_states_countries(self, table: Tables) -> List[str]:
        resultset = self.conn.execute(
            self.tables[table]
            .select()
            .distinct(self.tables[table].c.loc)
            .order_by(CovidDataAttr.LOCATION.value)
        )

        return [record[1] for record in resultset.fetchall()]

    def get_latest_covid_data(
        self, table: Tables, location: str
    ) -> Optional[CovidData]:
        # TODO: looks sus.. pls fix someone 🥺🥺🥺
        where_expression = self.tables[table].c.loc == location

        resultset = self.conn.execute(
            self.tables[table]
            .select()
            .where(where_expression)
            .order_by(desc(CovidDataAttr.TIMESTAMP.value))
            .limit(1)
        )
        values = resultset.fetchall()
        assert len(values) <= 1
        if len(values) == 0:
            return None
        self.logger.debug(f"Received {len(values)} row from {self.connection}")
        record = values[0]
        return CovidData(
            location=record[1],
            total_cases=record[2],
            discharged=record[3],
            deaths=record[4],
            timestamp=record[5],
        )

    def reset_tables(self):
        for i in self.tables:
            self.logger.info("Dropping table {}".format(i.value))
            self.tables[i].drop()
        self.logger.info("Data resetted successfully!")
