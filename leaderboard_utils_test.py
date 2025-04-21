import unittest

from leaderboard_utils import get_user_rankings

class TestGetUserRankings(unittest.TestCase):

    self.current_period = "month"

    def test_valid_user_id(self):
        """Test for a valid user ID"""
        user_id = 1
        expected_rankings = ["Gold", "Silver", "Bronze"]
        actual_rankings = get_user_rankings(self.current_period)
        self.assertEqual(actual_rankings, expected_rankings)

    def test_user_with_no_rankings(self):
        """Test for a valid user ID with no rankings"""
        user_id = 4  # Assuming user_id 4 doesn't exist or has no rankings
        expected_rankings = []
        actual_rankings = get_user_rankings(self.current_period)
        self.assertEqual(actual_rankings, expected_rankings)

    def test_invalid_user_id(self):
        """Test for an invalid user ID"""
        user_id = 999  # Assuming this is an invalid user ID
        expected_rankings = []
        actual_rankings = get_user_rankings(self.current_period)
        self.assertEqual(actual_rankings, expected_rankings)

    def test_edge_case_empty_user_id(self):
        """Test for empty or invalid user ID"""
        user_id = None  # or some edge case like an empty string
        expected_rankings = []
        actual_rankings = get_user_rankings(self.current_period)
        self.assertEqual(actual_rankings, expected_rankings)

if __name__ == '__main__':
    unittest.main()