from datetime import datetime, timezone
import urllib.request
import logging
from logging.handlers import RotatingFileHandler
import os

import pandas as pd


def to_mysql_ts(ts):

    if ts is not None:
        sql_ts = (
            datetime.fromisoformat(ts[:-1])
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        return sql_ts
    else:
        return None


def update_destination_table(df: pd.DataFrame, table: str, cur, metric_config: dict = None) -> None:

    if metric_config:
        update_mode = metric_config.get('update_mode', 'replace_all')

        if update_mode == 'replace_all':
            cur.execute(f"UPDATE {table} SET is_latest = FALSE WHERE is_latest = TRUE")

        elif update_mode == 'append_period':
            if table.endswith('_monthly'):
                period_col = 'month'
            elif table.endswith('_daily'):
                period_col = 'date'
            else:
                period_col = 'date'

            if period_col in df.columns:
                periods = tuple(df[period_col].unique())
                if len(periods) == 1:
                    cur.execute(f"UPDATE {table} SET is_latest = FALSE WHERE {period_col} = %s AND is_latest = TRUE", periods)
                else:
                    cur.execute(f"UPDATE {table} SET is_latest = FALSE WHERE {period_col} IN {sql_tuple(periods)} AND is_latest = TRUE")

    df['is_latest'] = True

    columns = df.columns.tolist()
    placeholders = ", ".join(["%s"] * len(columns))
    col_names = ", ".join(columns)

    for _, row in df.iterrows():
        cur.execute(
            f"""
            REPLACE INTO {table} ({col_names})
            VALUES ({placeholders})
        """,
            tuple(row.values),
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

def get_query(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode()

def setup_logging(script_name, max_bytes=10*1024*1024, backup_count=5):
    log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f'{script_name}.log')
    master_log = os.path.join(log_dir, 'master.log')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    master_handler = RotatingFileHandler(
        master_log,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    master_handler.setLevel(logging.INFO)
    master_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(master_handler)
    logger.addHandler(console_handler)

    return logger


def validate_data(df, metric_name, min_rows=1):
    if df.empty:
        raise ValueError(f"{metric_name}: dataframe is empty")

    row_count = len(df)
    if row_count < min_rows:
        raise ValueError(f"{metric_name}: too few rows ({row_count} < {min_rows})")

    null_cols = df.columns[df.isnull().all()].tolist()
    if null_cols:
        raise ValueError(f"{metric_name}: all-null columns: {null_cols}")

    return True


def validate_schema(df, table, cur):
    cur.execute(f"DESCRIBE {table}")
    table_cols = {row[0] for row in cur.fetchall()}
    df_cols = set(df.columns)

    missing = table_cols - df_cols
    extra = df_cols - table_cols

    if missing:
        raise ValueError(f"missing columns in data: {missing}")
    if extra:
        raise ValueError(f"extra columns in data: {extra}")

    return True
