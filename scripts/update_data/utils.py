from datetime import datetime, timezone
from typing import Optional, Dict, Any, Set
import logging
from logging.handlers import RotatingFileHandler
import os

import pandas as pd
import requests


def to_mysql_ts(ts: Optional[str]) -> Optional[str]:
    if ts is not None:
        sql_ts = (
            datetime.fromisoformat(ts[:-1])
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        return sql_ts
    else:
        return None


def update_destination_table(df: pd.DataFrame, table: str, cur, metric_config: Optional[Dict[str, Any]] = None) -> None:
    if df.empty:
        raise ValueError("Cannot update table with empty dataframe")

    if metric_config:
        update_mode = metric_config.get('update_mode', 'backfill')

        if update_mode == 'backfill':
            cur.execute(f"UPDATE {table} SET is_latest = FALSE WHERE is_latest = TRUE")

        elif update_mode == 'incremental':
            if table.endswith('_monthly'):
                period_col = 'month'
            elif table.endswith('_daily'):
                period_col = 'date'
            else:
                period_col = 'date'

            if period_col not in df.columns:
                raise ValueError(
                    f"Incremental mode requires '{period_col}' column, "
                    f"but it's missing from dataframe. Available columns: {df.columns.tolist()}"
                )

            periods = tuple(df[period_col].unique())
            if len(periods) == 1:
                cur.execute(f"UPDATE {table} SET is_latest = FALSE WHERE {period_col} = %s AND is_latest = TRUE", (periods[0],))
            else:
                cur.execute(f"UPDATE {table} SET is_latest = FALSE WHERE {period_col} IN {sql_tuple(periods)} AND is_latest = TRUE")

    df['is_latest'] = True

    columns = df.columns.tolist()
    placeholders = ", ".join(["%s"] * len(columns))
    col_names = ", ".join(columns)

    values = [tuple(row) for row in df.to_numpy()]
    cur.executemany(
        f"REPLACE INTO {table} ({col_names}) VALUES ({placeholders})",
        values
    )


def clear_destination_table(table: str, cur) -> None:

    cur.execute(f"TRUNCATE TABLE {table};")

# source: https://gitlab.wikimedia.org/repos/data-engineering/wmfdata-python/-/blob/main/src/wmfdata/utils.py?ref_type=heads#L201
# by https://gitlab.wikimedia.org/nshahquinn
def sql_tuple(i):
    """
    Given a Python iterable, returns a string representation that can be used in an SQL IN
    clause.

    For example:
    > sql_tuple(["a", "b", "c"])
    "('a', 'b', 'c')"

    WARNING: In some cases, this function produces incorrect results with strings that contain
    single quotes or backslashes. If you encounter this situation, consult the code comments or ask
    the maintainers for help.
    """

    if type(i) != list:
        i = [x for x in i]

    if len(i) == 0:
        raise ValueError("Cannot produce an SQL tuple without any items.")

    list_repr = repr(i)
    return "(" + list_repr[1:-1] + ")"

def get_query(url: str, user_agent: Optional[str] = None, timeout: int = 30) -> str:
    headers = {}
    if user_agent:
        headers['User-Agent'] = user_agent

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        raise requests.Timeout(f"Request to {url} timed out after {timeout} seconds")
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch query from {url}: {e}")

def setup_logging(script_name: str, max_bytes: int = 10*1024*1024, backup_count: int = 5) -> logging.Logger:
    log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(log_dir, exist_ok=True) 

    log_file = os.path.join(log_dir, f'{script_name}.log')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def validate_data(df: pd.DataFrame, metric_name: str, min_rows: int = 1, required_columns: Optional[Set[str]] = None) -> bool:
    if df.empty:
        raise ValueError(f"{metric_name}: dataframe is empty")

    row_count = len(df)
    if row_count < min_rows:
        raise ValueError(f"{metric_name}: too few rows ({row_count} < {min_rows})")

    null_cols = df.columns[df.isnull().all()].tolist()
    if null_cols:
        raise ValueError(f"{metric_name}: all-null columns: {null_cols}")

    if required_columns:
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"{metric_name}: missing required columns: {missing}")

        for col in required_columns:
            if df[col].isnull().all():
                raise ValueError(f"{metric_name}: required column '{col}' has all null values")

    return True


def validate_schema(df: pd.DataFrame, table: str, cur) -> bool:
    cur.execute(f"DESCRIBE {table}")
    table_cols = {row[0] for row in cur.fetchall()}
    df_cols = set(df.columns)

    expected_in_df = table_cols - {'is_latest'}

    missing = expected_in_df - df_cols
    extra = df_cols - table_cols

    if missing:
        raise ValueError(f"Schema validation failed for table '{table}': dataframe is missing columns: {sorted(missing)}")
    if extra:
        raise ValueError(f"Schema validation failed for table '{table}': dataframe has unexpected columns: {sorted(extra)}")

    return True
