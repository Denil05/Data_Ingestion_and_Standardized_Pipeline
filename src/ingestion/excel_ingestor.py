import pandas as pd

class ExcelIngestor:
    def __init__(self, file_path):
        self.file_path = file_path

    def ingest(self, sheet_name=0):
        """Ingest data from an Excel file."""
        df = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return df

# Example usage:
# excel_ingestor = ExcelIngestor('data/input/sample.xlsx')
# df = excel_ingestor.ingest() 