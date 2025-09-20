import streamlit as st
import os

from components import content, contribution

st.set_page_config(page_title="Indic Community Insights Dashboard", layout="wide")

# Sidebar filters
st.sidebar.header("Category Selection")
category = st.sidebar.selectbox("Select Category", ["Overview", "Content", "Contribution"])

st.sidebar.header("Filter")

# Month & Year picker (2015–2025) — select month and year only
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
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
    Welcome to the *Indic Community Insights Dashboard*!

    Explore activity trends and community growth across *Telugu, Hindi, and Malayalam Wikipedias* with this dashboard:
    - *Content* – See how articles, templates, and projects are growing.
    - *Contribution* – Track how editors are participating: edits made, active users, and community engagement.

    👉 Use the left sidebar (or the navigation at the top) to explore each section.
    """)

    # Visible but subtle team members section
    st.markdown("---")
    st.subheader("Team Members")
    st.markdown(
        """
        <div style='font-size:16px; line-height:1.8; color:#444;'>
        Usha Kiran Paruchuri &nbsp;|&nbsp; Bhargavi Vyshnavi Kancharla &nbsp;|&nbsp; Venkata Eswar Achi &nbsp;|&nbsp; Pavan Venkata Naga Manoj &nbsp;|&nbsp; Ziyaur Rahaman &nbsp;|&nbsp; Busi Venkata Mohan Reddy &nbsp;|&nbsp; Shaik Yeswanth
        </div>
        """,
        unsafe_allow_html=True
    )


elif category == "Content":
    # Call the content component
    content.show_content_page(date_filter, wiki_filter)

elif category == "Contribution":
    # Call the contribution component
    contribution.show_contribution_page(wiki_filter, date_filter, date_year)
