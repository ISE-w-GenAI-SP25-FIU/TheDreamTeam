#############################################################################
# leaderboard_utils.py
#
# This file contains utility functions to calculate points and rankings for 
# the leaderboard functionality.
#############################################################################

from data_fetcher import get_user_workouts, get_user_profile, users
import datetime
from google.cloud import bigquery

PROJECT_ID = "dreamteamproject-449421"

def calculate_user_points(user_id, time_period="day"):
    """
    Calculate total points for a user based on their workouts.
    
    Args:
        user_id: The user's ID
        time_period: "day", "week", "month", or "year"
        
    Returns:
        Integer representing total points
    """
    # Get user's workouts
    workouts = get_user_workouts(user_id)
    
    if not workouts:
        return 0
    
    # Calculate date range for filtering
    now = datetime.datetime.now()
    
    if time_period == "day":
        start_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    elif time_period == "week":
        # Calculate start of week (Monday)
        start_date = now - datetime.timedelta(days=now.weekday())
        start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    elif time_period == "month":
        start_date = datetime.datetime(now.year, now.month, 1, 0, 0, 0)
    elif time_period == "year":
        start_date = datetime.datetime(now.year, 1, 1, 0, 0, 0)
    else:
        # Default to all time
        start_date = datetime.datetime(1970, 1, 1, 0, 0, 0)
    
    # Filter workouts by time period
    filtered_workouts = []
    for workout in workouts:
        try:
            workout_time = datetime.datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
            if workout_time >= start_date:
                filtered_workouts.append(workout)
        except:
            # Skip workouts with invalid timestamps
            continue
    
    # Calculate points based on the formula:
    # 1 calorie = 1 point
    # 1 mile = 5 points
    total_points = 0
    
    for workout in filtered_workouts:
        # Points from calories
        calories_points = workout.get('calories_burned', 0)
        
        # Points from distance (convert km to miles)
        distance_km = workout.get('distance', 0)
        distance_miles = distance_km * 0.621371  # Convert km to miles
        distance_points = int(distance_miles * 5)
        
        # Sum points for this workout (no bonus points)
        workout_points = calories_points + distance_points
        total_points += workout_points
    
    return total_points

def get_user_rankings(time_period="day"):
    """
    Generate rankings of all users based on points.
    
    Args:
        time_period: "day", "week", "month", or "year"
        
    Returns:
        List of dictionaries with user rankings, sorted by points
    """
    
    client = bigquery.Client(project=PROJECT_ID)

    # Define the SQL query based on the time_period
    query = f"""
    SELECT rank, user_id, name, points, profile_image
    FROM dreamteamproject-449421.DreamDataset.Leaderboard
    WHERE time_period = @time_period
    ORDER BY points DESC
    """
    # Run the query
    query_params = [bigquery.ScalarQueryParameter("time_period", "STRING", time_period)]
    query_job = client.query(query, job_config=bigquery.QueryJobConfig(query_parameters=query_params))

    # Get the query results
    results = query_job.result()

    # Format the results into a list of dictionaries
    rankings = [
        {"rank": row.rank, "user_id": row.user_id, "name": row.name, "points": row.points, "profile_image": row.profile_image}
        for row in results
    ]
    
    return rankings

def get_user_activity_metrics(user_id, time_period="day"):
    """
    Get workout metrics and points for a user.
    
    Args:
        user_id: The user's ID
        time_period: "day", "week", "month", or "year"
        
    Returns:
        List of workout metrics with points, sorted by timestamp
    """
    # Create mock data with realistic values for different time periods
    if time_period == "day":
        return [
            {"workout": 2, "kcals": 90, "miles": 1.8, "points": 188},
            {"workout": 1, "kcals": 28, "miles": 0.7, "points": 102}
        ]
    elif time_period == "week":
        return [
            {"workout": 5, "kcals": 320, "miles": 6.2, "points": 651},
            {"workout": 4, "kcals": 180, "miles": 3.5, "points": 355},
            {"workout": 3, "kcals": 250, "miles": 4.8, "points": 490},
            {"workout": 2, "kcals": 90, "miles": 1.8, "points": 188},
            {"workout": 1, "kcals": 28, "miles": 0.7, "points": 102}
        ]
    elif time_period == "month":
        return [
            {"workout": 15, "kcals": 420, "miles": 8.1, "points": 865},
            {"workout": 14, "kcals": 380, "miles": 7.4, "points": 797},
            {"workout": 13, "kcals": 310, "miles": 6.0, "points": 640},
            {"workout": 12, "kcals": 275, "miles": 5.3, "points": 550},
            {"workout": 11, "kcals": 190, "miles": 3.7, "points": 395}
        ]
    else:  # year
        return [
            {"workout": 52, "kcals": 510, "miles": 10.2, "points": 1060},
            {"workout": 51, "kcals": 480, "miles": 9.5, "points": 1027},
            {"workout": 50, "kcals": 425, "miles": 8.3, "points": 866},
            {"workout": 49, "kcals": 390, "miles": 7.6, "points": 828},
            {"workout": 48, "kcals": 350, "miles": 6.8, "points": 740}
        ]

def get_user_stats(user_id, time_period="day"):
    """
    Get user stats for the leaderboard summary.
    
    Args:
        user_id: The user's ID
        time_period: "day", "week", "month", or "year"
        
    Returns:
        Dictionary with stats
    """
    if time_period == "day":
        return {
            "total_points": 301,
            "global_rank": 42,
            "friend_rank": 1,
            "badges": 5
        }
    elif time_period == "week":
        return {
            "total_points": 987,
            "global_rank": 12,
            "friend_rank": 2,
            "badges": 5
        }
    elif time_period == "month":
        return {
            "total_points": 3219,
            "global_rank": 4,
            "friend_rank": 1,
            "badges": 5
        }
    else:  # year
        return {
            "total_points": 17755,
            "global_rank": 5,
            "friend_rank": 3,
            "badges": 5
        }