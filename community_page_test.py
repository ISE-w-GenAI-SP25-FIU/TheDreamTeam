import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import streamlit as st
import sys
import os

# Add the parent directory to sys.path to import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
from community_page import toggle_view, set_time_period
from leaderboard_utils import (
    calculate_user_points, 
    get_user_rankings, 
    get_user_activity_metrics, 
    get_user_stats
)


class TestLeaderboardUtils(unittest.TestCase):
    """Test cases for the leaderboard utility functions."""

    @patch('leaderboard_utils.get_user_workouts')
    def test_calculate_user_points(self, mock_get_workouts):
        """Test the calculation of user points based on workouts."""
        # The actual function just returns mock data, so we'll test that it returns expected values
        # This avoids the actual calculation which depends on your real implementation
        points = calculate_user_points('user1', 'week')
        self.assertIsInstance(points, int)
        
        # If you want to test the actual calculation with mock data:
        # Just verify that day/week/month/year return different values as expected
        day_points = calculate_user_points('user1', 'day')
        week_points = calculate_user_points('user1', 'week')
        month_points = calculate_user_points('user1', 'month')
        year_points = calculate_user_points('user1', 'year')
        
        # Week should have more points than day, etc.
        self.assertGreaterEqual(week_points, day_points)
        self.assertGreaterEqual(month_points, week_points)
        self.assertGreaterEqual(year_points, month_points)
    
    def test_get_user_rankings(self):
        """Test that user rankings are retrieved correctly for different time periods."""
        # Test for each time period
        for period in ['day', 'week', 'month', 'year']:
            rankings = get_user_rankings(period)
            
            # Check that rankings have the expected format
            self.assertIsInstance(rankings, list)
            self.assertTrue(len(rankings) > 0)
            
            # Check that each ranking has the required fields
            for rank in rankings:
                self.assertIn('rank', rank)
                self.assertIn('user_id', rank)
                self.assertIn('name', rank)
                self.assertIn('points', rank)
                self.assertIn('profile_image', rank)
                
                # Check types
                self.assertIsInstance(rank['rank'], int)
                self.assertIsInstance(rank['user_id'], str)
                self.assertIsInstance(rank['name'], str)
                self.assertIsInstance(rank['points'], int)
    
    def test_get_user_activity_metrics(self):
        """Test that activity metrics are retrieved correctly for different time periods."""
        # Test for each time period
        for period in ['day', 'week', 'month', 'year']:
            metrics = get_user_activity_metrics('user1', period)
            
            # Check that metrics have the expected format
            self.assertIsInstance(metrics, list)
            
            # Check that each metric has the required fields
            for metric in metrics:
                self.assertIn('workout', metric)
                self.assertIn('kcals', metric)
                self.assertIn('miles', metric)
                self.assertIn('points', metric)
                
                # Check types
                self.assertIsInstance(metric['workout'], int)
                self.assertIsInstance(metric['kcals'], int)
                self.assertIsInstance(metric['miles'], float)
                self.assertIsInstance(metric['points'], int)
    
    def test_get_user_stats(self):
        """Test that user stats are retrieved correctly for different time periods."""
        # Test for each time period
        for period in ['day', 'week', 'month', 'year']:
            stats = get_user_stats('user1', period)
            
            # Check that stats have the expected format
            self.assertIsInstance(stats, dict)
            
            # Check that each stat has the required fields
            self.assertIn('total_points', stats)
            self.assertIn('global_rank', stats)
            self.assertIn('friend_rank', stats)
            self.assertIn('badges', stats)
            
            # Check types
            self.assertIsInstance(stats['total_points'], int)
            self.assertIsInstance(stats['global_rank'], int)
            self.assertIsInstance(stats['friend_rank'], int)
            self.assertIsInstance(stats['badges'], int)


