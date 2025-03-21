#############################################################################
# activity_page.py
#
# This file contains the activity page functionality for the app.
#
#############################################################################

import streamlit as st
from modules import display_recent_workouts, display_activity_summary
from data_fetcher import get_user_profile, create_user_post
import datetime
import pandas as pd
import json

def show_activity_page(user_id, workout_data):
    """
    Display the activity page for a given user.
    
    Args:
        user_id: The ID of the user whose activity to display
        workout_data: List of workout data for the user
    """
    try:
        user_profile = get_user_profile(user_id)
        user_name = user_profile['full_name']
        st.title(f"{user_name}'s Activity Dashboard")
    except ValueError:
        st.title("Activity Dashboard")
        user_name = "User"
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Recent Workouts", "Activity Summary", "Share"])
    
    with tab1:
        if workout_data:
            # Display only the 3 most recent workouts
            recent_workouts = sorted(
                workout_data,
                key=lambda w: datetime.datetime.strptime(w['start_timestamp'], '%Y-%m-%d %H:%M:%S'),
                reverse=True
            )[:3]
            
            # Use the display_recent_workouts function
            display_recent_workouts(recent_workouts)
        else:
            st.info("No recent workouts found.")
    
    with tab2:
        if workout_data:
            # Use the display_activity_summary function
            display_activity_summary(workout_data)
            
            # Add extra visualization - workout frequency by day of week
            st.subheader("Workout Frequency")

            # Convert timestamps to day of week
            workout_days = []
            for workout in workout_data:
                timestamp = datetime.datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
                day_of_week = timestamp.strftime('%A')  # Full day name
                workout_days.append(day_of_week)

            # Count workouts by day
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = {day: workout_days.count(day) for day in day_order}

            # Create DataFrame and display as bar chart
            chart_data = pd.DataFrame({
                'Day': list(day_counts.keys()),
                'Workouts': list(day_counts.values())
            })

            # Use Altair for better control over axis labels
            import altair as alt

            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X('Day:N', sort=day_order, axis=alt.Axis(labelAngle=0)),  # labelAngle=0 keeps labels horizontal
                y=alt.Y('Workouts:Q')
            ).properties(
                height=300
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No activity data available to summarize.")

    with tab3:
        st.subheader("Share Your Activity")
        
        # Create a summary for sharing
        if workout_data:
            total_workouts = len(workout_data)
            total_distance = sum(w['distance'] for w in workout_data)
            total_steps = sum(w['steps'] for w in workout_data)
            total_calories = sum(w['calories_burned'] for w in workout_data)
            
            share_text = f"""
            🏃‍♂️ My Fitness Journey 🏃‍♀️
            
            I've completed {total_workouts} workouts!
            📊 Stats:
            • {total_distance:.1f} km distance
            • {total_steps:,} steps
            • {total_calories} calories burned
            
            #FitnessGoals #StayActive
            """
            
            st.text_area("Share this summary on social media:", share_text, height=200)
            
            # Share to community button
            st.subheader("Share with Community")
            
            # Create share options
            stat_to_share = st.selectbox(
                "What would you like to share?",
                ["Steps", "Distance", "Calories Burned", "Workout Count"]
            )
            
            custom_message = st.text_input(
                "Add a custom message (optional):",
                placeholder="I'm crushing my fitness goals!"
            )
            
            # Generate share content based on selection
            if stat_to_share == "Steps":
                stat_value = f"{total_steps:,} steps"
                default_message = f"Look at this, I walked {stat_value} so far!"
            elif stat_to_share == "Distance":
                stat_value = f"{total_distance:.1f} km"
                default_message = f"I've traveled {stat_value} in my workouts!"
            elif stat_to_share == "Calories Burned":
                stat_value = f"{total_calories} calories"
                default_message = f"I've burned {stat_value} through exercise!"
            else:  # Workout Count
                stat_value = f"{total_workouts} workouts"
                default_message = f"I've completed {stat_value} in my fitness journey!"
            
            # Use custom message if provided, otherwise use default
            share_message = custom_message if custom_message else default_message
            
            # Preview the post
            st.markdown("**Post Preview:**")
            st.markdown(f"_{share_message}_")
            
            # Share button
            if st.button("📣 Share to Community"):
                try:
                    # Call function to create a post (we'll implement this next)
                    create_user_post(user_id, share_message)
                    st.success("Successfully shared to community! Your friends can now see your progress.")
                except Exception as e:
                    st.error(f"Error sharing post: {str(e)}")
            
            # Social media share buttons
            st.markdown("---")
            st.markdown("**Share on Social Media:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📱 Share to Twitter"):
                    st.success("Twitter share link generated!")
                    # In a real implementation, this would generate a Twitter share link
            
            with col2:
                if st.button("📘 Share to Facebook"):
                    st.success("Facebook share link generated!")
                    # In a real implementation, this would generate a Facebook share link
            
            with col3:
                if st.button("📸 Share to Instagram"):
                    st.success("Instagram share link generated!")
                    # In a real implementation, this would generate an Instagram share link
            
            # Download option
            workout_data_summary = {
                "user": user_name,
                "total_workouts": total_workouts,
                "total_distance": float(total_distance),
                "total_steps": total_steps,
                "total_calories": total_calories,
                "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            json_data = json.dumps(workout_data_summary, indent=2)
            st.download_button(
                label="📊 Download Activity Summary",
                data=json_data,
                file_name=f"{user_name.lower().replace(' ', '_')}_activity_summary.json",
                mime="application/json"
            )
        else:
            st.info("Complete some workouts to share your progress!")

# This code was replaced by using the create_user_post function from data_fetcher directly

# For testing as a standalone page
if __name__ == "__main__":
    import random
    from data_fetcher import get_user_workouts, users
    
    test_user_id = random.choice(list(users.keys()))
    test_workout_data = get_user_workouts(test_user_id)
    show_activity_page(test_user_id, test_workout_data)