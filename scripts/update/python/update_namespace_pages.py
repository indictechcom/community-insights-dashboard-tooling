import urllib.request
import json
import pandas as pd
import toolforge as forge

import os

from utils import (
    clear_destination_table,
    update_destination_table,
    sql_tuple,
    get_query,
    setup_logging,
    validate_data,
    validate_schema
)

logger = setup_logging('update_namespace_pages')

with open('../../../config.json', 'r') as f:
    config = json.load(f)
    logger.info('config loaded successfully.')

user_agent = forge.set_user_agent(
    tool=config['user_agent']['tool'],
    url=config['user_agent']['url'],
    email=config['user_agent']['email'],
)

config_metric_key = 'namespace_pages'
query_url = config['metric_map'][config_metric_key]['generation_query']
query = get_query(query_url)
logger.info('query fetched successfully')
destination_table = config['metric_map'][config_metric_key]['destination_table']
databases = config['databases']
tool_database = config['tool_database']
logger.info(f'target databases: {databases}')
logger.info(f'destination table: {destination_table}')

def fetch_data(query, db):
    logger.info(f'connecting to database: {db}')
    con = forge.connect(db)
    with con.cursor() as cur:
        logger.info(f'fetching data for {db}')
        cur.execute(query)
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=[col[0] for col in cur.description])
        logger.info(f'fetched {len(df)} rows for {db}')
    return df

def main():

    logger.info('starting data fetch from wikis')
    df = pd.DataFrame()
    for wiki_db in databases:
        logger.info(f'processing {wiki_db}')
        wiki_query = query.replace('{DATABASE}', f"'{wiki_db}'")
        wiki_df = fetch_data(wiki_query, wiki_db)
        df = pd.concat([df, wiki_df])
    df = df.reset_index(drop=True)

    logger.info(f'total rows collected: {len(df)}')

    if not df.empty:

        logger.info(f'connecting to the database of the tool: {tool_database["name"]}')
        con = forge.toolsdb(tool_database['name'])
        cur = con.cursor()

        try:
            validate_data(df, config_metric_key)
            validate_schema(df, destination_table, cur)
            logger.info(f'inserting {len(df)} rows into {destination_table}')
            update_destination_table(df, destination_table, cur)
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
    else:
        logger.warning('dataframe is empty')

if __name__ == '__main__':
    main()
