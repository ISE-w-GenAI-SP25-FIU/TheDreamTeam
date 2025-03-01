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
from data_fetcher import get_genai_advice, users
import re
from unittest.mock import MagicMock

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip()) # Credit ChatGPT

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayActivitySummary(unittest.TestCase):
    """
    Tests the display_activity_summary function

    If workouts_list = ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400]
    then, test_logic(workouts_list) returns ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400]
    thus, list = ['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400]
    
    It's hard to perform Unit Testing in Streamlit components like st.write() or st.button()
    So, test_logic function can be tested independently from the Streamlit components 
    to indirectly make sure input data and output data match 
    
    """
    def test_activity_summary(self):
        from modules import test_logic
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[0], '1:31:29')
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[1], '3:46:38')
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[2], 4)
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[3], (25.745178, -80.366124))
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[4], (25.728228, -80.270986))
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[5], 15000)
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[6], 400)


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_css_styling(self):
        """Tests to ensure CSS styling is consistent for every user entry."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_css = normalize_whitespace(at.markdown[0].value)
            expected_css = normalize_whitespace("""
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
            assert actual_css == expected_css

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
            assert actual_first_line == expected_first_line
            assert actual_last_line == expected_last_line

    def test_header_text(self):
        """Tests to ensure module has an h2 header as first element in the div with the correct text."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_line = at.markdown[1].value.strip().split('\n')[1].strip()
            expected_line = '<h2>GenAI Advice</h2>'
            assert actual_line == expected_line

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
            assert actual_line in {f"<p>{advice}</p>" for advice in advice_options}

    def test_timestamp_text(self):
        """Tests to ensure module contains a paragraph element with the timestamp."""
        for user in users.keys():
            advice_data = get_genai_advice(user)
            at = AppTest.from_function(display_genai_advice, args=(advice_data['timestamp'], advice_data['content'], advice_data['image']))
            at.run()
            assert not at.exception

            actual_line = at.markdown[1].value.strip().split('\n')[3].strip()
            expected_line = '<p><em>2024-01-01 00:00:00</em></p>'
            assert actual_line == expected_line

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
            assert actual_line in valid_image_line or actual_line == ""

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
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
