#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
#############################################################################

from internals import create_component
import streamlit as st
import datetime
import pandas as pd
import altair as alt

# Example custom component
def display_my_custom_component(value):
    """Displays a 'my custom component'."""
    data = {'NAME': value}
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Displays a user post with an image, timestamp, and text content."""
    
    st.markdown(f"### {username}'s Post")
    
    col1, col2 = st.columns([1, 9])
    
    with col1:
        st.image(user_image, width=50)

    with col2:
        st.write(f"📅 {timestamp}")
    
    st.write(content)
    
    if post_image:
        st.image(post_image, width=200)

    st.markdown("---")


def display_activity_summary(workouts_list):
    """
    Displays an activity summary based on the workouts list.
    """
    st.title("Workout Summary")
    st.markdown('Work out fun!!!!! :joy:')

    list = test_logic(workouts_list)
    for index, workout in enumerate(list):
        st.subheader(f"Workout #{index + 1}")
        st.write(f"- Start Time: {workout['start_timestamp']}")
        st.write(f"- End Time: {workout['end_timestamp']}")
        st.write(f"- Distance: {workout['distance']} km")
        st.write(f"- Start Coordinates: {workout['start_lat_lng']}")
        st.write(f"- End Coordinates: {workout['end_lat_lng']}")
        st.write(f"- Steps: {workout['steps']}")
        st.write(f"- Calories burned: {workout['calories_burned']}")

def test_logic(workouts_list):
    return workouts_list


def display_genai_advice(timestamp, content, image):
    """Displays motivational AI-generated advice with an optional image."""
    
    st.markdown(
        """
        <style>
        .genai-advice {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            background-color: #f0f0f0;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin: auto;
            padding: 15px;
            width: 60%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="genai-advice">
            <h2>GenAI Advice</h2>
            <p>{content}</p>
            <p><em>{timestamp}</em></p>
            {'<img src="' + image + '" width="200">' if image else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def display_recent_workouts(workouts):
    """
    Displays a user's recent workouts in a formatted way.
    """
    st.subheader("Recent Workouts")
    
    if not workouts:
        st.info("No recent workouts found.")
        return
    
    sorted_workouts = sorted(
        workouts, 
        key=lambda w: datetime.datetime.strptime(w['start_timestamp'], '%Y-%m-%d %H:%M:%S'),
        reverse=True
    )
    
    for i, workout in enumerate(sorted_workouts):
        start_datetime = datetime.datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
        formatted_date = start_datetime.strftime("%B %d, %Y")
        
        display_title = f"Workout on {formatted_date} (#{i+1})"
        
        with st.expander(display_title, expanded=(i == 0)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Distance", f"{workout['distance']:.2f} km")
                st.metric("Steps", f"{workout['steps']:,}")
                
                start_time = datetime.datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.strptime(workout['end_timestamp'], '%Y-%m-%d %H:%M:%S')
                duration = end_time - start_time
                minutes = duration.total_seconds() / 60
                st.metric("Duration", f"{int(minutes)} minutes")
            
            with col2:
                st.metric("Calories Burned", f"{workout['calories_burned']} cal")
                
                chart_data = pd.DataFrame([
                    {'point': 'Start', 'latitude': workout['start_lat_lng'][0], 'longitude': workout['start_lat_lng'][1]},
                    {'point': 'End', 'latitude': workout['end_lat_lng'][0], 'longitude': workout['end_lat_lng'][1]}
                ])
                
                st.write("Workout Path")
                chart = alt.Chart(chart_data).mark_circle(size=100).encode(
                    x=alt.X('longitude', title='Longitude'),
                    y=alt.Y('latitude', title='Latitude'),
                    color=alt.Color('point', scale=alt.Scale(domain=['Start', 'End'], range=['green', 'red'])),
                    tooltip=['point', 'latitude', 'longitude']
                ).properties(height=150)
                
                line_chart = alt.Chart(chart_data).mark_line().encode(
                    x='longitude',
                    y='latitude',
                    color=alt.value('gray')
                )
                
                st.altair_chart(chart + line_chart, use_container_width=True)

