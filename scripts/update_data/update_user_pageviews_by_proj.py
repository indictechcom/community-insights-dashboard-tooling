import pandas as pd 
import json 
import io
from datetime import datetime, timedelta


from utils import (
    get_query,
    setup_logging,
)

logger = setup_logging('update_user_pageviews_by_proj')
can_url = "https://gitlab.wikimedia.org/repos/data-engineering/canonical-data/-/raw/main/wiki/wikis.tsv"
project = "hi.wikipedia.org"
api = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

with open('../../config.json', 'r') as f:
    config = json.load(f)
    logger.info('config loaded successfully.')

def get_date_range():
    start_date = "20150101"
    
    today = datetime.now()
    last_month = today.replace(day=1) - timedelta(days=1)
    end_date = last_month.strftime('%Y%m%d')
    
    logger.info(f'date range: {start_date} to {end_date}')
    return start_date, end_date


def get_canonical_wiki_dbcode(url, proj_name):
    logger.info('fetching canonical wiki names')
    res =  get_query(url)
    can_df = pd.read_csv(io.StringIO(res), sep='\t')
    canonical_dbcode = can_df[can_df['domain_name'] == proj_name]['database_code'].values[0]
    logger.info(f'canonical db code for proj : {proj_name} = {canonical_dbcode}')
    return canonical_dbcode
    
def fetch_and_create_df(project, wiki_db, start_date, end_date, access_type = "all-access"):
    logger.info('fetching the data from Analytics Query Serivice api')
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
    logger.info(f'fetched {len(res_df)} rows')
    # print(res_df.head())
    return res_df

def main():
    start, end = get_date_range()
    for project in config.get('projects'):
        wiki_db = get_canonical_wiki_dbcode(can_url, project)
        fetch_and_create_df(project, wiki_db, start, end)

if __name__ == '__main__':
    main()