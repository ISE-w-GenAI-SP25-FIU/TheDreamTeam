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
    if workouts_list = ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400],
    
    Start Time: 1:31:29
    End Time: 3:46:38
    Distance: 4
    Start Coordinates: (25.745178, -80.366124)
    End Coordinates: (25.728228, -80.270986)
    Steps: 15000
    Calories burned: 400
    """

    st.title("Workout Summary")
    st.markdown('Work out fun!!!!! :joy:')

    # [start_time, end_time, distance, steps, calories burned, start_coordinates, end_coordinates]
    # if workouts_list = ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400]
    # then, test_logic(workouts_list) returns ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400]
    # thus, list = ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400]
    
    # It's hard to perform Unit Testing in Streamlit components like st.write() or st.button()
    # So, test_logic function can be tested independently from the Streamlit components 
    # to indirectly make sure input data and output data match 
    
    list = test_logic(workouts_list)
    for index, workout in enumerate(list):
        st.subheader(f"Workout #{index + 1}")
        st.write(f"- Start Time: {workout["start_timestamp"]}")
        st.write(f"- End Time: {workout["end_timestamp"]}")
        st.write(f"- Distance: {workout["distance"]}")
        st.write(f"- Start Coordinates: {workout["start_lat_lng"]}")
        st.write(f"- End Coordinates: {workout["end_lat_lng"]}")
        st.write(f"- Steps: {workout["steps"]}")
        st.write(f"- Calories burned: {workout["calories_burned"]}")

def test_logic(workouts_list):
    return workouts_list


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    data = {
        'WORKOUTS' : workouts_list,
        
    }

    html_file_name = "workouts_page"
    create_component(data, html_file_name)

    pass

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


