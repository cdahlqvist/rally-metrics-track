from influxdb import InfluxDBClient

import os
import logging

logger = logging.getLogger("track.metrics")

class InfluxDBCreateDatabaseRunner:
    def __init__(self):
        # Verify that the following environment variables are set:
        #  RALLY_INFLUXDB_HOST - defaults to 127.0.0.1
        #  RALLY_INFLUXDB_PORT - defaults to 8086
        #  RALLY_INFLUXDB_USER - defaults to 'root'
        #  RALLY_INFLUXDB_PASSWD - defaults to 'root'
        if "RALLY_INFLUXDB_HOST" in os.environ:
            self._host = os.environ["RALLY_INFLUXDB_HOST"]
        else:
            self._host = "127.0.0.1"

        if "RALLY_INFLUXDB_PORT" in os.environ:
            self._port = int(os.environ["RALLY_INFLUXDB_PORT"])
        else:
            self._port = 8086

        if "RALLY_INFLUXDB_USER" in os.environ:
            self._user = os.environ["RALLY_INFLUXDB_USER"]
        else:
            self._user = "root"

        if "RALLY_INFLUXDB_PASSWD" in os.environ:
            self._passwd = os.environ["RALLY_INFLUXDB_PASSWD"]
        else:
            self._passwd = "root"

        logger.info("InfluxDBCreateDatabaseRunner: Creating InfluxDB client.")
        self._influxdb_client = InfluxDBClient(host=self._host, port=self._port, username=self._user, password=self._passwd)
        logger.info("InfluxDBCreateDatabaseRunner: InfluxDB client created.")

    def __enter__(self):
        return self

    def __call__(self, es, params):
        """
        Runs one database creation operation against InfluxDB.

        :param es: The Elasticsearch client. Not used here
        :param params: A hash with all parameters. See below for details.
        :return: A hash with meta data for this bulk operation. See below for details.

        It expects a parameter dict with the following mandatory keys:

        * ``database``: the name of the database to create and clear.
        """

        # Set database if this is not already set
        if 'database' in params:
            database = params['database']
        else:
            database = "rally"

        logger.info("InfluxDBCreateDatabaseRunner: Check if database {} already exists.".format(database))
        database_exists = False

        try:
            dbs = self._influxdb_client.get_list_database()
        except BaseException:
            print("ERROR XXX")

        logger.info("InfluxDBCreateDatabaseRunner: Current databases: {}".format(dbs))

        for db in dbs:
            if db['name'] == database:
                database_exists = True

        if database_exists:
            logger.info("InfluxDBCreateDatabaseRunner: Drop database {}".format(database))
            self._influxdb_client.drop_database(database)
        else:
            logger.info("InfluxDBCreateDatabaseRunner: Database {} does not exist.".format(database))

        logger.info("InfluxDBCreateDatabaseRunner: Create database {}".format(database))
        self._influxdb_client.create_database(database)

        return 1, "ops"

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
