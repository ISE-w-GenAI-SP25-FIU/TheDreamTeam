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

#patches
@patch('google.cloud.bigquery.Client')
@patch('vertexai.init')
@patch('vertexai.generative_models.GenerativeModel')

class TestLeaderboardUtils(unittest.TestCase):
    """Test cases for the leaderboard utility functions."""

    def test_calculate_user_points(self):
        """Test the calculation of user points based on workouts."""
        # Simply verify the function returns a valid result for each time period
        day_points = calculate_user_points('user1', 'day')
        week_points = calculate_user_points('user1', 'week')
        month_points = calculate_user_points('user1', 'month')
        year_points = calculate_user_points('user1', 'year')
        
        # Verify they're integers
        self.assertIsInstance(day_points, int)
        self.assertIsInstance(week_points, int)
        self.assertIsInstance(month_points, int)
        self.assertIsInstance(year_points, int)
        
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


class TestCommunityPageFunctions(unittest.TestCase):
    """Test cases for specific community page functions."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock Streamlit session state
        if not hasattr(st, 'session_state'):
            st.session_state = {}
        st.session_state.view_mode = "leaderboard"
        st.session_state.time_period = "Week"
        st.session_state.initialized = True
    
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