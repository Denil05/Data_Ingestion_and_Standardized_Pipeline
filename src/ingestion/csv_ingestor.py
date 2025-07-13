import pandas as pd

class CSVIngestor:
    def __init__(self, file_path):
        self.file_path = file_path

    def ingest(self):
        """Ingest data from a CSV file."""
        df = pd.read_csv(self.file_path)
        return df

# Example usage:
# csv_ingestor = CSVIngestor('data/input/sample.csv')
# df = csv_ingestor.ingest() 