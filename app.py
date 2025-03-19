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

userId = random.choice(users)
workout_data = get_user_workouts(userId)

def display_app_page():
    """Displays the home page of the app."""
    st.set_page_config(layout="wide")
    st.title('Welcome to SDS!')

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        advice_data = get_genai_advice(userId)
        display_genai_advice(advice_data['timestamp'], advice_data['content'], advice_data['image'])

    with col2:
        posts_data = get_user_posts(userId)

        if not posts_data:
            st.info("No posts available.")
        else:
            for post in posts_data:
                user_profile = get_user_profile(post['user_id'])  # Fetch user details

                if user_profile:  # Ensure user profile exists
                    display_post(
                        user_profile['full_name'],  # Get full name
                        user_profile['profile_image'],  # Get profile image
                        post['timestamp'], 
                        post['content'], 
                        post['image']
                    )
                else:
                    st.warning(f"User {post['user_id']} not found.")  # Handle missing user


    with col3:
        display_activity_summary(workout_data)

    #Recent Workouts Display
    st.markdown("---")
    display_recent_workouts(workout_data)

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
