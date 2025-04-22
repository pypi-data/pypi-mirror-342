# snowpack_stack/type_mapper.py
def map_db_type(source, data_type, destination):
    """
    Map the data_type from the source database to a type for the destination.
    For now, we support a simple mapping for postgres -> bigquery.
    """
    mapping = {
        "bigint": "bigint",
        "integer": "integer",
        "timestamp with time zone": "timestamp",
        "timestamp without time zone": "timestamp",
        "text": "text",
        "numeric": "numeric",
        "double precision": "float64",
    }
    return mapping.get(data_type, data_type)