class TestCommunityPage(unittest.TestCase):
    """Test cases for the community page components."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock Streamlit session state
        if not hasattr(st, 'session_state'):
            st.session_state = {}
        st.session_state.view_mode = "leaderboard"
        st.session_state.time_period = "Week"
        st.session_state.initialized = True
        
        # Create mock returns for st.columns
        self.mock_col1 = MagicMock()
        self.mock_col2 = MagicMock()
        self.mock_col3 = MagicMock()
        self.mock_col4 = MagicMock()
        self.mock_col5 = MagicMock()
        
        # Setup columns mock to return the right values
        self.mock_columns = MagicMock()
        self.mock_columns.return_value = [
            self.mock_col1, self.mock_col2, self.mock_col3, self.mock_col4, self.mock_col5
        ]
        
        # Apply patches
        self.patcher1 = patch('streamlit.markdown', MagicMock())
        self.patcher2 = patch('streamlit.image', MagicMock())
        self.patcher3 = patch('streamlit.button', MagicMock())
        self.patcher4 = patch('streamlit.tabs', MagicMock())
        self.patcher5 = patch('streamlit.dataframe', MagicMock())
        self.patcher6 = patch('streamlit.container', MagicMock())
        self.patcher7 = patch('streamlit.columns', self.mock_columns)
        
        # Start patches
        self.patcher1.start()
        self.patcher2.start()
        self.patcher3.start()
        self.patcher4.start()
        self.patcher5.start()
        self.patcher6.start()
        self.patcher7.start()
    
    def tearDown(self):
        """Clean up after tests."""
        # Stop patches
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        self.patcher5.stop()
        self.patcher6.stop()
        self.patcher7.stop()
    
    def test_toggle_view(self):
        """Test that toggle_view correctly switches between leaderboard and activity views."""
        # Start with leaderboard view
        st.session_state.view_mode = "leaderboard"
        
        # Mock st.rerun to avoid actual rerun
        with patch('streamlit.rerun'):
            # Toggle to activity view
            toggle_view()
            self.assertEqual(st.session_state.view_mode, "activity")
            
            # Toggle back to leaderboard view
            toggle_view()
            self.assertEqual(st.session_state.view_mode, "leaderboard")
    
    def test_set_time_period(self):
        """Test that set_time_period correctly updates the time period."""
        # Start with Week
        st.session_state.time_period = "Week"
        
        # Change to different periods
        set_time_period("Day")
        self.assertEqual(st.session_state.time_period, "Day")
        
        set_time_period("Month")
        self.assertEqual(st.session_state.time_period, "Month")
        
        set_time_period("Year")
        self.assertEqual(st.session_state.time_period, "Year")
    
    @patch('community_page.display_leaderboard')
    def test_display_badges(self, mock_display_leaderboard):
        """Test that badges are displayed correctly."""
        # We'll import and patch display_badges here to avoid issues with st.columns
        from community_page import display_badges
        
        # We just verify it runs without errors (mock implementation)
        display_badges()
    
    @patch('community_page.get_user_profile')
    @patch('community_page.get_user_rankings') 
    @patch('community_page.get_user_activity_metrics')
    def test_display_leaderboard(self, mock_metrics, mock_rankings, mock_profile):
        """Test that leaderboard display code runs without errors."""
        # Import here to avoid module-level issues
        from community_page import display_leaderboard
        
        # Set up mocks
        mock_profile.return_value = {'full_name': 'Test User', 'profile_image': 'test.jpg'}
        mock_rankings.return_value = [{'rank': 1, 'user_id': 'user1', 'name': 'User 1', 'points': 100, 'profile_image': ''}]
        mock_metrics.return_value = [{'workout': 1, 'kcals': 100, 'miles': 1.0, 'points': 105}]
        
        # Test both view modes
        for mode in ["leaderboard", "activity"]:
            st.session_state.view_mode = mode
            # Just verify it doesn't error
            display_leaderboard()


# Integration-style test that doesn't actually render UI but checks flow
class TestCommunityPageIntegration(unittest.TestCase):
    """Integration-style tests for the community page functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock Streamlit session state
        if not hasattr(st, 'session_state'):
            st.session_state = {}
        st.session_state.view_mode = "leaderboard"
        st.session_state.time_period = "Week"
        st.session_state.initialized = True
        
        # Mock all Streamlit functions to avoid rendering
        self.patcher = patch('streamlit.write', MagicMock())
        self.patcher.start()
    
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
    
    def test_leaderboard_tab_flow(self):
        """Test the overall flow of the leaderboard tab."""
        # Test switching view mode
        with patch('streamlit.rerun'):
            # Test mode switching
            toggle_view()  # Should switch to activity
            self.assertEqual(st.session_state.view_mode, "activity")
            
            toggle_view()  # Should switch back to leaderboard
            self.assertEqual(st.session_state.view_mode, "leaderboard")
        
        # Test changing time period
        set_time_period("Month")
        self.assertEqual(st.session_state.time_period, "Month")
        
        set_time_period("Year")
        self.assertEqual(st.session_state.time_period, "Year")


if __name__ == '__main__':
    unittest.main()