import streamlit as st

st.set_page_config(page_title="Indic Community Insights Dashboard", layout="wide")

# Sidebar filters
st.sidebar.header("Category Selection")
category = st.sidebar.selectbox("Select Category", ["Overview", "Content", "Contribution"])

st.sidebar.header("Filter")
# Month & Year picker (2015-2025) — select month and year only
months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]
date_month = st.sidebar.selectbox("Month", months)
years = list(range(2015, 2026))  # 2015..2025
date_year = st.sidebar.selectbox("Year", years)
# Keep a `date_filter` variable for backwards compatibility (month, year)
date_filter = (date_month, date_year)

wiki_filter = st.sidebar.selectbox("Project", ["tewiki", "hiwiki", "mlwiki"])

# Display content based on selected category
if category == "Overview":
    st.title("📊 Indic Community Insights Dashboard")

    st.markdown("""
    Welcome to the **Indic Community Insights Dashboard**!

    This dashboard provides insights into:
    - **Content** – trends in articles, templates, and growth across Indic Wikipedias
    - **Contribution** – editor activity and participation metrics


    👉 Use the left sidebar (or the navigation at the top) to explore each section.
    """)

elif category == "Content":
    # Execute the content page with the current context
    exec(open("components/content.py").read(), globals())

elif category == "Contribution":
    # Execute the contribution page with the current context
    exec(open("components/contribution.py").read(), globals())



