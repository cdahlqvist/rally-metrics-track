from metrics.runners import indicesstats_runner
from metrics.runners import forcemerge_runner
from metrics.runners.influxdb_bulk_runner import InfluxDBBulkRunner
from metrics.runners.influxdb_create_database_runner import InfluxDBCreateDatabaseRunner

def register(registry):
    registry.register_runner("indicesstats", indicesstats_runner.indicesstats)
    registry.register_runner("forcemerge", forcemerge_runner.forcemerge)
    registry.register_runner("influxdb_bulk", InfluxDBBulkRunner())
    registry.register_runner("influxdb_create_database", InfluxDBCreateDatabaseRunner())
