from metrics.runners import indicesstats_runner
from metrics.runners import forcemerge_runner
from metrics.runners.influxdb_bulk_runner import InfluxDBBulkRunner
from metrics.runners.influxdb_create_database_runner import InfluxDBCreateDatabaseRunner
from metrics.runners.influxdb_database_size_runner import InfluxDBDatabaseSizeRunner

def register(registry):
    registry.register_runner("indicesstats", indicesstats_runner.indicesstats)
    registry.register_runner("forcemerge", forcemerge_runner.forcemerge)
    registry.register_runner("influxdb_bulk", InfluxDBBulkRunner())
    registry.register_runner("influxdb_create_database", InfluxDBCreateDatabaseRunner())
    registry.register_runner("influxdb_database_size", InfluxDBDatabaseSizeRunner())
