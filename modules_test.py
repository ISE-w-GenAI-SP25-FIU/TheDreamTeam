#############################################################################
# modules_test.py
#
# This file contains tests for modules.py using AppTest.
#
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_activity_summary, validate_workouts, display_post, display_recent_workouts, display_genai_advice


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function using AppTest"""

    def test_activity_summary(self):
        """Test if activity summary renders correctly in Streamlit"""

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

        app = AppTest(display_activity_summary, args=[workouts_list])
        app.run()

        # Check if UI contains expected elements
        app.assert_text("Workout Summary")
        app.assert_text("Workout #1")
        app.assert_text("Start Time: 2024-01-01 00:10:00")
        app.assert_text("End Time: 2024-01-01 00:20:00")
        app.assert_text("Distance: 10.0 km")
        app.assert_text("Steps: 10,000")
        app.assert_text("Calories burned: 50")


class TestValidateWorkouts(unittest.TestCase):
    """Tests the validate_workouts function"""

    def test_validate_workouts(self):
        """Ensure validate_workouts returns correct data"""
        workouts_list = [
            {"workout_id": "workout_1", "distance": 10.0},
            {"workout_id": "workout_2", "distance": 5.0},
        ]
        self.assertEqual(validate_workouts(workouts_list), workouts_list)


class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function using AppTest"""

    def test_display_post(self):
        """Ensure display_post renders correctly in Streamlit"""

        app = AppTest(
            display_post,
            args=[
                "John Doe",
                "https://example.com/sample-profile.jpg",
                "2024-01-01",
                "This is a post!",
                None,
            ],
        )
        app.run()

        # Verify UI elements
        app.assert_text("John Doe")
        app.assert_text("📅 2024-01-01")
        app.assert_text("This is a post!")
        app.assert_image("https://example.com/sample-profile.jpg")


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function using AppTest"""

    def test_display_recent_workouts(self):
        """Ensure recent workouts display correctly in Streamlit"""

        workouts = [
            {
                "workout_id": "workout_1",
                "start_timestamp": "2024-01-01 00:10:00",
                "end_timestamp": "2024-01-01 00:20:00",
                "distance": 10.0,
                "steps": 10000,
                "calories_burned": 50,
                "start_lat_lng": (7.77, 4.55),
                "end_lat_lng": (8.88, 4.75),
            }
        ]

        app = AppTest(display_recent_workouts, args=[workouts])
        app.run()

        app.assert_text("Recent Workouts")
        app.assert_text("Workout on January 01, 2024 (#1)")
        app.assert_text("Distance: 10.0 km")
        app.assert_text("Steps: 10,000")
        app.assert_text("Calories Burned: 50 cal")


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function using AppTest"""

    def test_display_genai_advice(self):
        """Ensure GenAI advice renders correctly in Streamlit"""

        app = AppTest(
            display_genai_advice,
            args=["2024-01-01", "Stay motivated!", None],
        )
        app.run()

        app.assert_text("GenAI Advice")
        app.assert_text("Stay motivated!")
        app.assert_text("2024-01-01")


if __name__ == "__main__":
    unittest.main()
