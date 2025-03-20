#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

import random
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
from datetime import datetime

PROJECT_ID = "dreamteamproject-449421"

users = {
    'user1': {
        'full_name': 'Remi',
        'username': 'remi_the_rems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user2', 'user3', 'user4'],
    },
    'user2': {
        'full_name': 'Blake',
        'username': 'blake',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1'],
    },
    'user3': {
        'full_name': 'Jordan',
        'username': 'jordanjordanjordan',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user4'],
    },
}


def get_user_sensor_data(user_id, workout_id):
    """Returns a list of timestampped information for a given workout.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    sensor_data = []
    sensor_types = [
        'accelerometer',
        'gyroscope',
        'pressure',
        'temperature',
        'heart_rate',
    ]
    for index in range(random.randint(5, 100)):
        random_minute = str(random.randint(0, 59))
        if len(random_minute) == 1:
            random_minute = '0' + random_minute
        timestamp = '2024-01-01 00:' + random_minute + ':00'
        data = random.random() * 100
        sensor_type = random.choice(sensor_types)
        sensor_data.append(
            {'sensor_type': sensor_type, 'timestamp': timestamp, 'data': data}
        )
    return sensor_data


def get_user_workouts(user_id):
    """Returns a list of user's workouts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    workouts = []
    for index in range(random.randint(1, 3)):
        random_lat_lng_1 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        random_lat_lng_2 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        workouts.append({
            'workout_id': f'workout{index}',
            'start_timestamp': '2024-01-01 00:00:00',
            'end_timestamp': '2024-01-01 00:30:00',
            'start_lat_lng': random_lat_lng_1,
            'end_lat_lng': random_lat_lng_2,
            'distance': random.randint(0, 200) / 10.0,
            'steps': random.randint(0, 20000),
            'calories_burned': random.randint(0, 100),
        })
    return workouts

def get_user_posts(user_id):
    """Returns a list of posts for a specific user."""
    
    client = bigquery.Client(project=PROJECT_ID)
    
    QUERY = """
        SELECT PostId, AuthorId, Timestamp, ImageUrl, Content
        FROM `dreamteamproject-449421.DreamDataset.Posts`
        WHERE AuthorId = @user_id
        ORDER BY Timestamp DESC
    """
    
    # Use parameterized queries to prevent SQL injection - Credit ChatGPT
    query_job = client.query(QUERY, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    ))

    rows = query_job.result()

    return [{
        'user_id': row.AuthorId,
        'post_id': row.PostId,
        'timestamp': row.Timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'content': row.Content,
        'image': row.ImageUrl,
    } for row in rows]

def get_user_profile(user_id):
    """
    Input: user_id 
    Output: A single dictionary with the keys full_name, username, date_of_birth, 
    profile_image, and friends (containing a list of friend user_ids) 
    """
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')

    # Initialize the BigQuery client
    client = bigquery.Client(project=PROJECT_ID)

    # Define id variable for user with the user_id param
    user_id = user_id

    # SQL query for friends list(friends ids), full_name, username, date_of_birth, profile_image
    query = f"""
        SELECT friends.UserId1, friends.UserId2, users.Username, users.Name, users.ImageUrl, users.DateOfBirth
        FROM `dreamteamproject-449421.DreamDataset.Friends` AS friends, `dreamteamproject-449421.DreamDataset.Users` AS users
        WHERE NOT (friends.UserId1 = @user_id OR friends.UserId2 = @user_id) AND users.UserId = @user_id
    """

    # Define query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        ]
    )

    # Execute the query
    query_job = client.query(query, job_config=job_config)

    # Fetch the results
    results = query_job.result()

    # user profile dict to return
    user_profile={}

    # Print the result
    for row in results:
        user_profile['full_name'] = row.Name
        user_profile['username'] = row.Username
        user_profile['date_of_birth'] = row.DateOfBirth
        user_profile['profile_image'] = row.ImageUrl
        user_profile['friends'] = [row.UserId1, row.UserId2]

    return user_profile


def get_genai_advice(user_id):
    """Returns the most recent advice and a motivational workout image based on the user's profile."""

    user_profile = get_user_profile(user_id)
    if not user_profile:
        return None
    
    user_name = user_profile['full_name']

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    query = f"Can you please give {user_name} a short motivational quote or short piece of advice to improve workouts? Only refer to them by their first name please"
    response = model.generate_content(query)

    image = random.choice([
    'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    None,
    ])

    # Return the data
    return {
        'advice_id': 'advice1',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'content': response.text,
        'image': image,
    }



