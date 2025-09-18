# Content page - this will be executed from app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import calendar

# Load data function
def load_data(wiki, data_type="templates"):
    file_map = {
        "templates": {
            "tewiki": "data/top_5_templates/top_5_templates_te.tsv",
            "hiwiki": "data/top_5_templates/top_5_templates_hi.tsv",
            "mlwiki": "data/top_5_templates/top_5_templates_ml.tsv",
        },
        "untouched":{
            "tewiki": "data/untouched_pages/untouched_pages_te.tsv",
            "hiwiki": "data/untouched_pages/untouched_pages_hi.tsv",
            "mlwiki": "data/untouched_pages/untouched_pages_ml.tsv",
        },
        "platform": {
            "tewiki": "data/by_platform/by_platform_te.tsv",
            "hiwiki": "data/by_platform/by_platform_hi.tsv",
            "mlwiki": "data/by_platform/by_platform_ml.tsv",
        },
        "tool":{
            "tewiki": "data/by_tools/by_tools_te.tsv",
            "hiwiki": "data/by_tools/by_tools_hi.tsv",
            "mlwiki": "data/by_tools/by_tools_ml.tsv",
        },
        "page_length": {
            "tewiki": "data/content_namespace/content_namespace_te.tsv",
            "hiwiki": "data/content_namespace/content_namespace_hi.tsv",
            "mlwiki": "data/content_namespace/content_namespace_ml.tsv",
        },
        "namespace": {
            "tewiki": "data/pages_by_namespace/pages_by_namespace_te.tsv",
            "hiwiki": "data/pages_by_namespace/pages_by_namespace_hi.tsv",
            "mlwiki": "data/pages_by_namespace/pages_by_namespace_ml.tsv",
        },
        "top_edited_pages":{
            "tewiki": "data/top_edited_pages/top_edited_content_pages_te.tsv",
            "hiwiki": "data/top_edited_pages/top_edited_content_pages_hi.tsv",
            "mlwiki": "data/top_edited_pages/top_edited_content_pages_ml.tsv",
        },
        "deleted_pages":{
            "tewiki": "data/deleted_pages/deleted_pages--tewiki.tsv",
            "hiwiki": "data/deleted_pages/deleted_pages--hiwiki.tsv",
            "mlwiki": "data/deleted_pages/deleted_pages--mlwiki.tsv",
        }
    }
    
    return pd.read_csv(file_map[data_type][wiki], sep="\t")

