#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component


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
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
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


