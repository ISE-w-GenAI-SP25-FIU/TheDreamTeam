#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import random
from data_fetcher import (
    get_user_sensor_data, get_user_workouts, get_user_profile,
    get_genai_advice, get_user_posts, create_user_post
)

class TestDataFetcher(unittest.TestCase):

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_sensor_data(self, mock_bigquery_client):
        """Tests get_user_sensor_data function."""
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [
            MagicMock(sensor_type="Heart Rate", timestamp=datetime(2025, 3, 20, 12, 0, 0), data=75, units="bpm"),
            MagicMock(sensor_type="Steps", timestamp=datetime(2025, 3, 20, 12, 5, 0), data=100, units="count")
        ]
        
        result = get_user_sensor_data("user1", "workout1")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['sensor_type'], "Heart Rate")
        self.assertEqual(result[0]['data'], 75)
        self.assertEqual(result[1]['sensor_type'], "Steps")
        self.assertEqual(result[1]['data'], 100)

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_workouts(self, mock_bigquery_client):
        """Tests get_user_workouts function."""
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [
            MagicMock(
                WorkoutId="workout1",
                StartTimestamp=datetime(2025, 3, 20, 12, 0, 0),
                EndTimestamp=datetime(2025, 3, 20, 13, 0, 0),
                StartLocationLat=37.7749,
                StartLocationLong=-122.4194,
                EndLocationLat=37.7750,
                EndLocationLong=-122.4195,
                TotalDistance=5.5,
                TotalSteps=1000,
                CaloriesBurned=500
            )
        ]
        
        result = get_user_workouts("user1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['workout_id'], "workout1")
        self.assertEqual(result[0]['distance'], 5.5)
        self.assertEqual(result[0]['steps'], 1000)

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_posts(self, mock_bigquery_client):
        """Tests get_user_posts function."""
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [
            MagicMock(PostId="post1", AuthorId="user1", Timestamp=datetime(2025, 3, 22, 15, 30, 0), ImageUrl="http://example.com/image1.jpg", Content="First post!"),
            MagicMock(PostId="post2", AuthorId="user1", Timestamp=datetime(2025, 3, 21, 14, 20, 0), ImageUrl="http://example.com/image2.jpg", Content="Second post!")
        ]
        
        result = get_user_posts("user1")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['post_id'], "post1")
        self.assertEqual(result[0]['user_id'], "user1")
        self.assertEqual(result[0]['timestamp'], "2025-03-22 15:30:00")
        self.assertEqual(result[0]['content'], "First post!")
        self.assertEqual(result[0]['image'], "http://example.com/image1.jpg")

        self.assertEqual(result[1]['post_id'], "post2")
        self.assertEqual(result[1]['user_id'], "user1")
        self.assertEqual(result[1]['timestamp'], "2025-03-21 14:20:00")
        self.assertEqual(result[1]['content'], "Second post!")
        self.assertEqual(result[1]['image'], "http://example.com/image2.jpg")

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_profile(self, mock_bigquery_client):
        """Tests get_user_profile function."""
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [
            MagicMock(UserId1="friend1", UserId2="friend2", Username="remi_the_rems", Name="Remi", DateOfBirth="1990-01-01", ImageUrl="http://example.com/profile.jpg")
        ]
        
        result = get_user_profile("user1")
        self.assertEqual(result['full_name'], "Remi")
        self.assertEqual(result['username'], "remi_the_rems")
        self.assertEqual(result['date_of_birth'], "1990-01-01")
        self.assertEqual(result['profile_image'], "http://example.com/profile.jpg")
        self.assertIn("friend1", result['friends'])
        self.assertIn("friend2", result['friends'])

    @patch('data_fetcher.vertexai.init')
    @patch('data_fetcher.GenerativeModel')
    @patch('data_fetcher.get_user_profile')
    def test_get_genai_advice(self, mock_get_user_profile, mock_GenerativeModel, mock_vertexai_init):
        """Tests get_genai_advice function."""
        mock_get_user_profile.return_value = {'full_name': 'Remi'}
        mock_model_instance = mock_GenerativeModel.return_value
        mock_model_instance.generate_content.return_value.text = "Keep pushing forward!"
        
        result = get_genai_advice("user1")
        self.assertEqual(result['content'], "Keep pushing forward!")
        self.assertIn(result['image'], ['https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', None])

    @patch('data_fetcher.bigquery.Client')
    def test_create_user_post(self, mock_bigquery_client):
        """Tests create_user_post function."""
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = None  # Simulate successful insert
        
        result = create_user_post("user1", "This is a test post", "http://example.com/image.jpg")
        
        self.assertEqual(result['user_id'], "user1")
        self.assertEqual(result['content'], "This is a test post")
        self.assertEqual(result['image'], "http://example.com/image.jpg")
        self.assertTrue(result['post_id'].startswith('post_'))
        self.assertIn('timestamp', result)

if __name__ == '__main__':
    unittest.main()
