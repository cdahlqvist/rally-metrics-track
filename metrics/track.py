from metrics.runners import indicesstats_runner

def register(registry):
    registry.register_runner("indicesstats", indicesstats_runner.indicesstats)