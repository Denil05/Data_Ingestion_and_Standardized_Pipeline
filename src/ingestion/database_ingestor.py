import pandas as pd
import sqlalchemy

class DatabaseIngestor:
    def __init__(self, connection_string):
        self.engine = sqlalchemy.create_engine(connection_string)

    def ingest(self, query):
        """Ingest data from a database using a SQL query."""
        df = pd.read_sql(query, self.engine)
        return df

# Example usage:
# db_ingestor = DatabaseIngestor('sqlite:///example.db')
# df = db_ingestor.ingest('SELECT * FROM my_table') 