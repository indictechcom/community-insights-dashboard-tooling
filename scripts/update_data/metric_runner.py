import json
import pandas as pd
import toolforge as forge
from typing import Dict, Any, List

from utils import (
    update_destination_table,
    get_query,
    setup_logging,
    validate_data,
    validate_schema
)


def load_config() -> Dict[str, Any]:
    with open('../../config.json', 'r') as f:
        return json.load(f)


def setup_user_agent(config: Dict[str, Any]) -> str:
    return forge.set_user_agent(
        tool=config['user_agent']['tool'],
        url=config['user_agent']['url'],
        email=config['user_agent']['email'],
    )


def fetch_wiki_data(query: str, databases: List[str], logger) -> pd.DataFrame:
    def fetch_data(query, db):
        logger.info(f'connecting to database: {db}')
        con = forge.connect(db)
        with con.cursor() as cur:
            logger.info(f'fetching data for {db}')
            cur.execute(query)
            result = cur.fetchall()
            df = pd.DataFrame(result, columns=[col[0] for col in cur.description])
            logger.info(f'fetched {len(df)} rows for {db}')
        con.close()
        return df

    logger.info('starting data fetch from wikis')
    df = pd.DataFrame()
    for wiki_db in databases:
        logger.info(f'processing {wiki_db}')
        wiki_query = query.replace('{DATABASE}', f"'{wiki_db}'")
        wiki_df = fetch_data(wiki_query, wiki_db)
        df = pd.concat([df, wiki_df])
    df = df.reset_index(drop=True)
    logger.info(f'total rows collected: {len(df)}')
    return df


def insert_data(df: pd.DataFrame, metric_key: str, destination_table: str, tool_database: Dict[str, str], config: Dict[str, Any], logger, display_name: str = None) -> None:
    if df.empty:
        logger.warning('dataframe is empty')
        return

    validation_name = display_name if display_name else metric_key

    logger.info(f'connecting to the database of the tool: {tool_database["name"]}')
    con = forge.toolsdb(tool_database['name'])
    cur = con.cursor()

    try:
        validate_data(df, validation_name)
        validate_schema(df, destination_table, cur)
        logger.info(f'inserting {len(df)} rows into {destination_table}')
        update_destination_table(df, destination_table, cur, config['metric_map'][metric_key])
        con.commit()
        logger.info('data update successful')
    except Exception as e:
        logger.error(f'error updating due to: {e}')
        con.rollback()
        logger.info('transaction rolled back')
        raise
    finally:
        cur.close()
        con.close()
        logger.info('database connection closed')


def run_metric_update(metric_key: str) -> None:
    logger = setup_logging(f'update_{metric_key}')

    config = load_config()
    logger.info('config loaded successfully.')

    user_agent = setup_user_agent(config)

    query_url = config['metric_map'][metric_key]['generation_query']
    query = get_query(query_url)
    logger.info('query fetched successfully')

    destination_table = config['metric_map'][metric_key]['destination_table']
    databases = config['databases']
    tool_database = config['tool_database']
    logger.info(f'target databases: {databases}')
    logger.info(f'destination table: {destination_table}')

    df = fetch_wiki_data(query, databases, logger)
    insert_data(df, metric_key, destination_table, tool_database, config, logger)
