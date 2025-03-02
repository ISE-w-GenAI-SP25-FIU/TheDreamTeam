#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts
from data_fetcher import get_genai_advice, users
import re
from unittest.mock import MagicMock

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip()) 

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""
    
    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function"""

    def test_activity_summary(self):
        """Test workout summary logic"""

        workouts_list = [
            {
                'workout_id': 'workout 1',
                'start_timestamp': '2024-01-01 00:10:00',
                'end_timestamp': '2024-01-01 00:20:00',
                'start_lat_lng': 7.77,
                'end_lat_lng': 8.88,
                'distance': 10.0,
                'steps': 10000,
                'calories_burned': 50
            },  # Removed extra closing `}` here
            {
                'workout_id': 'workout 2',
                'start_timestamp': '2024-02-01 00:00:00',
                'end_timestamp': '2024-02-01 00:30:00',
                'start_lat_lng': 1.11,
                'end_lat_lng': 2.22,
                'distance': 5.0,
                'steps': 1000,
                'calories_burned': 10
            }  # Removed extra closing `}` here
        ]
        
        from modules import test_logic
        self.assertEqual(test_logic(workouts_list), workouts_list)


if __name__ == "__main__":
    unittest.main()

