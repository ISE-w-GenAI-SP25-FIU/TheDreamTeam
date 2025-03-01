#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts, users
import random

userId = random.choice(list(users.keys()))

def display_app_page():
    """Displays the home page of the app."""
    st.set_page_config(layout="wide")
    st.title('TheDreamTeam')

    col1, col2 = st.columns(2, gap="small")
    with col1:
        advice_data = get_genai_advice(userId)
        display_genai_advice(advice_data['timestamp'], advice_data['content'], advice_data['image'])
    with col2:
        workout_data = get_user_workouts(userId)
        display_activity_summary(workout_data)

    #Recent Workouts Display
    st.markdown("---")
    workout_data = get_user_workouts(userId)
    display_recent_workouts(workout_data)

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
