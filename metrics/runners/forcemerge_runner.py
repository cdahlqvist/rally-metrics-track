import elasticsearch

def forcemerge(es, params):
    """
    Force merges indices matching an index pattern in Elasticsearch.

    It expects the parameter hash to contain the following keys:
        "index_pattern"        - Specifies the index pattern to forcemerge. Defaults to '*'
        "max_num_segments"     - Specifies the maximum number of segments to merge to.
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
