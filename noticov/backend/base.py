from typing import List

from noticov.covidstats.data import CovidData


class BaseConnection:
    connection: str = None

    def __init__(self):
        pass

    def add_data(self, data: CovidData):
        """
        Add a CovidData to the database..
        :param data:
        :type data:
        :return:
        :rtype:
        """
        raise NotImplementedError

    def add_multiple_data(self, data_sequence: List[CovidData]):
        """
        Add a sequence of Covid19Data to the database
        :param data_sequence:
        :type data_sequence:
        :return:
        :rtype:
        """
        raise NotImplementedError

    @property
    def get_connection_type(self):
        return self.connection

