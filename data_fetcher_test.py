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
from data_fetcher import get_user_posts, get_genai_advice

class TestDataFetcher(unittest.TestCase):

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_posts(self, mock_bigquery_client):
        """Tests get_user_posts function."""
        
        # Mock BigQuery client and query result
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [
            MagicMock(PostId="123", AuthorId="user1", Timestamp=datetime(2025, 3, 20, 12, 0, 0), ImageUrl="http://example.com/image.jpg", Content="This is a test post"),
            MagicMock(PostId="124", AuthorId="user1", Timestamp=datetime(2025, 3, 19, 14, 30, 0), ImageUrl=None, Content="Another test post"),
        ]

        user_id = "user1"
        expected_output = [
            {
                'user_id': "user1",
                'post_id': "123",
                'timestamp': "2025-03-20 12:00:00",
                'content': "This is a test post",
                'image': "http://example.com/image.jpg",
            },
            {
                'user_id': "user1",
                'post_id': "124",
                'timestamp': "2025-03-19 14:30:00",
                'content': "Another test post",
                'image': None,
            }
        ]

        result = get_user_posts(user_id)
        self.assertEqual(result, expected_output)

    @patch('data_fetcher.GenerativeModel')
    @patch('data_fetcher.vertexai.init')
    @patch('data_fetcher.get_user_profile')
    def test_get_genai_advice(self, mock_get_user_profile, mock_vertexai_init, mock_generative_model):
        """Tests get_genai_advice function."""

        # Mock user profile
        mock_get_user_profile.return_value = {'full_name': 'John Doe'}

        # Mock VertexAI response
        mock_model_instance = mock_generative_model.return_value
        mock_response = MagicMock()
        mock_response.text = "Keep pushing forward, John!"
        mock_model_instance.generate_content.return_value = mock_response

        with patch('data_fetcher.random.choice', return_value="http://example.com/motivational.jpg"):
            user_id = "user1"
            result = get_genai_advice(user_id)

        self.assertEqual(result['advice_id'], 'advice1')
        self.assertTrue(result['timestamp'])  # Check if timestamp exists
        self.assertEqual(result['content'], "Keep pushing forward, John!")
        self.assertEqual(result['image'], "http://example.com/motivational.jpg")

if __name__ == "__main__":
    unittest.main()
