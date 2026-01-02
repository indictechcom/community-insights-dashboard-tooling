#!/usr/bin/env python3
from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils import setup_logging, get_query
from metric_runner import load_config, setup_user_agent, fetch_wiki_data, insert_data


def generate_month_ranges(start_date, end_date):
    months = []
    current = start_date

    while current < end_date:
        month_start = current
        month_end = current + relativedelta(months=1)
        months.append((month_start, month_end))
        current = month_end

    return months


def modify_query_for_month(query, month_start, month_end, target_month):
    month_start_str = month_start.strftime('%Y%m%d%H%M%S')
    month_end_str = month_end.strftime('%Y%m%d%H%M%S')
    target_month_str = target_month.strftime('%Y-%m-01')

    modified_query = query.replace(
        "DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y%m01000000') AS month_start",
        f"'{month_start_str}' AS month_start"
    ).replace(
        "DATE_FORMAT(CURDATE(), '%Y%m01000000') AS month_end",
        f"'{month_end_str}' AS month_end"
    ).replace(
        "DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01') AS month",
        f"'{target_month_str}' AS month"
    )

    return modified_query


def main():
    logger = setup_logging('backfill_new_editor_activation')

    config = load_config()
    logger.info('config loaded successfully.')

    user_agent = setup_user_agent(config)

    metric_key = 'new_editor_activation'
    query_url = config['metric_map'][metric_key]['generation_query']
    ua = config['user_agent']
    ua_string = f"{ua['tool']} ({ua['url']}; {ua['email']})"
    base_query = get_query(query_url, user_agent=ua_string)
    logger.info('query fetched successfully')

    destination_table = config['metric_map'][metric_key]['destination_table']
    databases = config['databases']
    tool_database = config['tool_database']
    logger.info(f'target databases: {databases}')
    logger.info(f'destination table: {destination_table}')

    start_date = datetime(2015, 1, 1)
    end_date = datetime.now().replace(day=1)

    logger.info(f'backfilling from {start_date.strftime("%Y-%m")} to {end_date.strftime("%Y-%m")}')

    month_ranges = generate_month_ranges(start_date, end_date)
    logger.info(f'total months to process: {len(month_ranges)}')

    for month_start, month_end in month_ranges:
        logger.info(f'processing month: {month_start.strftime("%Y-%m")}')

        monthly_query = modify_query_for_month(base_query, month_start, month_end, month_start)
        df = fetch_wiki_data(monthly_query, databases, logger)

        logger.info(f'total rows collected for {month_start.strftime("%Y-%m")}: {len(df)}')

        if not df.empty:
            try:
                insert_data(df, f"{metric_key}_{month_start.strftime('%Y-%m')}", destination_table, tool_database, config, logger)
                logger.info(f'successfully inserted data for {month_start.strftime("%Y-%m")}')
            except Exception as e:
                logger.error(f'error updating {month_start.strftime("%Y-%m")}: {e}')
                raise
        else:
            logger.warning(f'no data for {month_start.strftime("%Y-%m")}')

    logger.info('backfill completed successfully')


if __name__ == '__main__':
    main()
