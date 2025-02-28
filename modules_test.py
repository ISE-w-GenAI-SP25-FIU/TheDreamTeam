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
    def test_foo(self):
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[0], '1:31:29')
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[1], '3:46:38')
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[2], 4)
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[3], (25.745178, -80.366124))
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[4], (25.728228, -80.270986))
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[5], 15000)
        self.assertEqual(test_logic(['1:31:29', '3:46:38', 4, (25.745178, -80.366124), (25.728228, -80.270986), 15000, 400])[6], 400)


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
