import pandas as pd
import matplotlib.pyplot as plt
import requests

# 1. Fetch the SQL from GitHub
query_url = "https://raw.githubusercontent.com/BhargaviVyshnavi20/community-insights-dashboard-tooling/main/monthly_active_editors_rolling_yoy.sql"
query1 = requests.get(query_url).text

# 2. Define the wikis you want to run on
wikis = ['tewiki', 'hiwiki', 'mlwiki']
all_dfs = []

# 3. Loop through each wiki and run the query
for wiki in wikis:
    output = connect_and_query(wiki, query1)
    df = pd.DataFrame(output, columns=['year', 'month', 'edits'])
    df['wiki'] = wiki  # Add differentiation column
    all_dfs.append(df)

# 4. Combine all results
combined_df = pd.concat(all_dfs, ignore_index=True)

# 5. Format date and sort
combined_df['date'] = pd.to_datetime(combined_df[['year', 'month']].assign(day=1))
combined_df = combined_df.sort_values(['wiki', 'date'])

# 6. Plot per wiki
for wiki in wikis:
    df = combined_df[combined_df['wiki'] == wiki].copy()
    df['moving_avg'] = df['edits'].rolling(window=3).mean()

    plt.figure(figsize=(12, 6))
    plt.bar(df['date'], df['edits'], width=20, color='skyblue', label='Active Editors')
    plt.plot(df['date'], df['moving_avg'], color='red', linewidth=2, label='3-Month Moving Average')
    
    plt.title(f'Monthly Active Editors with 3-Month Moving Average ({wiki})')
    plt.xlabel('Month')
    plt.ylabel('Number of Active Editors')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
