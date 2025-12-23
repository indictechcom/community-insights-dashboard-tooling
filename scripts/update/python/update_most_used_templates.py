import urllib.request
import json
import pandas as pd
import toolforge as forge

import os
import logging

from utils import (
    clear_destination_table,
    update_destination_table,
    sql_tuple,
    get_query
)

with open('../../../config.json', 'r') as f:
    config = json.load(f)

user_agent = forge.set_user_agent(
    tool=config['user_agent']['tool'],
    url=config['user_agent']['url'],
    email=config['user_agent']['email'],
)

config_metric_key = 'most_used_templates'
query_url = config['metric_map'][config_metric_key]['generation_query']
query = get_query(query_url)
destination_table = config['metric_map'][config_metric_key]['destination_table']
databases = config['databases']
tool_database = config['tool_database']

def fetch_data(query, db):
    con = forge.connect(db)
    with con.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=[col[0] for col in cur.description])
    return df

def main():

    df = pd.DataFrame()
    for wiki_db in databases:
        wiki_query = query.replace('{DATABASE}', f"'{wiki_db}'")
        wiki_df = fetch_data(wiki_query, wiki_db)
        df = pd.concat([df, wiki_df])
    df.reset_index(drop=True)

    if df is not None:

        con = forge.toolsdb(tool_database['name'])
        cur = con.cursor()

        try:
            clear_destination_table(destination_table, cur)
            update_destination_table(df, destination_table, cur)
            con.commit()
        except Exception as e:
            con.rollback()
        finally:
            cur.close()
            con.close()

if __name__ == "__main__":
    main()
