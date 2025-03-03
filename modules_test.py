#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts
from data_fetcher import get_genai_advice, get_user_posts, get_user_workouts, users
import re

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_display_username(self):
        """Tests username display on page."""
        for user in users.keys():
            posts_data = get_user_posts(user)
            for post in posts_data:
                full_name = users[post['user_id']]['full_name']
                at = AppTest.from_function(
                    display_post, 
                    args=(
                        full_name, 
                        users[post['user_id']]['profile_image'], 
                        post['timestamp'], 
                        post['content'], 
                        post['image']
                    )
                )
                at.run()
                assert not at.exception
                assert at.markdown[1].value == f"### {full_name}", "Incorrect full name displayed in post"

    def test_display_timestamp(self):
        """Tests timestamp display on page."""
        for user in users.keys():
            posts_data = get_user_posts(user)
            for post in posts_data:
                timestamp = post['timestamp']
                at = AppTest.from_function(
                    display_post, 
                    args=(
                        users[post['user_id']]['full_name'], 
                        users[post['user_id']]['profile_image'], 
                        timestamp,
                        post['content'],
                        post['image']
                    )
                )
                at.run()
                assert not at.exception
                assert at.markdown[2].value == f":calendar: {timestamp}", "Incorrect timestamp displayed in post"

    def test_display_content(self):
        """Tests content display on page."""
        for user in users.keys():
            posts_data = get_user_posts(user)
            for post in posts_data:
                content = post['content']
                at = AppTest.from_function(
                    display_post, 
                    args=(
                        users[post['user_id']]['full_name'], 
                        users[post['user_id']]['profile_image'], 
                        post['timestamp'],
                        content,
                        post['image']
                    )
                )
                at.run()
                assert not at.exception
                assert at.text[0].value == content, "Incorrect content displayed in post"


class TestDisplayActivitySummary(unittest.TestCase):
    """
    Tests the display_activity_summary function
    """
    def test_header(self):
        """Tests if header is displayed."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception
            assert at.header[0].value == "Workout Summary", "Displayed workout summary header is incorrect"

    def test_divider(self):
        """Tests if divider is displayed."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception
            assert at.markdown[1].value == "---", "Displayed workout summary divider is incorrect"

    def test_subheader(self):
        """Tests if subheader is displayed."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception
            assert at.subheader[0].value == "Total Workouts", "Displayed workout summary subheader is incorrect"

    def test_total_time(self):
        """Tests if total time that is displayed is calculated correctly."""
        from datetime import datetime
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception

            total_time = 0
            for index, workout in enumerate(workout_data):
                # Convert the string timestamps to datetime objects
                start_time = datetime.strptime(workout_data[index]['start_timestamp'], '%Y-%m-%d %H:%M:%S')

                end_time = datetime.strptime(workout_data[index]['end_timestamp'], '%Y-%m-%d %H:%M:%S')

                # Calculate the time difference in seconds
                time_difference = end_time - start_time
                total_seconds = time_difference.total_seconds()
                
                # Calculate the total time
                total_time += total_seconds

                # Extract hours, minutes, and seconds from the timedelta
                hours = total_time // 3600
                minutes = (total_time % 3600) // 60
                seconds = total_time % 60
            assert hours >= 0, "Total hours shouldn't ever be negative"
            assert minutes >= 0, "Total minutes shouldn't ever be negative"
            assert seconds >= 0, "Total seconds shouldn't ever be negative"
            assert at.text[0].value == f"- Total Time: {hours} hours, {minutes} minutes, {seconds} seconds", "Displayed total time is incorrect"

    def test_total_distance(self):
        """Tests if total distance that is displayed is calculated correctly."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception

            total_distance = 0
            for index, workout in enumerate(workout_data):
                total_distance += workout_data[index]['distance']
            assert total_distance >= 0, "Total distance shouldn't ever be negative"
            assert at.text[1].value == f"- Total Distance: {total_distance} km", "Displayed total distance is incorrect"

    def test_total_steps(self):
        """Tests if total steps that are displayed is calculated correctly."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception

            total_steps = 0
            for index, workout in enumerate(workout_data):
                total_steps += workout_data[index]['steps']
            assert total_steps >= 0, "Total steps shouldn't ever be negative"
            assert at.text[2].value == f"- Total Steps: {total_steps} steps", "Displayed total steps is incorrect"

    def test_total_calories_burned(self):
        """Tests if total calories burned that are displayed is calculated correctly."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data,))
            at.run()
            assert not at.exception

            total_calories_burned = 0
            for index, workout in enumerate(workout_data):
                total_calories_burned += workout_data[index]['calories_burned']
            assert total_calories_burned >= 0, "Total calories shouldn't ever be negative"
            assert at.text[3].value == f"- Total Calories Burned: {total_calories_burned} cal", "Displayed total calories burned is incorrect"
        
