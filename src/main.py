import yaml
import os
import argparse
from utils.logger import get_logger
from ingestion.csv_ingestor import ingest_csv
from ingestion.sql_ingestor import ingest_sql
from ingestion.excel_ingestor import ingest_excel
from standardization.standardizer import standardize

def main():
    parser = argparse.ArgumentParser(description="Data Ingestion and Standardization Pipeline")
    parser.add_argument('--config', type=str, default='config/config.yaml', help='Path to config YAML file')
    parser.add_argument('--mode', type=str, choices=['all', 'csv', 'excel', 'sql'], default='all', help='Which sources to process')
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)
    logger = get_logger()
    all_dfs = []
    all_invalids = []
    summary = []

    # Ingest CSVs
    if args.mode in ['all', 'csv']:
        for i, src in enumerate(config.get("csv_sources", [])):
            df = ingest_csv(src["path"], logger)
            column_mapping = src.get("column_mapping")
            validation = src.get("validation")
            valid_df, invalid_df = standardize(
                df,
                config["standard_schema"],
                logger,
                column_mapping=column_mapping,
                validation=validation,
                invalid_log_path=f"logs/invalid_csv_{i}.csv"
            )
            valid_df.to_csv(f"data/processed/standardized_csv_{i}.csv", index=False)
            logger.info(f"Saved standardized_csv_{i}.csv")
            all_dfs.append(valid_df)
            all_invalids.append(invalid_df)
            summary.append({
                'source': src["path"],
                'rows_processed': len(df),
                'valid_rows': len(valid_df),
                'invalid_rows': len(invalid_df)
            })

    # Ingest Excel files
    if args.mode in ['all', 'excel']:
        for i, src in enumerate(config.get("excel_sources", [])):
            df = ingest_excel(src["path"], logger)
            column_mapping = src.get("column_mapping")
            validation = src.get("validation")
            valid_df, invalid_df = standardize(
                df,
                config["standard_schema"],
                logger,
                column_mapping=column_mapping,
                validation=validation,
                invalid_log_path=f"logs/invalid_excel_{i}.csv"
            )
            valid_df.to_csv(f"data/processed/standardized_excel_{i}.csv", index=False)
            logger.info(f"Saved standardized_excel_{i}.csv")
            all_dfs.append(valid_df)
            all_invalids.append(invalid_df)
            summary.append({
                'source': src["path"],
                'rows_processed': len(df),
                'valid_rows': len(valid_df),
                'invalid_rows': len(invalid_df)
            })

    # Ingest SQL tables
    if args.mode in ['all', 'sql']:
        for i, src in enumerate(config.get("sql_sources", [])):
            df = ingest_sql(src["connection_string"], src["table"], logger)
            column_mapping = src.get("column_mapping")
            validation = src.get("validation")
            valid_df, invalid_df = standardize(
                df,
                config["standard_schema"],
                logger,
                column_mapping=column_mapping,
                validation=validation,
                invalid_log_path=f"logs/invalid_sql_{i}.csv"
            )
            valid_df.to_csv(f"data/processed/standardized_sql_{i}.csv", index=False)
            logger.info(f"Saved standardized_sql_{i}.csv")
            all_dfs.append(valid_df)
            all_invalids.append(invalid_df)
            summary.append({
                'source': src["table"],
                'rows_processed': len(df),
                'valid_rows': len(valid_df),
                'invalid_rows': len(invalid_df)
            })

    # Output summary report
    with open("logs/summary_report.txt", "w") as f:
        for item in summary:
            f.write(f"Source: {item['source']}\n")
            f.write(f"  Rows processed: {item['rows_processed']}\n")
            f.write(f"  Valid rows: {item['valid_rows']}\n")
            f.write(f"  Invalid rows: {item['invalid_rows']}\n\n")
    logger.info("Summary report written to logs/summary_report.txt")

if __name__ == "__main__":
    main() 