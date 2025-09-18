import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar



# Load data function
def load_data(wiki, data_type="templates"):
    file_map = {
        "editors-activity-5edits": {
            "tewiki": "data/editor_activity_yoy_5edits/editor_activity_5edits_te.tsv",
            "hiwiki": "data/editor_activity_yoy_5edits/editor_activity_5edits_hi.tsv",
            "mlwiki": "data/editor_activity_yoy_5edits/editor_activity_5edits_ml.tsv",
        },
        "editors-activity-1edit": {
            "tewiki": "data/editor_activity_yoy_1edit/editors_activity_1edit_te.tsv",
            "hiwiki": "data/editor_activity_yoy_1edit/editors_activity_1edit_hi.tsv",
            "mlwiki": "data/editor_activity_yoy_1edit/editors_activity_1edit_ml.tsv",
        } ,
        'user-activation': {
            'tewiki': 'data/user_activation/new_users_activated_te.tsv',
            'hiwiki': 'data/user_activation/new_users_activated_hi.tsv',
            'mlwiki': 'data/user_activation/new_users_activated_ml.tsv',
        } ,
        'user-edit-buckets': {
            'tewiki': 'data/user_edit_buckets/user-edit-bucket-te.tsv',
            'hiwiki': 'data/user_edit_buckets/user-edit-bucket-hi.tsv',
            'mlwiki': 'data/user_edit_buckets/user-edit-bucket-ml.tsv',
        } ,
        'user-rights-stats': {
            'tewiki': 'data/user_rights_stats/user-right-te.tsv',
            'hiwiki': 'data/user_rights_stats/user-right-hi.tsv',
            'mlwiki': 'data/user_rights_stats/user-right-ml.tsv',
        } ,
        'avg-edit-size-by-bucket': {
            'tewiki' : 'data/avg_edit_size_by_bucket/avg_edit_size_te.tsv',
            'hiwiki' : 'data/avg_edit_size_by_bucket/avg_edit_size_hi.tsv',
            'mlwiki' : 'data/avg_edit_size_by_bucket/avg_edit_size_ml.tsv'
        },
        'talk-page-activity': {
            'tewiki': 'data/edits_on_talk_pages/edits_on_talk_pages_te.tsv',
            'hiwiki': 'data/edits_on_talk_pages/edits_on_talk_pages_hi.tsv',
            'mlwiki': 'data/edits_on_talk_pages/edits_on_talk_pages_ml.tsv',
        },
        'reverted_rollback_undo': {
            'tewiki': 'data/reverted_rollback_undo/reverted_rollback_undo--tewiki.tsv',
            'hiwiki': 'data/reverted_rollback_undo/reverted_rollback_undo--hiwiki.tsv',
            'mlwiki': 'data/reverted_rollback_undo/reverted_rollback_undo--mlwiki.tsv',
        },
        
        'automated_edits': {
            'tewiki': 'data/automated_edits/Automated_edits--tewiki.tsv',
            'hiwiki': 'data/automated_edits/Automated_edits--hiwiki.tsv',
            'mlwiki': 'data/automated_edits/Automated_edits--mlwiki.tsv',
        },
        'non-bot-users': {
            'tewiki': 'data/non-bot-users/non_bot_te.tsv',
            'hiwiki': 'data/non-bot-users/non_bot_hi.tsv',
            'mlwiki': 'data/non-bot-users/non_bot_ml.tsv',
        },
        'blocked_ips': {
            'tewiki': 'data/blocked_ips/blocked_ips_te.tsv',    
            'hiwiki': 'data/blocked_ips/blocked_ips_hi.tsv',
            'mlwiki': 'data/blocked_ips/blocked_ips_ml.tsv',
        },
        'total-users': {
            'tewiki': 'data/total_users/total_users_te.tsv',
            'hiwiki': 'data/total_users/total_users_hi.tsv',
            'mlwiki': 'data/total_users/total_users_ml.tsv',
        },
    }

    return pd.read_csv(file_map[data_type][wiki], sep="\t")




