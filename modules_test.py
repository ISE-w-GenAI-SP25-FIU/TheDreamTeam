#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
#############################################################################

import unittest
from unittest.mock import patch
from modules import (
    display_post,
    display_activity_summary,
    display_genai_advice,
    display_recent_workouts,
    test_logic
)
from data_fetcher import get_genai_advice, users
import re


def normalize_whitespace(text):
    """Helper function to remove extra whitespace for string comparisons."""
    return re.sub(r'\s+', ' ', text.strip())


# ----------------------------------------------
#  TEST: display_post()
# ----------------------------------------------
class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    @patch("streamlit.write")
    @patch("streamlit.image")
    def test_display_post(self, mock_image, mock_write):
        """Tests that display_post correctly renders user posts."""
        display_post(
            "Alice",
            "profile.jpg",
            "2025-03-01 12:00:00",
            "Hello World!",
            "post.jpg",
        )

        #  Ensure Streamlit functions were called correctly
        mock_write.assert_any_call("📅 2025-03-01 12:00:00")
        mock_write.assert_any_call("Hello World!")
        mock_image.assert_any_call("profile.jpg", width=50)
        mock_image.assert_any_call("post.jpg", width=200)


# ----------------------------------------------
# TEST: display_activity_summary()
# ----------------------------------------------
class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function"""

    @patch("streamlit.subheader")
    @patch("streamlit.write")
    def test_activity_summary(self, mock_write, mock_subheader):
        """Test workout summary logic"""
        workouts_list = [
            {
                "workout_id": "workout_1",  #  Fixed incorrect syntax
                "start_timestamp": "2024-01-01 00:10:00",
                "end_timestamp": "2024-01-01 00:20:00",
                "start_lat_lng": (7.77, 4.55),  #  Fixed incorrect formatting
                "end_lat_lng": (8.88, 4.75),  #  Fixed incorrect formatting
                "distance": 10.0,
                "steps": 10000,
                "calories_burned": 50,
            },
            {
                "workout_id": "workout_2",
                "start_timestamp": "2024-02-01 00:00:00",
                "end_timestamp": "2024-02-01 00:30:00",
                "start_lat_lng": (1.11, 4.22),
                "end_lat_lng": (2.22, 4.44),
                "distance": 5.0,
                "steps": 1000,
                "calories_burned": 10,
            },
        ]

        #  Run function
        display_activity_summary(workouts_list)

        #  Ensure correct values were written
        mock_write.assert_any_call("- Start Time: 2024-01-01 00:10:00")
        mock_write.assert_any_call("- Distance: 10.0")
        mock_write.assert_any_call("- Steps: 10000")
        mock_write.assert_any_call("- Calories burned: 50")


# ----------------------------------------------
# TEST: display_recent_workouts()
# ----------------------------------------------
class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests display_recent_workouts function."""

    @patch("streamlit.subheader")
    @patch("streamlit.expander")
    @patch("streamlit.metric")
    def test_display_recent_workouts(self, mock_metric, mock_expander, mock_subheader):
        """Test if recent workouts are displayed correctly."""

        test_workouts = [
            {
                "workout_id": "workout_1",
                "start_timestamp": "2024-02-27 08:30:00",
                "end_timestamp": "2024-02-27 09:15:00",
                "start_lat_lng": (1.55, 4.55),
                "end_lat_lng": (1.85, 4.85),
                "distance": 3.2,
                "steps": 4500,
                "calories_burned": 85,
            }
        ]

        display_recent_workouts(test_workouts)

        mock_subheader.assert_called_with("Recent Workouts")
        mock_expander.assert_called()
        mock_metric.assert_any_call("Distance", "3.20 km")
        mock_metric.assert_any_call("Steps", "4,500")
        mock_metric.assert_any_call("Calories Burned", "85 cal")


# ----------------------------------------------
# TEST: get_genai_advice()
# ----------------------------------------------
class TestGenAiAdvice(unittest.TestCase):
    """Tests the get_genai_advice function."""

    def test_genai_advice(self):
        """Ensures GenAI advice returns a valid string."""
        user_id = "user1"
        advice = get_genai_advice(user_id)

        self.assertIn("content", advice)
        self.assertIsInstance(advice["content"], str)
        self.assertIn("timestamp", advice)


# ----------------------------------------------
# RUN TESTS
# ----------------------------------------------
if __name__ == "__main__":
    unittest.main()

