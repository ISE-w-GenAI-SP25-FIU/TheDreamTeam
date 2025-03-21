from data_fetcher import get_user_sensor_data

# Example test values
user_id = "12345"
workout_id = "67890"

sensor_data = get_user_sensor_data(user_id, workout_id)
print(sensor_data)
