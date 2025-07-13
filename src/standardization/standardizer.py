import re
import pandas as pd

def validate_row(row, validation_rules):
    errors = {}
    for col, rules in validation_rules.items():
        val = row.get(col)
        if rules.get('required') and (pd.isnull(val) or val == ''):
            errors[col] = 'Missing required value'
        if 'type' in rules:
            if rules['type'] == 'int':
                try:
                    int(val)
                except (ValueError, TypeError):
                    errors[col] = 'Invalid int'
            elif rules['type'] == 'str':
                if not isinstance(val, str):
                    errors[col] = 'Invalid str'
        if 'pattern' in rules and isinstance(val, str):
            if not re.match(rules['pattern'], val):
                errors[col] = 'Pattern mismatch'
    return errors

def standardize(df, standard_schema, logger, column_mapping=None, validation=None, invalid_log_path=None):
    # Apply column mapping if provided
    if column_mapping:
        df = df.rename(columns=column_mapping)
    df = df.rename(columns=lambda x: x.strip().lower())
    # Add missing columns
    for col in standard_schema:
        if col not in df.columns:
            df[col] = None
            logger.warning(f"Missing column {col} added as None")
    # Reorder columns
    df = df[standard_schema]
    # Data validation
    valid_rows = []
    invalid_rows = []
    for idx, row in df.iterrows():
        errors = validate_row(row, validation or {})
        if errors:
            row_dict = row.to_dict()
            row_dict['__errors__'] = errors
            invalid_rows.append(row_dict)
            logger.error(f"Invalid row at index {idx}: {errors}")
        else:
            valid_rows.append(row)
    valid_df = pd.DataFrame(valid_rows, columns=standard_schema)
    invalid_df = pd.DataFrame(invalid_rows)
    # Log invalid rows to a separate file if path provided
    if invalid_log_path and not invalid_df.empty:
        invalid_df.to_csv(invalid_log_path, index=False)
        logger.info(f"Logged {len(invalid_df)} invalid rows to {invalid_log_path}")
    return valid_df, invalid_df 