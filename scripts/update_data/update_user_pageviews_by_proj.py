import pandas as pd 
import json 
import io
import toolforge as forge
from datetime import datetime, timedelta


from utils import (
    get_query,
    setup_logging,
    update_destination_table,
    validate_data,
    validate_schema
)

logger = setup_logging('update_user_pageviews_by_proj')
can_url = "https://gitlab.wikimedia.org/repos/data-engineering/canonical-data/-/raw/main/wiki/wikis.tsv"
api = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

with open('../../config.json', 'r') as f:
    config = json.load(f)
    logger.info('config loaded successfully.')

user_agent = forge.set_user_agent(
    tool=config['user_agent']['tool'],
    url=config['user_agent']['url'],
    email=config['user_agent']['email'],
)

config_metric_key = 'user_pageviews_by_project'
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
    
def fetch_and_create_df(project, wiki_db, start_date, end_date, access_type="all-access"):
    logger.info(f'fetching pageview data for {project} from {start_date} to {end_date}')
    url = f"{api}/aggregate/{project}/{access_type}/user/daily/{start_date}/{end_date}"
    user_agent_config = config.get('user_agent')
    snapshot_date = datetime.now().date()
    
    res = get_query(url, user_agent_config)
    raw_data = json.loads(res)
    records = []

    if raw_data and 'items' in raw_data:
        for item in raw_data['items']:
            records.append({
                'snapshot_date': snapshot_date,
                'wiki_db': wiki_db,
                'access_type': item.get('access'),
                'date': datetime.strptime(item['timestamp'], '%Y%m%d%H').date(),
                'view_count': item.get('views', 0)
            })
    
    res_df = pd.DataFrame(records)
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