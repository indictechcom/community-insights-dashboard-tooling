import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Load data function
def load_data(wiki, data_type="templates"):
    file_map = {
        "editors-activity-5edits": {
            "tewiki": "data/",
            "hiwiki": "data/",
            "mlwiki": "data/",
        }
    }
    return pd.read_csv(file_map[data_type][wiki], sep="\t")


def show_contribution_page():
    st.title("CONTRIBUTION - VISUALISATIONS")

    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Number of new account registrations")
        st.write("placeholder")
    with col2:
        st.subheader("Top 10 non-bot registered users for the selected time period")
        st.write("placeholder")
    with col3:
        st.subheader("Project health indicators - monthly edits on talk pages; dimensions")
        st.write("placeholder")

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Number of edits deleted, reverted or rolled back")
        st.write("placeholder")
    with col5:
        st.subheader("Number of automated edits")
        st.write("placeholder")

    st.markdown("---") 

    
    col6, col7, col8 = st.columns(3)
    with col6:
        st.subheader("Total users")
        st.write("placeholder")
    with col7:
        st.subheader("Total new users")
        st.write("placeholder")
    with col8:
        st.subheader("Number of unique user / and their rights")
        st.write("placeholder")

    col9, col10 = st.columns(2)
    with col9:
        st.subheader("Number of editors with at least one edit (rolling YoY)")
        st.write("placeholder")
    with col10:
        st.subheader("Number of editors with at least 5 edits a month (rolling YoY)")
        st.write("placeholder")
        

    col11, col12, col13 = st.columns(3)
    with col11:
        st.subheader("New users activated in the last 30 days (1+, 5+)")
        st.write("placeholder")
    with col12:
        st.subheader("Average size of an edit by edit count bucket")
        st.write("placeholder")
    with col13:
        st.subheader("Number of editors by user edit bucket")
        st.write("placeholder")

    col14, col15 = st.columns(2)
    with col14:
        st.subheader("Currently blocked users")
        st.write("placeholder")
    with col15:
        st.subheader("IP addresses or ranges blocked currently")
        st.write("placeholder")


# Call the function when this file is executed
show_contribution_page()
