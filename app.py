#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st

def display_app_page():
    # Navigation setup
    home_page = st.Page("home_page.py", title="Home", icon="🏠", default=True)
    community_page = st.Page("community_page.py", title="Community", icon="🤝", default=False, url_path="community")
    activity_page = st.Page("activity_page.py", title="Activity", icon="🏃‍♀️", default=False, url_path="activity")

    # Handle navigation without force-clearing content
    pg = st.navigation([home_page, community_page, activity_page])
    st.set_page_config(layout="wide", page_title="ISE Workouts", page_icon="🏃‍♀️")
    pg.run()

if __name__ == '__main__':
    display_app_page()


