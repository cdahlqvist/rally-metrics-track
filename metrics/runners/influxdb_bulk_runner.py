from influxdb import InfluxDBClient

import os
import logging

logger = logging.getLogger("track.metrics")

class InfluxDBBulkRunner:
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

        self._database = None

        logger.info("InfluxDBBulkRunner: Creating InfluxDB client.")
        self._influxdb_client = InfluxDBClient(host=self._host, port=self._port, username=self._user, password=self._passwd)

    def __enter__(self):
        return self

    def __call__(self, es, params):
        """
        Runs one bulk indexing operation against InfluxDB.

        :param es: The Elasticsearch client. Not used here
        :param params: A hash with all parameters. See below for details.
        :return: A hash with meta data for this bulk operation. See below for details.

        It expects a parameter dict with the following mandatory keys:

        * ``body``: containing all documents for the current bulk request.
        * ``bulk-size``: the number of documents in this bulk.
        * ``database``: the name of the database to insert this bulk request into. Defaults to 'rally'
        * ``time_precision``: the time precision used for points to be written. Defaults to 'ms'.
        """

        # Set database if this is not already set
        if 'database' in params:
            database = params['database']
        else:
            database = "rally"

        if self._database != database:
            self._influxdb_client.switch_database(database)
            self._database = database

        try:
            bulk_size = params["bulk-size"]
        except KeyError:
            raise exceptions.DataError(
                "Bulk parameter source did not provide a 'bulk-size' parameter. Please add it to your parameter source.")

        if "time_precision" in params.keys():
            time_precision = params['time_precision']
        else:
            time_precision = 'ms'

        logger.info("InfluxDBBulkRunner: Params: {}".format(params))

        body_size = len(params['body'])
        if body_size != bulk_size:
            raise exceptions.DataError("Bulk size ({}) does not correspond to the size of the body ({}).".format(bulk_size, body_size))

        response = {}
        if self._influxdb_client.write_points(params['body'], time_precision=time_precision, database=database, retention_policy=None, tags=None, batch_size=bulk_size, protocol='line'):
            response = { "weight": bulk_size, "unit": "docs", "bulk-size": bulk_size, "success": True, "success-count": bulk_size, "error-count": 0 }
        else:
            response = { "weight": bulk_size, "unit": "docs", "bulk-size": bulk_size, "success": False, "success-count": 0, "error-count": bulk_size }

        return response

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