class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def normalize_whitespace(self, text):
        return re.sub(r'\s+', ' ', text.strip()) # Credit ChatGPT

    def test_css_styling(self):
        """Tests to ensure CSS styling is consistent for every user entry."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_css = self.normalize_whitespace(at.markdown[0].value)
            expected_css = self.normalize_whitespace("""
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
            """)
            assert actual_css == expected_css, "Incorrect CSS styling for GenAI Advice"

    def test_div_tags(self):
        """Tests to ensure module is in correct div container for every possible input user."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_first_line = at.markdown[1].value.strip().split('\n')[0].strip()
            actual_last_line = at.markdown[1].value.strip().split('\n')[-1].strip()
            expected_first_line = '<div class="genai-advice">'
            expected_last_line = '</div>'
            assert actual_first_line == expected_first_line, "Incorrect div container for GenAI Advice"
            assert actual_last_line == expected_last_line, "Incorrect div container for GenAI Advice"

    def test_header_text(self):
        """Tests to ensure module has an h2 header as first element in the div with the correct text."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_line = at.markdown[1].value.strip().split('\n')[1].strip()
            expected_line = '<h2>GenAI Advice</h2>'
            assert actual_line == expected_line, "Incorrect header for GenAI Advice"

    def test_advice_text(self):
        """Tests to ensure module contains one of the randomly generated advice texts."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            advice_options = (
                'Your heart rate indicates you can push yourself further. You got this!',
                "You're doing great! Keep up the good work.",
                'You worked hard yesterday, take it easy today.',
                'You have burned 100 calories so far today!',
            )
            actual_line = at.markdown[1].value.strip().split('\n')[2].strip()
            assert actual_line in {f"<p>{advice}</p>" for advice in advice_options}, "Incorrect advice text for GenAI Advice"

        # Test with no advice
        at = AppTest.from_function(display_genai_advice, args=(None, None, None))
        at.run()
        assert not at.exception
        actual_line = at.markdown[1].value.strip().split('\n')[2].strip()
        assert actual_line == '<p>No advice today :(</p>', "Incorrect advice text when no advice is available"

    def test_timestamp_text(self):
        """Tests to ensure module contains a paragraph element with the timestamp."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_line = at.markdown[1].value.strip().split('\n')[3].strip()
            expected_line = '<p><em>2024-01-01 00:00:00</em></p>'
            assert actual_line == expected_line, "Incorrect timestamp for GenAI Advice"

        # Test with no timestamp
        at = AppTest.from_function(display_genai_advice, args=(None, None, None))
        at.run()
        assert not at.exception
        actual_line = at.markdown[1].value.strip().split('\n')[3].strip()
        assert actual_line == '', "Timestamp should not exist when one isn't given for GenAI Advice"

    def test_motivational_image(self):
        """Tests to ensure module contains a paragraph element with the timestamp."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            image_options = (
                'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                None,
            )
            valid_image_line = {f'<img src="{image}" width="200">' for image in image_options}
            actual_line = at.markdown[1].value.strip().split('\n')[4].strip()
            assert actual_line in valid_image_line or actual_line == "", "Incorrect image for GenAI Advice"

class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_display_recent_workouts(self): 
        """Test display_recent_workouts function with varied workout data."""
        from unittest.mock import patch
        
        # Create a diverse set of mock workouts with different datesstre
        varied_workouts = [
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-02-27 08:30:00',
                'end_timestamp': '2024-02-27 09:15:00',
                'start_lat_lng': (1.55, 4.55),
                'end_lat_lng': (1.85, 4.85),
                'distance': 3.2,
                'steps': 4500,
                'calories_burned': 85,
            },
            {
                'workout_id': 'workout2',
                'start_timestamp': '2024-02-25 07:45:00',
                'end_timestamp': '2024-02-25 08:30:00',
                'start_lat_lng': (1.22, 4.22),
                'end_lat_lng': (1.77, 4.77),
                'distance': 4.5,
                'steps': 6200,
                'calories_burned': 120,
            },
            {
                'workout_id': 'workout3',
                'start_timestamp': '2024-02-23 18:15:00',
                'end_timestamp': '2024-02-23 19:00:00',
                'start_lat_lng': (1.33, 4.33),
                'end_lat_lng': (1.66, 4.66),
                'distance': 2.8,
                'steps': 3800,
                'calories_burned': 75,
            },
            {
                'workout_id': 'workout4',
                'start_timestamp': '2024-02-20 12:00:00',
                'end_timestamp': '2024-02-20 12:45:00',
                'start_lat_lng': (1.44, 4.44),
                'end_lat_lng': (1.88, 4.88),
                'distance': 5.1,
                'steps': 7300,
                'calories_burned': 135,
            },
            {
                'workout_id': 'workout5',
                'start_timestamp': '2024-02-18 16:30:00',
                'end_timestamp': '2024-02-18 17:15:00',
                'start_lat_lng': (1.11, 4.11),
                'end_lat_lng': (1.99, 4.99),
                'distance': 3.7,
                'steps': 5200,
                'calories_burned': 95,
            }
        ]
        
        # Use patch as a context manager to mock streamlit and other dependencies
        with patch('modules.st'), patch('modules.pd'), patch('modules.alt'):
            # Import and test the function
            from modules import display_recent_workouts
            display_recent_workouts(varied_workouts)
            
        # If we get here without exceptions, the test passes
        self.assertTrue(True), "Error in unit test to display recent workouts"

if __name__ == "__main__":
    unittest.main()
