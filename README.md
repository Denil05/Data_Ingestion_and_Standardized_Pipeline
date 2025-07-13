# Data Ingestion and Standardization Pipeline

## Overview
This project provides a modular pipeline for ingesting, validating, and standardizing data from multiple sources (CSV, Excel, SQL databases) into a unified schema. It is designed for extensibility, robust validation, and easy integration into larger data workflows.

## Features
- Ingest data from CSV, Excel, and SQL database sources
- Flexible column mapping and schema standardization
- Row-level data validation with customizable rules
- Logging of all pipeline steps and invalid data
- Modular codebase for easy extension (add new sources, validation, etc.)
- Configuration-driven: all sources and rules are defined in `config/config.yaml`

## Project Structure
```
Data_ingestion_and_standardize_pipeline/
  ├── config/
  │   └── config.yaml         # All pipeline configuration
  ├── data/
  │   └── processed/         # Output standardized data
  ├── logs/                  # Log files and reports
  ├── requirements.txt       # Python dependencies
  ├── src/
  │   ├── ingestion/
  │   │   ├── csv_ingestor.py
  │   │   ├── excel_ingestor.py
  │   │   ├── sql_ingestor.py
  │   │   └── database_ingestor.py
  │   ├── main.py            # Pipeline entry point
  │   ├── standardization/
  │   │   └── standardizer.py
  │   └── utils/
  │       └── logger.py
```

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Create required directories:**
   ```sh
   mkdir logs
   mkdir -p data/processed
   ```
4. **Configure the pipeline:**
   - Edit `config/config.yaml` to define your data sources, column mappings, and validation rules (see below).
5. **Run the pipeline:**
   ```sh
   python src/main.py
   ```
   - Use `--mode csv|excel|sql|all` to control which sources are processed.
   - Use `--config <path>` to specify a custom config file.

## Configuration (`config/config.yaml`)
- **csv_sources**/**excel_sources**: List of files, column mappings, and validation rules.
- **sql_sources**: List of database connections, tables, mappings, and validation.
- **standard_schema**: The unified column order for all outputs.

Example:
```yaml
csv_sources:
  - path: "data/raw/customers.csv"
    column_mapping:
      customer_id: id
      customer_name: name
      customer_email: email
      campaign_name: campaign
      signup_date: date
    validation:
      id:
        required: true
        type: int
      email:
        required: true
        type: str
        pattern: "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"
# ... (see full config/config.yaml for more)
```

## Pipeline Workflow
1. **Ingestion**: Reads data from each source using the appropriate ingestor module.
2. **Standardization**: Applies column mapping, reorders columns, and fills missing columns.
3. **Validation**: Checks each row against rules (type, required, regex, etc.).
4. **Output**: Writes valid rows to `data/processed/standardized_<source>_<i>.csv` and invalid rows to `logs/invalid_<source>_<i>.csv`.
5. **Logging**: All steps and errors are logged to `logs/pipeline.log`. A summary report is written to `logs/summary_report.txt`.

## Ingestion Modules
- **CSV**: `src/ingestion/csv_ingestor.py` (`CSVIngestor` class)
- **Excel**: `src/ingestion/excel_ingestor.py` (`ExcelIngestor` class)
- **SQL**: `src/ingestion/sql_ingestor.py` (`ingest_sql` function)
- **Database (generic)**: `src/ingestion/database_ingestor.py` (`DatabaseIngestor` class)

## Standardization & Validation
- `src/standardization/standardizer.py` handles column mapping, schema enforcement, and row validation.
- Validation rules are defined per column in the config file (type, required, regex, etc.).

## Logging
- Logging is set up in `src/utils/logger.py`.
- All pipeline actions, warnings, and errors are written to `logs/pipeline.log`.
- Invalid data is logged separately for review.

## Usage Examples
- **Run all sources:**
  ```sh
  python src/main.py --mode all
  ```
- **Run only CSV ingestion:**
  ```sh
  python src/main.py --mode csv
  ```
- **Custom config file:**
  ```sh
  python src/main.py --config my_config.yaml
  ```

## Extending the Pipeline
- Add new ingestion modules in `src/ingestion/` for other formats (e.g., JSON, Parquet).
- Add new validation rules in `standardizer.py` as needed.
- Update `config.yaml` to add new sources or schema changes.

## Troubleshooting
- Check `logs/pipeline.log` for errors and warnings.
- Invalid rows are saved in `logs/invalid_<source>_<i>.csv` for review.
- Ensure all required directories exist before running the pipeline.

## License
MIT License (add your license here) 