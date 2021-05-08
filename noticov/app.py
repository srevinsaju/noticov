
import os
from dotenv import load_dotenv

from noticov.backend.base import BaseConnection
from noticov.backend.postgresql import PostgreSQLConnection
from noticov.exceptions import DBStringNotFound


class NotiCovBackend:
    def __init__(self,
                 connection: BaseConnection = None):
        if connection is None:
            raise ConnectionError("BaseConnection failed to initialize..")

    def loop(self):
        """
        Something which will be run
        :return:
        :rtype:
        """
        pass

    def start(self):
        pass


def main():
    load_dotenv()

    db_string = os.getenv("DB_STRING")
    if not db_string:
        raise DBStringNotFound("$DB_STRING is not defined in the environment. Please define it with"
                               "DB_STRING=\"...\" python3 -m noticov to run this software")

    # initialize the psql connection
    psql = PostgreSQLConnection(destination=db_string)

    ncb = NotiCovBackend(connection=psql)





