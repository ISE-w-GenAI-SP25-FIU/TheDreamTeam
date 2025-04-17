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

def get_user_sensor_data(user_id: str, workout_id: str):
    """
    Fetches sensor data for a given workout from BigQuery.

    :param user_id: The ID of the user.
    :param workout_id: The ID of the workout.
    :return: A list of sensor data dictionaries.
    """
    client = bigquery.Client(project=PROJECT_ID)

    query = """
        SELECT
            st.sensor_type_name AS sensor_type,
            sd.timestamp,
            sd.data,
            sd.units
        FROM `dreamteamproject-449421.DreamDataset.SensorData` sd
        JOIN `dreamteamproject-449421.DreamDataset.SensorTypes` st
        ON sd.sensor_type_id = st.sensor_type_id
        WHERE sd.user_id = @user_id AND sd.workout_id = @workout_id
        ORDER BY sd.timestamp
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id),
        ]
    )

    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()

        sensor_data = []
        for row in results:
            sensor_data.append({
                "sensor_type": row.sensor_type,
                "timestamp": row.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "data": row.data,
                "units": row.units,
            })

        return sensor_data

    except Exception as e:
        print(f"Error fetching sensor data: {e}")
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
    
    client = bigquery.Client(project=PROJECT_ID)
    
    query = """
        SELECT 
            WorkoutId,
            StartTimestamp,
            EndTimestamp,
            StartLocationLat,
            StartLocationLong,
            EndLocationLat,
            EndLocationLong,
            TotalDistance,
            TotalSteps,
            CaloriesBurned
        FROM `dreamteamproject-449421.DreamDataset.Workouts`
        WHERE UserId = @user_id
        ORDER BY StartTimestamp DESC
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
                start_lat = float(row.StartLocationLat) if row.StartLocationLat is not None else 0.0
                start_lng = float(row.StartLocationLong) if row.StartLocationLong is not None else 0.0
                end_lat = float(row.EndLocationLat) if row.EndLocationLat is not None else 0.0
                end_lng = float(row.EndLocationLong) if row.EndLocationLong is not None else 0.0
                distance = float(row.TotalDistance) if row.TotalDistance is not None else 0.0
                steps = int(row.TotalSteps) if row.TotalSteps is not None else 0
                calories = int(row.CaloriesBurned) if row.CaloriesBurned is not None else 0
                
                # Create workout dictionary
                workout = {
                    'workout_id': row.WorkoutId,
                    'start_timestamp': row.StartTimestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(row.StartTimestamp, 'strftime') else str(row.StartTimestamp),
                    'end_timestamp': row.EndTimestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(row.EndTimestamp, 'strftime') else str(row.EndTimestamp),
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
        return []

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
    from google.cloud import bigquery
    
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
        client = bigquery.Client(project=PROJECT_ID)
        
        # Define the table reference
        table_id = 'dreamteamproject-449421.DreamDataset.Posts'
        
        # Create a query to insert the post
        query = f"""
            INSERT INTO `{table_id}` (PostId, AuthorId, Timestamp, Content, ImageUrl)
            VALUES (@post_id, @user_id, @timestamp, @content, @image)
        """
        
        query_params = [
            bigquery.ScalarQueryParameter("post_id", "STRING", post_id),
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("timestamp", "DATETIME", timestamp),
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

# Table name
TABLE_NAME = "dreamteamproject-449421.DreamDataset.Favorites"

def add_favorite(user_id, exercise):
    """Add a favorite exercise to the BigQuery table."""
    client = bigquery.Client(project=PROJECT_ID)
    row = {
        "UserId": user_id,
        "Exercise": exercise
    }

    # Insert the row into BigQuery
    try:
        client.insert_rows_json(TABLE_NAME, [row])  # Send the exercise as a JSON record
        print(f"Exercise {exercise['name']} added to favorites.")
    except Exception as e:
        print(f"Error adding favorite: {e}")

def remove_favorite(user_id, exercise_name):
    """Mark a favorite exercise as deleted in the BigQuery table."""
    client = bigquery.Client(project=PROJECT_ID)

    # Construct the UPDATE query to set IsDeleted to True for the given user and exercise
    query = f"""
    DELETE FROM `{TABLE_NAME}`
    WHERE UserId = @user_id AND Exercise.name = @exercise_name
    """
    
    # Set up query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("exercise_name", "STRING", exercise_name),
        ]
    )
    
    # Run the query to update the favorite
    try:
        client.query(query, job_config=job_config).result()  # Wait for query to finish
        print(f"Exercise {exercise_name} marked as deleted from favorites.")
    except Exception as e:
        print(f"Error removing favorite: {e}")

def get_user_favorites(user_id):
    """Get all non-deleted favorite exercises for a user from BigQuery."""
    client = bigquery.Client(project=PROJECT_ID)
    
    query = f"""
    SELECT Exercise
    FROM `{TABLE_NAME}`
    WHERE UserId = @user_id
    """
    
    # Set up query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        ]
    )
    
    # Execute the query and fetch the results
    try:
        result = client.query(query, job_config=job_config).result()  # Wait for query to finish
        favorites = [row["Exercise"] for row in result]  # Extract the exercise JSON objects
        return favorites
    except Exception as e:
        print(f"Error fetching favorites: {e}")
        return []

