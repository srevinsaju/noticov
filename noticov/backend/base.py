from typing import List

from noticov.backend.tables import Tables
from noticov.covidstats.data import CovidData, CovidDataList


class BaseConnection:
    connection: str = None

    def __init__(self):
        pass

    def initialize(self):
        """
        Create the tables and databases here
        :return:
        :rtype:
        """
        raise NotImplementedError

    def add_data(self, data: CovidData, table: Tables):
        """
        Add a CovidData to the database..
        :param table:
        :type table:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def add_multiple_data(self, data_sequence: CovidDataList, table: Tables):
        """
        Add a sequence of Covid19Data to the database
        :param table:
        :type table:
        :param data_sequence:
        :type data_sequence:
        :return:
        :rtype:
        """
        raise NotImplementedError

    @property
    def get_connection_type(self):
        """
        Returns the names of the connection
        :return:
        :rtype:
        """

        return self.connection

    def get_all_covid_data(self, table: Tables, location: str) -> CovidDataList:
        """
        Gets all the covid data from the database
        :param table:
        :type table:
        :param location:
        :type location:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def get_top_covid_cases(self, table: Tables) -> CovidDataList:
        """
        Returns the top 7 covid cases in the state wise if available
        :param table:
        :type table:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def get_latest_covid_data(self, table: Tables, location: str) -> CovidData:
        """
        Gets the last saved covid data
        :param table:
        :type table:
        :param location:
        :type location:
        :return:
        :rtype:
        """
        raise NotImplementedError