def show_contribution_page():
    st.title("CONTRIBUTION - VISUALISATIONS")

    
    col1, col2 = st.columns([1, 0.70])
    with col1:
        st.subheader("Total Users")

        # Load data for selected wiki
        df_total_users = load_data(wiki_filter, "total-users")
        df_total_users['total_new_users'] = df_total_users['total_new_users'].astype(int)
        df_total_users['month_year'] = df_total_users['month_year'].astype(str)

        # Filter by year only (not month)
        selected_year = str(date_year)
        df_year = df_total_users[df_total_users['month_year'].str.endswith(selected_year)]

        if not df_year.empty:
            total_users_year = df_year['total_new_users'].sum()
        else:
            total_users_year = 0

        # Compact card
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6;
                        padding:16px 18px;
                        border-radius:10px;
                        width:500px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.1);
                        text-align:center;
                        margin:auto;
                        display:inline-block;">
                <h5 style="margin:0;color:#2E86C1;font-size:19px;">{wiki_filter.upper()} - {selected_year}</h5>
                <h3 style="margin:8px 0; color:#2E86C1; font-size:50px;">{total_users_year:,}</h3>

            </div>
            """,
            unsafe_allow_html=True
        )

        # Add space before table
        st.markdown("<br>", unsafe_allow_html=True)

        # Unique Users table
        st.subheader("Unique user by user right")
        df = load_data(wiki_filter, "user-rights-stats")  
        df = df[["ug_group", "unique_users"]].sort_values("unique_users", ascending=False)

        st.dataframe(
            df, use_container_width=True
        )


    with col2:
        st.subheader("Project health indicators - edits on talk pages")
        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"

        # Load data
        df = load_data(wiki, "talk-page-activity")
        df["year"] = df["year"].astype(int)
        df["month"] = df["month"].astype(int)
        df["edit_count"] = df["edit_count"].astype(int)

        # Convert to datetime
        df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

        # Group & pivot
        yearly_df = df.groupby(["year", "talk_page_type"])["edit_count"].sum().reset_index()
        yearly_pivot = yearly_df.pivot(
            index="year",
            columns="talk_page_type",
            values="edit_count"
        ).fillna(0)

        yearly_pivot = yearly_pivot.reindex(
            columns=["Article Talk", "User Talk", "Project Talk"],
            fill_value=0
        )

        COLOR_MAP = {
            "Article Talk": "#1f77b4",
            "User Talk": "#ff7f0e",
            "Project Talk": "#2ca02c",
        }

        # Plot
        fig, ax = plt.subplots(figsize=(6, 6))
        yearly_pivot.plot(
            kind="bar",
            stacked=True,
            ax=ax,
            color=[COLOR_MAP.get(col, "#333333") for col in yearly_pivot.columns],
            alpha=0.85,
            edgecolor="black",
            linewidth=0.5
        )

        ax.set_title(f"Yearly Edits by Talk Page Type - {wiki}", fontsize=12)
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Edits")
        ax.legend(title="Talk Page Type", fontsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        st.pyplot(fig)


    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Edits reverted or rolled back or undo")
        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"

        df = load_data(wiki, "reverted_rollback_undo")
        df['Edit_Date'] = pd.to_datetime(df['Edit_Date'], errors='coerce')
        df = df.dropna(subset=['Edit_Date'])

        months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]

        if 'date_filter' in globals() and isinstance(globals()['date_filter'], (list, tuple)):
            sel_month, sel_year = globals()['date_filter']
        else:
            sel_month = months[datetime.date.today().month - 1]
            sel_year = datetime.date.today().year

        try:
            month_num = months.index(sel_month) + 1
        except ValueError:
            month_num = datetime.date.today().month

        df_filtered = df[(df['Edit_Date'].dt.year == int(sel_year)) & (df['Edit_Date'].dt.month == month_num)]
        counts = df_filtered.groupby(df_filtered['Edit_Date'].dt.day)['reverted_edits'].sum()

        last_day = calendar.monthrange(int(sel_year), month_num)[1]
        all_days = pd.Series(0, index=range(1, last_day + 1))
        counts = all_days.add(counts, fill_value=0).astype(int)

        # Bar plot for reverted edits per day in the selected month
        fig, ax = plt.subplots(figsize=(10, 5))
        if counts.max() == 0:
            ax.bar(counts.index, counts.values, color='skyblue', edgecolor='black', alpha=0.7)
            ax.set_ylim(0, 1)
            ax.text(0.5, 0.5, 'No reverted edits in the selected month', ha='center', va='center', fontsize=12, color='gray', transform=ax.transAxes)
        else:
            bars = ax.bar(counts.index, counts.values, color='skyblue', edgecolor='black', alpha=0.7)
            for bar, y in zip(bars, counts.values):
                if y > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, y/2, str(int(y)), ha='center', va='center', fontsize=13, fontweight='bold', color='black')
        ax.set_xlabel('Day of month', fontsize=14)
        ax.set_ylabel('Number of Reverted Edits', fontsize=14)
        ax.set_title(f'Reverted Edits per day in {sel_month} {sel_year}', fontsize=16)
        ax.set_xticks(range(1, last_day + 1))
        ax.tick_params(axis='x', labelsize=12, rotation=0)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig, use_container_width=True)

    with col5:
        st.subheader("Automated edits")

        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"

        df = load_data(wiki, "automated_edits")
        df['Edit_Date'] = pd.to_datetime(df['Edit_Date'], errors='coerce')
        df = df.dropna(subset=['Edit_Date'])

        months = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
        ]

        if 'date_filter' in globals() and isinstance(globals()['date_filter'], (list, tuple)):
            sel_month, sel_year = globals()['date_filter']
        else:
            sel_month = months[datetime.date.today().month - 1]
            sel_year = datetime.date.today().year

        try:
            month_num = months.index(sel_month) + 1
        except ValueError:
            month_num = datetime.date.today().month

        df_filtered = df[(df['Edit_Date'].dt.year == int(sel_year)) & (df['Edit_Date'].dt.month == month_num)]
        counts = df_filtered.groupby(df_filtered['Edit_Date'].dt.day)['Automated_Edits'].sum()

        last_day = calendar.monthrange(int(sel_year), month_num)[1]
        all_days = pd.Series(0, index=range(1, last_day + 1))
        counts = all_days.add(counts, fill_value=0).astype(int)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.step(counts.index, counts.values, where='mid', color='blue', linewidth=2)
        ax.set_xlabel('Day of month', fontsize=14)
        ax.set_ylabel('Number of Automated Edits', fontsize=14)
        ax.set_title(f'Automated Edits per day in {sel_month} {sel_year}', fontsize=16)
        ax.set_xticks(range(1, last_day + 1))
        ax.tick_params(axis='x', labelsize=12, rotation=0)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        for x, y in zip(counts.index, counts.values):
            ax.text(x, y, str(int(y)), ha='center', va='bottom', color='black', fontsize=11, fontweight='bold')

        st.pyplot(fig, use_container_width=True)


    col9, col10 = st.columns(2)
    with col9:
        st.subheader("Editors with at least one edit (rolling YoY)")

    # Pick wiki (default = tewiki)
        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"

    # Load 1+ edit dataset
        df = load_data(wiki, "editors-activity-1edit")
        df = df.sort_values(by="edit_year")

    # Compute 2-year moving average
        df["moving_avg"] = df["active_editors"].rolling(window=2).mean()

        max_editors = df["active_editors"].max()

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(df["edit_year"], df["active_editors"], color="skyblue", label="Active Editors")
        ax.plot(df["edit_year"], df["moving_avg"], color="red", marker="o", linewidth=2, label="2-Year Moving Avg")

        ax.set_title(f"Yearly Active Editors {wiki}", fontsize=12)
        ax.set_xlabel("Edit Year")
        ax.set_ylabel("Number of Active Editors")
        ax.set_ylim(0, max_editors * 1.1)
        ax.set_xticks(df["edit_year"])
        ax.set_xticklabels(df["edit_year"], rotation=45)
        ax.legend()
        ax.grid(axis="y")

        st.pyplot(fig)

    with col10:
        st.subheader("Editors with at least 5 edits (rolling YoY)")

        # --- Plot for editors with 5+ edits ---
        wiki = wiki_filter if 'wiki_filter' in globals() else "tewiki"

        df = load_data(wiki, "editors-activity-5edits")

        # Prepare data
        df = df.rename(columns={
            "edit_year": "year",
            "edit_month": "month",
            "active_editors": "edits"
        })
        df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
        df = df.sort_values(by="date")

        # 2-month moving average
        df["2_month_moving_avg"] = df["edits"].rolling(window=2).mean()
        max_edits = df["edits"].max()

        # Plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(df["date"], df["edits"], width=20, color="skyblue", label="Monthly Active Editors")
        ax.plot(df["date"], df["2_month_moving_avg"], color="red", marker="o", linewidth=2,
                label="2-Month Moving Average")

        ax.set_title(f"Monthly Active Editors with Moving Average {wiki}", fontsize=12)
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Active Editors")
        ax.set_ylim(0, max_edits * 1.1)
        ax.tick_params(axis="x", rotation=45)
        ax.legend()
        ax.grid(axis="y")

        st.pyplot(fig)



    col11, col12, col13 = st.columns(3)
    with col11:
        st.subheader("New users activated in the last 30 days")

        # Pick wiki (default = tewiki)
        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"

        # Load activation dataset
        df = load_data(wiki, "user-activation")

        # Expected TSV columns: total_new_users, new_users_with_1_edit, new_users_with_5_edits, activation_rate_1_edit_percent
        values = [
            df["total_new_users"].iloc[0],
            df["new_users_with_1_edit"].iloc[0],
            df["new_users_with_5_edits"].iloc[0],
        ]
        activation_rate = df["activation_rate_1_edit_percent"].iloc[0]

        # Prepare dataframe for plotting
        plot_df = pd.DataFrame({
            "Metric": ["Total New Users", "Users with at least 1 Edit", "Users with at least 5 Edits"],
            "Count": values
        })

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(plot_df["Metric"], plot_df["Count"], color=["skyblue", "lightgreen", "salmon"])

        # Add values on top of bars
        for i, v in enumerate(plot_df["Count"]):
            ax.text(i, v + 5, str(v), ha="center", fontsize=10, fontweight="bold")

        # Title and labels
        ax.set_title(f"New Users Activation Summary (Last 30 Days) - {wiki}", fontsize=12)
        ax.set_ylabel("Number of Users")
        ax.grid(axis="y", linestyle="--", alpha=0.6)

            # ✅ Fix ylim so no empty space below axis
        ax.set_ylim(0, max(plot_df["Count"]) * 1.15)

        # ✅ Add activation rate text below x-axis labels
        ax.set_xlabel(f"User Activation Rate: {activation_rate:.2f}%", fontsize=11, fontweight="bold", labelpad=15)

        st.pyplot(fig)

    with col12:
        st.subheader("Average size of an edit by edit count bucket")

        df = load_data(wiki_filter, "avg-edit-size-by-bucket")

        colors = ["#4CAF50"] * len(df)

        fig, ax = plt.subplots()
        ax.bar(df["edit_count_bucket"], df["avg_edit_size"], color=colors)
        
        ax.set_xlabel("Edit Count Bucket")
        ax.set_ylabel("Average Edit Size")
        ax.set_title("Average size of an edit by edit count bucket")
        plt.xticks(rotation=45)

        st.pyplot(fig)
    

    with col13:
        st.subheader("Editor Distribution by Edit Count Bucket")
        ## st.write("placeholder")
        # --- Plot for editors by contribution buckets ---
        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"

        df = load_data(wiki, "user-edit-buckets")

        # Ensure correct column names
        df = df.rename(columns={df.columns[0]: "number_of_editors", df.columns[1]: "bucket"})

        # Sort buckets by number_of_editors (descending)
        bucket_order = df.sort_values("number_of_editors", ascending=False)["bucket"].tolist()
        df = df.set_index("bucket").reindex(bucket_order).reset_index()

        # Color palette
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#5D737E']

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(df["bucket"], df["number_of_editors"],
              color=colors[:len(df)], alpha=0.8, edgecolor="black", linewidth=0.5,
              label="Number of Editors")

        # Log scale
        ax.set_yscale("log")

        # Add value labels
        for i, (bucket, count) in enumerate(zip(df["bucket"], df["number_of_editors"])):
            if count > 0:
                ax.text(i, count * 1.1, f"{int(count):,}",
                ha="center", va="bottom", fontweight="bold", fontsize=9)

        # Titles and labels
        ax.set_title(f"Editors by Contribution Buckets (Log Scale) - {wiki}", fontsize=12)
        ax.set_xlabel("Contribution Buckets")
        ax.set_ylabel("Number of Editors (Log Scale)")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y")
        ax.legend()

        st.pyplot(fig)


    col14, col15= st.columns([1, 2])
    with col14:
        st.subheader("IP addresses or ranges blocked")
        # Load blocked users/IPs data
        df_blocks = load_data(wiki_filter, "blocked_ips")  # adjust to your TSV/CSV source

        if not df_blocks.empty:
            # Categorize blocks by duration type
            df_blocks["duration_type"] = df_blocks["expiry"].apply(
                lambda x: "Indefinite" if x == "infinity" else "Definite"
            )

            # Count
            duration_counts = df_blocks["duration_type"].value_counts()

            # Plot pie chart
            fig, ax = plt.subplots(figsize=(6, 6))
            colors = ["#2E86AB", "#F18F01"]

            wedges, texts, autotexts = ax.pie(
                duration_counts.values,
                labels=duration_counts.index,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
                textprops={"fontsize": 10, "color": "black"}
            )

            ax.set_title(f"Block Duration Distribution - {wiki_filter}", fontsize=12, pad=20)

            st.pyplot(fig)
        else:
            st.info("No block data available for this wiki.")

    with col15:
        st.subheader("Top 10 non-bot registered users")
        wiki = wiki_filter if "wiki_filter" in globals() else "tewiki"
        df = load_data(wiki, "non-bot-users")

        df["month_year"] = pd.to_datetime(df["month_year"], format="%Y-%m")

        month_map = {
            "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
            "July":7,"August":8,"September":9,"October":10,"November":11,"December":12
        }

        selected_month = month_map[date_filter[0]]
        selected_year = date_filter[1]

        selected_date = pd.to_datetime(f"{selected_year}-{selected_month:02d}")

        df_selected = df[df["month_year"] == selected_date]

        top10 = df_selected.sort_values("edits", ascending=False).head(10)

        st.table(top10[["username", "edits"]].reset_index(drop=True))

        

# Call the function when this file is executed
show_contribution_page()
