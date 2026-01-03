import pandas as pd 
import json 
import requests
import toolforge as forge
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from utils import (
    to_mysql_ts,
    setup_logging,
    update_destination_table,
    validate_data,
    validate_schema
)

logger = setup_logging('update_editor_user_counts_by_project')
can_url = "https://gitlab.wikimedia.org/repos/data-engineering/canonical-data/-/raw/main/wiki/wikis.tsv"
api = "https://wikimedia.org/api/rest_v1/metrics/editors"

with open('../../config.json', 'r') as f:
    config = json.load(f)
    logger.info('config loaded successfully.')

user_agent = forge.set_user_agent(
    tool=config['user_agent']['tool'],
    url=config['user_agent']['url'],
    email=config['user_agent']['email'],
)

config_metric_key = 'editor_user_counts_by_project'
destination_table = config['metric_map'][config_metric_key]['destination_table']
database_codes = config['databases']
tool_database = config['tool_database']
logger.info(f'target databases : {database_codes}')
logger.info(f'destination table: {destination_table}')

def get_date_range():
    start_date = "20150101"
    
    today = datetime.now()
    last_month = today.replace(day=1) - timedelta(days=1)
    end_date = last_month.strftime('%Y%m%d')
    
    logger.info(f'date range: {start_date} to {end_date}')
    return start_date, end_date


def get_canonical_project_url(url, db_code):
    logger.info(f'fetching project url of project with db code {db_code}')
    can_df = pd.read_csv(url, sep='\t')
    canonical_project_url = can_df[can_df['database_code'] == db_code]['domain_name'].values[0]
    logger.info(f'project url for the db code {db_code} is {canonical_project_url}')
    return canonical_project_url
    
def get_date_chunks(start_date_str, end_date_str, chunk_months=12):
    """Split date range into smaller chunks"""
    start = datetime.strptime(start_date_str, '%Y%m%d')
    end = datetime.strptime(end_date_str, '%Y%m%d')
    
    chunks = []
    current = start
    
    while current < end:
        chunk_end = min(current + relativedelta(months=chunk_months) - timedelta(days=1), end)
        chunks.append({
            'start': current.strftime('%Y%m%d'),
            'end': chunk_end.strftime('%Y%m%d')
        })
        current = chunk_end + timedelta(days=1)
    
    return chunks

def fetch_and_create_df(project, wiki_db, start_date, end_date):
    logger.info(f'fetching editor(user) counts data for {project} from {start_date} to {end_date}')
    user_agent = f"{config['user_agent']['tool']} ({config['user_agent']['url']}; {config['user_agent'].get('email','')})"
    snapshot_date = datetime.now().date()
    
    chunks = get_date_chunks(start_date, end_date, chunk_months=24)
    all_records = []
    
    for i, chunk in enumerate(chunks):
        logger.info(f'Fetching chunk {i+1}/{len(chunks)}: {chunk["start"]} to {chunk["end"]}')
        url = f"{api}/aggregate/{project}/user/all-page-types/all-activity-levels/daily/{chunk['start']}/{chunk['end']}"
        
        max_retries = 5
        retry_count = 0
        chunk_success = False
        
        while retry_count < max_retries and not chunk_success:
            try:
                res = requests.get(url, headers={'User-Agent': user_agent}, timeout=120)
                res.raise_for_status()
                raw_data = res.json()
                
                if raw_data and 'items' in raw_data:
                    for item in raw_data['items']:
                        if 'results' in item:
                            for result in item['results']:
                                all_records.append({
                                    'snapshot_date': snapshot_date,
                                    'wiki_db': wiki_db,
                                    'date': to_mysql_ts(result['timestamp']).split()[0],
                                    'page_type': item.get('page-type'),
                                    'activity_level': item.get('activity-level'),
                                    'editor_count': result.get('editors', 0),
                                    'is_latest': True
                                })
                
                chunk_success = True
                logger.info(f'Successfully fetched chunk {i+1}/{len(chunks)}')
                
                    
            except requests.exceptions.RequestException as e:
                retry_count += 1
                logger.warning(f'Error fetching chunk {chunk["start"]} to {chunk["end"]} (attempt {retry_count}/{max_retries}): {e}')
                
                if retry_count < max_retries:
                    wait_time = 2 * retry_count  
                    logger.info(f'Waiting {wait_time} seconds before retry...')
                    time.sleep(wait_time)
                else:
                    logger.error(f'Failed to fetch chunk after {max_retries} attempts. Skipping this chunk.')
                    break
    
    res_df = pd.DataFrame(all_records)
    logger.info(f'fetched {len(res_df)} rows for {project}')
    return res_df

def main():
    logger.info('starting data fetch from Analytics API')
    df = pd.DataFrame()
    start, end = get_date_range()
    
    for db_code in database_codes:
        logger.info(f'processing project with db code: {db_code}')
        project_url = get_canonical_project_url(can_url, db_code)
        project_df = fetch_and_create_df(project_url, db_code, start, end)
        df = pd.concat([df, project_df])
    
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
            update_destination_table(df, destination_table, cur, config['metric_map'][config_metric_key])
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