def show_content_page(date_filter, wiki_filter):
    st.title("CONTENT - VISUALISATIONS")

    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Number of pages by namespace")
        df_platform = load_data(wiki_filter, "namespace")

        fig, ax = plt.subplots(figsize=(8, 3))  
        wedges, texts, autotexts = ax.pie(
            df_platform['page_count'],
            startangle=140,
            autopct='%1.1f%%'  
        )

        # Style the percentage text
        plt.setp(autotexts, size=5)

        # Legend fixed in top-right corner
        ax.legend(
            wedges,
            df_platform['namespace'],
            title="Namespace",
            loc="upper right",
            bbox_to_anchor=(1.5, 1),  
            fontsize=7,
            title_fontsize=8
        )

        st.pyplot(fig, use_container_width=False)


    
    with col2:
        st.subheader("Untouched pages")
        
        df_untouched_pages = load_data(wiki_filter, "untouched")
        df_untouched_pages['no_of_unedited_pages'] = df_untouched_pages['no_of_unedited_pages'].astype(int)
        df_untouched_pages = df_untouched_pages.sort_values(
            by="no_of_unedited_pages", ascending=False
        )

        # Show as Streamlit table
        st.table(df_untouched_pages.reset_index(drop=True))


        
    col3, col4 = st.columns([1,2])
    with col3:
        st.subheader("Top 5 templates")
        df_templates = load_data(wiki_filter, "templates")
        st.table(df_templates)
        
    with col4:
        st.subheader("Page length distribution")
        df_pages = load_data(wiki_filter, "page_length")

        # Bigger figure size
        fig, ax = plt.subplots(figsize=(8, 3))

        # Histogram
        ax.hist(df_pages['page_length'], bins=50, color='skyblue', edgecolor='black')

        # Titles and labels with consistent font sizes
        ax.set_title("Histogram of Page Lengths", fontsize=16)
        ax.set_xlabel("Page Length", fontsize=14)
        ax.set_ylabel("Number of Pages", fontsize=14)

        # Tick styling
        ax.tick_params(axis='x', labelsize=12, rotation=0)
        ax.tick_params(axis='y', labelsize=12)

        # Grid (like your line chart)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        st.pyplot(fig, use_container_width=True)


    col5, col6 = st.columns(2)
    with col5:
        st.subheader("By platform")

        df_platform = load_data(wiki_filter, "platform")
        df_platform['edit_timestamp'] = pd.to_datetime(df_platform['edit_timestamp'], format='%Y%m%d')

        # Month names same as app.py
        months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]

        if 'date_filter' in globals() and isinstance(globals()['date_filter'], (list, tuple)):
            sel_month, sel_year = globals()['date_filter']
        else:
            sel_month = months[datetime.date.today().month - 1]
            sel_year = datetime.date.today().year

        # Convert month name to number
        try:
            month_num = months.index(sel_month) + 1
        except ValueError:
            month_num = datetime.date.today().month

        # Filter to year + month
        df_filtered = df_platform[
            (df_platform['edit_timestamp'].dt.year == int(sel_year)) &
            (df_platform['edit_timestamp'].dt.month == int(month_num))
        ]

        df_grouped = df_filtered.groupby('platform', as_index=False)['edit_count'].sum()

        # Pie chart
        fig, ax = plt.subplots(figsize=(5, 3))
        wedges, texts, autotexts = ax.pie(
            df_grouped['edit_count'],
            labels=df_grouped['platform'],
            autopct='%1.1f%%',
            startangle=140
        )

        plt.setp(texts, size=8)       # <-- label size
        plt.setp(autotexts, size=7) 
        ax.set_title(f"Edit Distribution by Platform - {sel_year}-{month_num:02d}", fontsize=10)
        st.pyplot(fig, use_container_width=False)

        
    with col6:
        st.subheader("By tool")
        
        # Load tool edits data
        df_tools = load_data(wiki_filter, "tool")

        # Convert edit_month to datetime
        df_tools['edit_month'] = pd.to_datetime(df_tools['edit_month'], format='%Y-%m')

        # Read selected month/year from globals() (already set in app.py as date_filter)
        if 'date_filter' in globals() and isinstance(globals()['date_filter'], (list, tuple)):
            sel_month, sel_year = globals()['date_filter']
        else:
            months = [
                "January","February","March","April","May","June",
                "July","August","September","October","November","December"
            ]
            sel_month = months[datetime.date.today().month - 1]
            sel_year = datetime.date.today().year

        # Convert month name to number
        try:
            month_num = months.index(sel_month) + 1
        except ValueError:
            month_num = datetime.date.today().month

        # Filter data for the selected month/year
        df_filtered = df_tools[
            (df_tools['edit_month'].dt.year == int(sel_year)) &
            (df_tools['edit_month'].dt.month == int(month_num))
        ]

        # Histogram
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df_filtered['edit_tool'], df_filtered['edit_count'],
            color="skyblue", edgecolor="black")

        ax.set_title(f"Edit Counts by Tool - {sel_year}-{month_num:02d}", fontsize=16)
        ax.set_xlabel("Edit Tool", fontsize=14)
        ax.set_ylabel("Edit Count", fontsize=14)
        plt.xticks(rotation=20)

        # Annotate bars
        for i, val in enumerate(df_filtered['edit_count']):
            ax.text(i, val, str(val), ha='center', va='bottom', fontsize=10, fontweight='bold')

        st.pyplot(fig, use_container_width=True)

    col7, col8 = st.columns([1,2])
    with col7:
        st.subheader("Top edited pages")


        df_top_pages = load_data(wiki_filter, "top_edited_pages")  


        df_top_pages["edit_count"] = df_top_pages["edit_count"].astype(int)

        df_top_pages["edit_month"] = pd.to_datetime(df_top_pages["edit_month"], format="%Y-%m")

    
        month_map = {
            "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
            "July":7,"August":8,"September":9,"October":10,"November":11,"December":12
        }
        selected_month = month_map[date_filter[0]]
        selected_year = date_filter[1]
        selected_date = pd.to_datetime(f"{selected_year}-{selected_month:02d}")

       
        df_selected = df_top_pages[df_top_pages["edit_month"] == selected_date]

        top10_pages = df_selected.sort_values("edit_count", ascending=False).head(10)

        st.table(top10_pages[["page_title", "edit_count"]].reset_index(drop=True))

        
    with col8:
        st.subheader("Deleted pages")
        df_deleted = load_data(wiki_filter, "deleted_pages")

        months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]

        
        sel_month, sel_year = date_filter

        # Convert month name to number
        month_num = months.index(sel_month) + 1

        df_deleted['Deletion_Date'] = pd.to_datetime(df_deleted['Deletion_Date'], errors='coerce')
        df_filtered = df_deleted[df_deleted['Deletion_Date'].notna()]
        df_filtered = df_filtered[
            (df_filtered['Deletion_Date'].dt.year == int(sel_year)) &
            (df_filtered['Deletion_Date'].dt.month == int(month_num))
        ]

        # Aggregate counts per day (if a numeric deleted_pages column exists, sum it; otherwise count rows)
        if 'deleted_pages' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['deleted_pages']):
            counts = df_filtered.groupby(df_filtered['Deletion_Date'].dt.day)['deleted_pages'].sum()
        else:
            counts = df_filtered.groupby(df_filtered['Deletion_Date'].dt.day).size()

        # Ensure days 1..last_day are present
        last_day = calendar.monthrange(int(sel_year), int(month_num))[1]
        all_days = pd.Series(0, index=range(1, last_day + 1))
        counts = all_days.add(counts, fill_value=0).astype(int)

        # Plot line chart
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(counts.index, counts.values, marker='o', markersize=6, linewidth=2, linestyle='-')
        ax.set_xlabel('Day of month', fontsize=14)
        ax.set_ylabel('No. of Deleted pages', fontsize=14)
        ax.set_title(f'Deleted pages per day in {sel_month} {sel_year}', fontsize=16)
        ax.set_xticks(range(1, last_day + 1))
        ax.tick_params(axis='x', labelsize=12, rotation=0)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        # Annotate each point with its value
        for x, y in zip(counts.index, counts.values):
            ax.text(x, y, str(int(y)), ha='center', va='bottom', color='black', fontsize=11, fontweight='bold')

        st.pyplot(fig, use_container_width=True)

