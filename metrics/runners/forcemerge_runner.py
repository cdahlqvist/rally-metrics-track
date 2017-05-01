import elasticsearch

def deleteindex(es, params):
    """
    Deletes all indices in Elasticsearch matching the specified index pattern.

    It expects the parameter hash to contain the following key:
        "index_pattern"        - Specifies the index pattern to delete. Defaults to 'elasticlogs-*'
    """
    if 'index_pattern' in params:
        index_pattern = params['index_pattern']
    else:
        index_pattern = "*"

    if 'max_num_segments' in params:
        es.indices.forcemerge(index=index_pattern, max_num_segments=params["max_num_segments"])
    else:
        es.indices.forcemerge(index=index_pattern)

    return 1, "ops"
