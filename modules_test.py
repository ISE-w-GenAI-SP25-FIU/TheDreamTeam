#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_activity_summary, validate_workouts, display_post, display_recent_workouts, display_genai_advice
from unittest.mock import patch
import re

def normalize_whitespace(text):
    """Helper function to remove extra whitespace for string comparisons."""
    return re.sub(r'\s+', ' ', text.strip())

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function"""

    @patch("streamlit.subheader")
    @patch("streamlit.write")
    def test_activity_summary(self, mock_write, mock_subheader):
        """Test workout summary logic"""

        workouts_list = [
            {
                "workout_id": "workout_1",
                "start_timestamp": "2024-01-01 00:10:00",
                "end_timestamp": "2024-01-01 00:20:00",
                "start_lat_lng": (7.77, 4.55),
                "end_lat_lng": (8.88, 4.75),
                "distance": 10.0,
                "steps": 10000,
                "calories_burned": 50,
            }
        ]

        display_activity_summary(workouts_list)

        mock_write.assert_any_call("- Start Time: 2024-01-01 00:10:00")
        mock_write.assert_any_call("- Distance: 10.0 km")
        mock_write.assert_any_call("- Steps: 10000")

    def test_validate_workouts(self):
        """Test validate_workouts function returns input data correctly"""
        workouts_list = [
            {"workout_id": "workout_1", "distance": 10.0},
            {"workout_id": "workout_2", "distance": 5.0},
        ]
        self.assertEqual(validate_workouts(workouts_list), workouts_list)

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    @patch("streamlit.write")
    def test_display_post(self, mock_write):
        """Ensures the display_post function outputs expected text."""
        display_post("John Doe", "user_img.jpg", "2024-01-01", "This is a post!", None)

        mock_write.assert_any_call("📅 2024-01-01")
        mock_write.assert_any_call("This is a post!")

if __name__ == "__main__":
    unittest.main()
