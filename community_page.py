import streamlit as st
from home_page import userId
from modules import display_genai_advice, display_post
from data_fetcher import get_genai_advice, get_user_profile, get_user_posts, users
import random

userId = random.choice(list(users.keys()))

st.title('Community')
col1, col2 = st.columns(2, gap="small")

with col1:
    advice_data = get_genai_advice(userId)
    display_genai_advice(advice_data['timestamp'], advice_data['content'], advice_data['image'])

with col2:
    user_profile = get_user_profile(userId)
    friends_ids = user_profile['friends']

    all_posts = []
    friend_profiles = {}

    for friend_id in friends_ids:
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

    sorted_posts = sorted(all_posts, key=lambda post: post['timestamp'], reverse=True)
    top_10_posts = sorted_posts[:10]

    for post in top_10_posts:
        display_post(
            post['full_name'], 
            post['user_image'], 
            post['timestamp'], 
            post['content'], 
            post['image']
        )



