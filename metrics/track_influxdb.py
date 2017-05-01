from eventdata.runners.influxdb_bulk_runner import InfluxDBBulkRunner
from eventdata.runners.influxdb_compaction_runner import InfluxDBCompactionRunner
from eventdata.runners.influxdb_database_size_runner import InfluxDBDatabaseSizeRunner

def register(registry):
    registry.register_runner("influxdb_bulk", InfluxDBBulkRunner())
    registry.register_runner("influxdb_compaction", InfluxDBCompactionRunner())
    registry.register_runner("influxdb_database_size", InfluxDBDatabaseSizeRunner())



