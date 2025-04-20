import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import streamlit as st
import sys
import os

# Add the parent directory to sys.path to import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
from community_page import toggle_view, set_time_period, display_leaderboard, display_badges
from leaderboard_utils import (
    calculate_user_points, 
    get_user_rankings, 
    get_user_activity_metrics, 
    get_user_stats
)


class TestLeaderboardUtils(unittest.TestCase):
    """Test cases for the leaderboard utility functions."""

    def test_calculate_user_points(self):
        """Test the calculation of user points based on workouts."""
        # Mock data
        mock_workouts = [
            {
                'workout_id': 'workout1',
                'calories_burned': 100,
                'distance': 2.0,  # km
                'start_timestamp': '2024-04-15 10:00:00'
            },
            {
                'workout_id': 'workout2',
                'calories_burned': 200,
                'distance': 4.0,  # km
                'start_timestamp': '2024-04-16 11:00:00'
            }
        ]
        
        # Mock the get_user_workouts function
        with patch('leaderboard_utils.get_user_workouts', return_value=mock_workouts):
            # Calculate points (1 calorie = 1 point, 1 mile = 5 points)
            points = calculate_user_points('user1', 'week')
            
            # Expected: 100 + 200 (calories) + 2*0.621371*5 + 4*0.621371*5 (miles to points) = 300 + 18.64 ≈ 318
            expected_points = 300 + int((2.0 + 4.0) * 0.621371 * 5)
            self.assertEqual(points, expected_points)
    
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
        
        # Mock Streamlit functions
        self.mock_markdown = MagicMock()
        self.mock_image = MagicMock()
        self.mock_button = MagicMock()
        self.mock_tabs = MagicMock()
        self.mock_dataframe = MagicMock()
        self.mock_container = MagicMock()
        self.mock_columns = MagicMock()
        
        # Apply patches
        self.patcher1 = patch('streamlit.markdown', self.mock_markdown)
        self.patcher2 = patch('streamlit.image', self.mock_image)
        self.patcher3 = patch('streamlit.button', self.mock_button)
        self.patcher4 = patch('streamlit.tabs', self.mock_tabs)
        self.patcher5 = patch('streamlit.dataframe', self.mock_dataframe)
        self.patcher6 = patch('streamlit.container', self.mock_container)
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
    
    def test_display_leaderboard(self):
        """Test that display_leaderboard handles both view modes correctly."""
        # Mock user profile and other dependencies
        mock_user_profile = {'full_name': 'Test User', 'profile_image': 'test.jpg'}
        
        # Test leaderboard view
        with patch('community_page.get_user_profile', return_value=mock_user_profile), \
             patch('community_page.get_user_rankings'), \
             patch('community_page.get_user_activity_metrics'):
            
            # Test with leaderboard view
            st.session_state.view_mode = "leaderboard"
            display_leaderboard()
            
            # Check that markdown was called with user name
            name_found = False
            for call in self.mock_markdown.call_args_list:
                if 'Test User' in str(call):
                    name_found = True
                    break
            self.assertTrue(name_found)
            
            # Test with activity view
            st.session_state.view_mode = "activity"
            display_leaderboard()
            
            # Check that "Activity Metrics" was mentioned
            activity_found = False
            for call in self.mock_markdown.call_args_list:
                if 'Activity Metrics' in str(call):
                    activity_found = True
                    break
            self.assertTrue(activity_found)
    
    def test_display_badges(self):
        """Test that display_badges correctly shows badge icons."""
        # We just check that it doesn't raise exceptions
        display_badges()
        
        # Verify markdown was called for badges
        badges_found = False
        for call in self.mock_markdown.call_args_list:
            if 'Badges' in str(call):
                badges_found = True
                break
        self.assertTrue(badges_found)


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
    
    @patch('community_page.get_user_profile')
    @patch('community_page.get_user_rankings')
    @patch('community_page.get_user_activity_metrics')
    @patch('community_page.get_user_stats')
    @patch('community_page.get_genai_advice')
    @patch('community_page.get_user_posts')
    def test_leaderboard_tab_flow(self, mock_posts, mock_advice, mock_stats, mock_metrics, mock_rankings, mock_profile):
        """Test the overall flow of the leaderboard tab."""
        # Set up mocks
        mock_profile.return_value = {'full_name': 'Test User', 'profile_image': 'test.jpg', 'friends': []}
        mock_rankings.return_value = [{'rank': 1, 'user_id': 'user1', 'name': 'User 1', 'points': 100, 'profile_image': ''}]
        mock_metrics.return_value = [{'workout': 1, 'kcals': 100, 'miles': 1.0, 'points': 105}]
        mock_stats.return_value = {'total_points': 100, 'global_rank': 5, 'friend_rank': 1, 'badges': 3}
        
        # Test switching view mode
        with patch('streamlit.button', return_value=True), patch('streamlit.rerun'):
            toggle_view()  # Should switch to activity
            self.assertEqual(st.session_state.view_mode, "activity")
            
            toggle_view()  # Should switch back to leaderboard
            self.assertEqual(st.session_state.view_mode, "leaderboard")
        
        # Test changing time period
        with patch('streamlit.tabs'):
            set_time_period("Month")
            self.assertEqual(st.session_state.time_period, "Month")
            
            set_time_period("Year")
            self.assertEqual(st.session_state.time_period, "Year")


if __name__ == '__main__':
    unittest.main()