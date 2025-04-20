import streamlit as st
from modules import display_genai_advice, display_post
from data_fetcher import get_genai_advice, get_user_profile, get_user_posts, users, get_user_workouts
from leaderboard_utils import get_user_rankings, get_user_activity_metrics, get_user_stats
import random
import pandas as pd

# Get the user ID only once
if 'userId' not in globals():
    userId = random.choice(list(users.keys()))
else:
    from home_page import userId

# Initialize session state without triggering reruns
if "initialized" not in st.session_state:
    st.session_state.view_mode = "leaderboard"  # Default: show user rankings
    st.session_state.time_period = "Week"  # Default: weekly view
    st.session_state.initialized = True

# Function to toggle view with immediate rerun
def toggle_view():
    st.session_state.view_mode = "activity" if st.session_state.view_mode == "leaderboard" else "leaderboard"
    st.rerun()  # Force a rerun to update the UI immediately

# Function to set time period without triggering rerun
def set_time_period(period):
    st.session_state.time_period = period

# Main function to display the leaderboard
def display_leaderboard():
    """
    Displays the leaderboard component using Streamlit native components.
    """
    # Get user profile - only get this once
    try:
        user_profile = get_user_profile(userId)
        user_name = user_profile['full_name']
        profile_img = user_profile.get('profile_image', '')
    except:
        user_name = "Bob Smith"  # Default name
        profile_img = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
    
    # Create a purple container
    st.markdown(
        """
        <style>
        .purple-container {
            background-color: #5B21B6;
            border-radius: 10px;
            padding: 20px;
            color: white;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create a container with purple background
    with st.container():
        st.markdown('<div class="purple-container">', unsafe_allow_html=True)
        
        # Display profile info
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(profile_img, width=60)
        with col2:
            st.markdown(f"<h3 style='color:white; margin:0;'>{user_name}</h3>", unsafe_allow_html=True)
            
            # Change button text based on current view
            button_text = "View Points Summary" if st.session_state.view_mode == "leaderboard" else "View Leaderboard"
            if st.button(button_text):
                toggle_view()
        
        # Tabs for time periods
        time_periods = ["Day", "Week", "Month", "Year"]
        
        # Create tabs and find currently selected tab
        tab_index = time_periods.index(st.session_state.time_period)
        selected_tab = st.tabs(time_periods)[tab_index]
        
        # Update time period based on which tab is selected
        for i, tab_name in enumerate(time_periods):
            if i == tab_index:
                with selected_tab:
                    set_time_period(tab_name)
        
        # Get current time period in lowercase for function arguments
        current_period = st.session_state.time_period.lower()
        
        # Content for the current view and time period
        if st.session_state.view_mode == "leaderboard":
            # User rankings view
            st.markdown("<h4 style='color:white;'>User Rankings</h4>", unsafe_allow_html=True)
            
            # Get rankings data for current time period
            rankings = get_user_rankings(current_period)
            
            # Format the data for display
            users_data = [
                {"Rank": user["rank"], "User": user["name"], "Points": user["points"]}
                for user in rankings
            ]
            
            # Create and display the dataframe
            df = pd.DataFrame(users_data)
            st.dataframe(
                df,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn(format="%d"),
                    "User": st.column_config.TextColumn(),
                    "Points": st.column_config.NumberColumn(format="%d")
                },
                use_container_width=True
            )
            
        else:
            # Activity metrics view
            st.markdown("<h4 style='color:white;'>Activity Metrics</h4>", unsafe_allow_html=True)
            
            # Get activity data for current time period
            metrics = get_user_activity_metrics(userId, current_period)
            
            # Format the data for display
            activity_data = [
                {"Workout": m["workout"], "kCals": m["kcals"], "Miles": m["miles"], "Points": m["points"]}
                for m in metrics
            ]
            
            # Create and display the dataframe
            df = pd.DataFrame(activity_data)
            st.dataframe(
                df,
                hide_index=True,
                column_config={
                    "Workout": st.column_config.NumberColumn(format="%d"),
                    "kCals": st.column_config.NumberColumn(format="%d"),
                    "Miles": st.column_config.NumberColumn(format="%.1f"),
                    "Points": st.column_config.NumberColumn(format="%d")
                },
                use_container_width=True
            )
        
        # Help icon with tooltip
        st.markdown(
            """
            <style>
            .tooltip {
                position: relative;
                display: inline-block;
                float: right;
            }
            
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                text-align: left;
                border-radius: 6px;
                padding: 10px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            </style>
            
            <div class='tooltip'>
                <span style='background-color:rgba(255,255,255,0.2); border-radius:50%; width:25px; height:25px; display:inline-block; text-align:center; line-height:25px; color:white;'>?</span>
                <div class='tooltiptext'>
                    <strong>Points Calculation:</strong><br>
                    • 1 calorie burned = 1 point<br>
                    • 1 mile traveled = 5 points<br>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Close the purple container
        st.markdown('</div>', unsafe_allow_html=True)

# Function to display badges
def display_badges():
    """Displays the badges section."""
    st.markdown("<h4>Badges</h4>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div style='background-color:#f0f2f6; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;'>
        🔥
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background-color:#f0f2f6; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;'>
        🏃
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background-color:#f0f2f6; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;'>
        30
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style='background-color:#f0f2f6; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;'>
        🎯
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div style='background-color:#f0f2f6; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;'>
        🏆
        </div>
        """, unsafe_allow_html=True)

# Main community page
st.title('Community')

# Create tabs for different views
leaderboard_tab, feed_tab = st.tabs(["Leaderboard", "Social Feed"])

with leaderboard_tab:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Display the leaderboard
        display_leaderboard()
        
        # Display badges
        display_badges()
    
    with col2:
        # User stats
        st.subheader("Your Stats")
        
        # Get stats based on current time period
        stats = get_user_stats(userId, st.session_state.time_period.lower())
        
        # Create metrics
        col1, col2 = st.columns(2)
        col1.metric("Total Points", str(stats["total_points"]))
        col2.metric("Global Rank", f"#{stats['global_rank']}")
        
        col1, col2 = st.columns(2)
        col1.metric("Friends Rank", f"#{stats['friend_rank']}")
        col2.metric("Badges Earned", str(stats["badges"]))
        
        # Motivational image
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Jumping-1461189_960_720.jpg/640px-Jumping-1461189_960_720.jpg", 
                caption="Stay motivated!")

with feed_tab:
    # Display the existing social feed content
    col1, col2 = st.columns(2, gap="small")

    with col1:
        try:
            advice_data = get_genai_advice(userId)
            display_genai_advice(advice_data['timestamp'], advice_data['content'], advice_data['image'])
        except:
            st.info("GenAI advice not available.")

    with col2:
        try:
            user_profile = get_user_profile(userId)
            friends_ids = user_profile.get('friends', [])

            all_posts = []
            friend_profiles = {}

            for friend_id in friends_ids:
                try:
                    friend_profile = get_user_profile(friend_id)
                    friend_profiles[friend_id] = {
                        'full_name': friend_profile['full_name'],
                        'profile_image': friend_profile['profile_image']
                    }
                    
                    friend_posts = get_user_posts(friend_id)
                    
                    for post in friend_posts:
                        post['full_name'] = friend_profiles[friend_id]['full_name']
                        post['user_image'] = friend_profiles[friend_id]['profile_image']
                        all_posts.append(post)
                except:
                    continue

            sorted_posts = sorted(all_posts, key=lambda post: post['timestamp'], reverse=True)
            top_10_posts = sorted_posts[:10]

            if top_10_posts:
                for post in top_10_posts:
                    display_post(
                        post['full_name'], 
                        post['user_image'], 
                        post['timestamp'], 
                        post['content'], 
                        post['image']
                    )
            else:
                st.info("No posts available from your friends.")
        except Exception as e:
            st.error(f"Error loading social feed: {str(e)}")
            st.info("No friend posts available.")