from metrics.runners import indicesstats_runner
from metrics.runners import forcemerge_runner

def register(registry):
    registry.register_runner("indicesstats", indicesstats_runner.indicesstats)
    registry.register_runner("forcemerge", forcemerge_runner.forcemerge)