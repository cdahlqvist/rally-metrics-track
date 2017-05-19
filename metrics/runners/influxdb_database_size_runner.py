from influxdb import InfluxDBClient

import os
import logging
import time

logger = logging.getLogger("track.metrics")

class InfluxDBDatabaseSizeRunner:
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

        logger.info("InfluxDBDatabaseSizeRunner: Creating InfluxDB client.")
        self._influxdb_client = InfluxDBClient(host=self._host, port=self._port, username=self._user, password=self._passwd)
        logger.info("InfluxDBDatabaseSizeRunner: InfluxDB client created.")

    def __enter__(self):
        return self

    def __call__(self, es, params):
        """
        Runs one get database size operation InfluxDB.

        :param es: The Elasticsearch client. Not used here
        :param params: A hash with all parameters. See below for details.
        :return: A hash with meta data for this bulk operation. See below for details.

        It expects a parameter dict with the following mandatory keys:

        * ``index``: the name of the database to get size of.
        * ``sleep``: the number of seconds to sleep before retrieving stats. Defaults to 0.
        """
        if 'sleep' in params:
            time.sleep(int(params['sleep']))

        if 'index' in params:
            database = params['index']
        else:
            database = "rally"

        response = {
            "weight": 1,
            "unit": "ops",
            "index_pattern": database
        }

        query = 'SELECT diskBytes, writePointsOk FROM "shard" GROUP BY "database" ORDER BY time DESC LIMIT 1'

        logger.info("[InfluxDBDatabaseSizeRunner] Query: {}".format(query))

        response = self._influxdb_client.query(query, database="_internal").raw

        logger.info("[InfluxDBDatabaseSizeRunner] Response: {}".format(response))

        response['total_doc_count'] = 0
        response['total_size_bytes'] = 0

        if 'series' in response.keys():
            for item in response['series']:
                if item['tags']['database'] == database
                    col_list = item['columns']
                    val_list = item['values'][0]

                    response['total_doc_count'] = val_list[col_list.index("writePointsOk")]
                    response['total_size_bytes'] = val_list[col_list.index("diskBytes")]

        logger.info("[InfluxDBDatabaseSizeRunner] Database: {} Points: {} Size: {}".format(database, response['total_doc_count'], response['total_size_bytes']))

        return response

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
