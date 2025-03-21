#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# Updated in Unit 3: get_user_sensor_data now pulls data from BigQuery.
#############################################################################

from google.cloud import bigquery
import os
import random

# Ensure authentication is set (Make sure the JSON file exists)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# Dictionary to simulate user profiles
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
    'user4': {
        'full_name': 'Gemmy',
        'username': 'gems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user3'],
    },
}

def get_user_sensor_data(user_id: str, workout_id: str):
    """
    Fetches sensor data for a given workout from BigQuery.

    :param user_id: The ID of the user.
    :param workout_id: The ID of the workout.
    :return: A list of sensor data dictionaries with keys:
             sensor_type, timestamp, data, units.
    """
    client = bigquery.Client()

    query = f"""
        SELECT sensor_type, timestamp, data, units
        FROM `bigquery-sql-project-453401.CIS4993.sensor_data`
        WHERE user_id = @user_id AND workout_id = @workout_id
        ORDER BY timestamp ASC
    """

    query_params = [
        bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id),
    ]

    job_config = bigquery.QueryJobConfig(query_parameters=query_params)

    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()

        sensor_data = []
        for row in results:
            sensor_data.append({
                "sensor_type": row.sensor_type,
                "timestamp": row.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "data": row.data,
                "units": row.units
            })

        return sensor_data

    except Exception as e:
        print(f"Error fetching data from BigQuery: {e}")
        return []


def get_user_workouts(user_id):
    """Returns a list of user's workouts. Fetches workout data for a given user from BigQuery.
    
     Args:
        user_id: The ID of the user.
        
    Returns:
        A list of workout dictionaries with keys:
        - workout_id: Unique identifier for the workout
        - start_timestamp: When the workout started (format: 'YYYY-MM-DD HH:MM:SS')
        - end_timestamp: When the workout ended (format: 'YYYY-MM-DD HH:MM:SS')
        - start_lat_lng: List of [latitude, longitude] for the start location
        - end_lat_lng: List of [latitude, longitude] for the end location
        - distance: Distance covered in kilometers (float)
        - steps: Number of steps taken (integer)
        - calories_burned: Number of calories burned (integer)
    """
    from google.cloud import bigquery
    
    client = bigquery.Client()
    
    query = """
        SELECT 
            workout_id,
            start_timestamp,
            end_timestamp,
            start_latitude,
            start_longitude,
            end_latitude,
            end_longitude,
            distance,
            steps,
            calories_burned
        FROM `bigquery-sql-project-453401.CIS4993.workouts`
        WHERE user_id = @user_id
        ORDER BY start_timestamp DESC
    """
    
    query_params = [
        bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
    ]
    
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        workouts = []
        for row in results:
            try:
                # Safely convert values with error handling
                start_lat = float(row.start_latitude) if row.start_latitude is not None else 0.0
                start_lng = float(row.start_longitude) if row.start_longitude is not None else 0.0
                end_lat = float(row.end_latitude) if row.end_latitude is not None else 0.0
                end_lng = float(row.end_longitude) if row.end_longitude is not None else 0.0
                distance = float(row.distance) if row.distance is not None else 0.0
                steps = int(row.steps) if row.steps is not None else 0
                calories = int(row.calories_burned) if row.calories_burned is not None else 0
                
                # Create workout dictionary
                workout = {
                    'workout_id': row.workout_id,
                    'start_timestamp': row.start_timestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(row.start_timestamp, 'strftime') else str(row.start_timestamp),
                    'end_timestamp': row.end_timestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(row.end_timestamp, 'strftime') else str(row.end_timestamp),
                    'start_lat_lng': [start_lat, start_lng],
                    'end_lat_lng': [end_lat, end_lng],
                    'distance': distance,
                    'steps': steps,
                    'calories_burned': calories
                }
                workouts.append(workout)
            except Exception as e:
                print(f"Error processing workout row: {e}")
                continue
        
        return workouts
        
    except Exception as e:
        print(f"Error fetching workouts from BigQuery: {e}")
        # Return empty list on error
        return []


def get_user_profile(user_id):
    """Returns information about the given user.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')
    return users[user_id]


def get_user_posts(user_id):
    """Returns a list of a user's posts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    content = random.choice([
        'Had a great workout today!',
        'The AI really motivated me to push myself further, I ran 10 miles!',
    ])
    return [{
        'user_id': user_id,
        'post_id': 'post1',
        'timestamp': '2024-01-01 00:00:00',
        'content': content,
        'image': 'image_url',
    }]

def create_user_post(user_id, content, image=None):
    """
    Creates a new post for the specified user.
    
    Args:
        user_id: ID of the user creating the post
        content: Text content of the post
        image: Optional image URL for the post (defaults to None)
        
    Returns:
        The created post dictionary
    """
    import datetime
    import os
    from google.cloud import bigquery
    
    # Set the environment variable for Google credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"
    
    # Generate timestamp and post_id
    timestamp = datetime.datetime.now()
    post_id = f'post_{timestamp.strftime("%Y%m%d%H%M%S")}'
    
    # Create post object
    new_post = {
        'user_id': user_id,
        'post_id': post_id,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'content': content,
        'image': image
    }
    
    try:
        # Create BigQuery client
        client = bigquery.Client()
        
        # Define the table reference
        table_id = 'bigquery-sql-project-453401.CIS4993.posts'
        
        # Create a query to insert the post
        query = f"""
            INSERT INTO `{table_id}` (post_id, user_id, timestamp, content, image)
            VALUES (@post_id, @user_id, @timestamp, @content, @image)
        """
        
        query_params = [
            bigquery.ScalarQueryParameter("post_id", "STRING", post_id),
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("timestamp", "TIMESTAMP", timestamp),
            bigquery.ScalarQueryParameter("content", "STRING", content),
            bigquery.ScalarQueryParameter("image", "STRING", image if image else None),
        ]
        
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # Wait for the query to complete
        
    except Exception as e:
        print(f"Error creating post in BigQuery: {e}")
        # If there's an error with BigQuery, we'll at least store the post in memory
        # for the current session
        global posts
        if 'posts' not in globals():
            posts = {}
        
        if user_id not in posts:
            posts[user_id] = []
        
        posts[user_id].append(new_post)
    
    return new_post


def get_genai_advice(user_id):
    """Returns the most recent advice from the genai model.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    advice = random.choice([
        'Your heart rate indicates you can push yourself further. You got this!',
        "You're doing great! Keep up the good work.",
        'You worked hard yesterday, take it easy today.',
        'You have burned 100 calories so far today!',
    ])
    image = random.choice([
        'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        None,
    ])
    return {
        'advice_id': 'advice1',
        'timestamp': '2024-01-01 00:00:00',
        'content': advice,
        'image': image,
    }
