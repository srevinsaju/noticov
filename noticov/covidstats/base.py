class BaseCovidApi:
    """
    A base class for Covid API. The location is set to none
    """

    location: str = None  # "global", "india"
    canonical_url: str = None  # the endpoint of the api

    def __init__(self):
        pass

    def get_data(self):
        """
        Gets the data from the api as a dictionary
        :return:
        :rtype:
        """
        raise NotImplementedError

    def initialize(self):
        """
        Do some tasks to initialize and api
        :return:
        :rtype:
        """
        pass
