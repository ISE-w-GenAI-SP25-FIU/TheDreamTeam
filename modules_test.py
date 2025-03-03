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
    def test_foo(self):
        """Tests foo."""
        for user in users.keys():
            workout_data = get_user_workouts(user)
            at = AppTest.from_function(display_activity_summary, args=(workout_data))
            at.run()
            #assert not at.exception
            #assert at.markdown[1].value == f"### {full_name}", "Incorrect full name displayed in post"
        
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

    def test_foo(self):
        """Tests foo."""
        pass

if __name__ == "__main__":
    unittest.main()
