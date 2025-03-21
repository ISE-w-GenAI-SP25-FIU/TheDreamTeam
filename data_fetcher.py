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

# Set Google Cloud credentials (make sure this file exists locally)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# Simulated user profiles
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
    :return: A list of sensor data dictionaries.
    """
    client = bigquery.Client()

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


# The rest remain as-is for now (to be updated in your other steps)

def get_user_workouts(user_id):
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


def get_user_profile(user_id):
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')
    return users[user_id]


def get_user_posts(user_id):
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


def get_genai_advice(user_id):
    advice = random.choice([
        'Your heart rate indicates you can push yourself further. You got this!',
        "You're doing great! Keep up the good work.",
        'You worked hard yesterday, take it easy today.',
        'You have burned 100 calories so far today!',
    ])
    image = random.choice([
        'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop',
        None,
    ])
    return {
        'advice_id': 'advice1',
        'timestamp': '2024-01-01 00:00:00',
        'content': advice,
        'image': image,
    }
