#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt

# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
    pass


def display_activity_summary(workouts_list):
    """
    Input: A list of workouts 
    Workouts contain information for start and end timestamps, 
    distance, steps, calories burned, start and end coordinates
    
    Output: None

    Example:
    workouts_list = [
        {'workout_id': f'workout 1',
        'start_timestamp': '2024-01-01 00:10:00',
        'end_timestamp': '2024-01-01 00:20:00',
        'start_lat_lng': 7.77,
        'end_lat_lng': 8.88,
        'distance': 10.0,
        'steps': 10000,
        'calories_burned': 50,},
        
        {'workout_id': f'workout 2',
        'start_timestamp': '2024-02-01 00:00:00',
        'end_timestamp': '2024-02-01 00:30:00',
        'start_lat_lng': 1.11,
        'end_lat_lng': 2.22,
        'distance': 5.0,
        'steps': 1000,
        'calories_burned': 10,
    }]
    """

    st.title("Display Workout Summary")
    st.markdown("---")

    total_time = 0
    total_distance = 0
    total_steps = 0
    total_calories_burned = 0

    for index, workout in enumerate(workouts_list):
        # Convert the string timestamps to datetime objects
        start_time = datetime.strptime(workouts_list[index]['start_timestamp'], '%Y-%m-%d %H:%M:%S')

        end_time = datetime.strptime(workouts_list[index]['end_timestamp'], '%Y-%m-%d %H:%M:%S')

        # Calculate the time difference in seconds
        time_difference = end_time - start_time
        total_seconds = time_difference.total_seconds()
        
        # Calculate the total time
        total_time += total_seconds
        total_distance += workouts_list[index]['distance']
        total_steps += workouts_list[index]['steps']
        total_calories_burned += workouts_list[index]['calories_burned']

        # Extract hours, minutes, and seconds from the timedelta
        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60

    st.subheader("Total Workouts")
    st.write(f"- Total Time: {hours} hours, {minutes} minutes, {seconds} seconds")
    st.write(f"- Total Distance: {total_distance} miles")
    st.write(f"- Total Steps: {total_steps} steps")
    st.write(f"- Total Calories Burned: {total_calories_burned} cal")


def display_genai_advice(timestamp, content, image):
    """Displays the most recent motivational advice from the GenAI model,
    including text, timestamp, and an optional image.

    timestamp: Date and time of GenAI advice
    content: Randomly selected motivational advice text
    image: Either a random motivational image or None
    """
    import streamlit as st

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
    
    Args:
        workouts: A list of workout dictionaries. Each workout contains:
            - workout_id: Unique identifier for the workout
            - start_timestamp: When the workout started
            - end_timestamp: When the workout ended
            - distance: Total distance covered (in km)
            - steps: Total steps taken
            - calories_burned: Calories burned during workout
            - start_lat_lng: Starting coordinates (latitude, longitude)
            - end_lat_lng: Ending coordinates (latitude, longitude)
    
    Returns:
        None
    """
    import streamlit as st
    import datetime
    import pandas as pd
    import altair as alt
    
    st.subheader("Recent Workouts")
    
    if not workouts:
        st.info("No recent workouts found.")
        return
    
    # Sort workouts by start_timestamp (most recent first)
    sorted_workouts = sorted(
        workouts, 
        key=lambda w: datetime.datetime.strptime(w['start_timestamp'], '%Y-%m-%d %H:%M:%S'),
        reverse=True
    )
    
    for i, workout in enumerate(sorted_workouts):
        # Format the date as month day year
        start_datetime = datetime.datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
        formatted_date = start_datetime.strftime("%B %d, %Y")
        
        # Add workout index to make them visually distinct even if dates are the same
        display_title = f"Workout on {formatted_date} (#{i+1})"
        
        with st.expander(display_title, expanded=(i == 0)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Distance", f"{workout['distance']:.2f} km")
                st.metric("Steps", f"{workout['steps']:,}")
                
                # Calculate duration
                start_time = datetime.datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.strptime(workout['end_timestamp'], '%Y-%m-%d %H:%M:%S')
                duration = end_time - start_time
                minutes = duration.total_seconds() / 60
                st.metric("Duration", f"{int(minutes)} minutes")
            
            with col2:
                st.metric("Calories Burned", f"{workout['calories_burned']} cal")
                
                # Create a chart showing start and end locations
                chart_data = pd.DataFrame([
                    {'point': 'Start', 'latitude': workout['start_lat_lng'][0], 'longitude': workout['start_lat_lng'][1]},
                    {'point': 'End', 'latitude': workout['end_lat_lng'][0], 'longitude': workout['end_lat_lng'][1]}
                ])
                
                # Create a chart
                st.write("Workout Path")
                chart = alt.Chart(chart_data).mark_circle(size=100).encode(
                    x=alt.X('longitude', title='Longitude'),
                    y=alt.Y('latitude', title='Latitude'),
                    color=alt.Color('point', scale=alt.Scale(domain=['Start', 'End'], range=['green', 'red'])),
                    tooltip=['point', 'latitude', 'longitude']
                ).properties(height=150)
                
                # Add a line connecting start and end points
                line_chart = alt.Chart(chart_data).mark_line().encode(
                    x='longitude',
                    y='latitude',
                    color=alt.value('gray')
                )
                
                st.altair_chart(chart + line_chart, use_container_width=True)
