import pandas as pd
from sqlalchemy import create_engine

def ingest_sql(connection_string, table, logger):
    try:
        engine = create_engine(connection_string)
        df = pd.read_sql_table(table, engine)
        logger.info(f"Loaded SQL table: {table}")
        return df
    except Exception as e:
        logger.error(f"Failed to load SQL table {table}: {e}")
        return pd.DataFrame() 