#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st

def display_app_page():
    st.set_page_config(layout="wide", page_title="ISE Workouts", page_icon="🏃‍♀️")

    # Navigation setup
    home_page = st.Page("home_page.py", title="Home", icon="🏠")
    community_page = st.Page("community_page.py", title="Community", icon="🤝")
    activity_page = st.Page("activity_page.py", title="Activity", icon="🏃‍♀️")

    # Handle navigation without force-clearing content
    pg = st.navigation([home_page, community_page, activity_page])
    pg.run()

if __name__ == '__main__':
    display_app_page()


