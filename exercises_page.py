import streamlit as st
import requests
import os
from data_fetcher import get_user_favorites, add_favorite, remove_favorite

user_id = "user1"

API_KEY = os.getenv("API_KEY")
API_URL = "https://api.api-ninjas.com/v1/exercises"

st.title("🏋️ Exercise Explorer")

# Convert filter labels to API value and vice versa
def format_label(s): return s.replace("_", " ").title()
def unformat_label(s): return s.lower().replace(" ", "_")

type_options_raw = [
    "cardio", "olympic_weightlifting", "plyometrics",
    "powerlifting", "strength", "stretching", "strongman"
]
muscle_options_raw = [
    "abdominals", "abductors", "adductors", "biceps", "calves", "chest", 
    "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", 
    "neck", "quadriceps", "traps", "triceps"
]
difficulty_options_raw = ["beginner", "intermediate", "expert"]

# Display-friendly labels
type_options = [format_label(t) for t in type_options_raw]
muscle_options = [format_label(m) for m in muscle_options_raw]
difficulty_options = [format_label(d) for d in difficulty_options_raw]

with st.sidebar:
    st.header("🔎 Filter Exercises")
    search_query = st.text_input("Exercise Name", placeholder="e.g. press")

    selected_type_label = st.selectbox("Type", ["All"] + type_options)
    selected_muscle_label = st.selectbox("Muscle", ["All"] + muscle_options)
    selected_difficulty_labels = st.multiselect(
        "Difficulty", difficulty_options, default=[]
    )

# Convert labels back to raw values for API query
selected_type = unformat_label(selected_type_label) if selected_type_label != "All" else None
selected_muscle = unformat_label(selected_muscle_label) if selected_muscle_label != "All" else None
selected_difficulties = [unformat_label(d) for d in selected_difficulty_labels]

@st.cache_data(show_spinner=True)
def fetch_exercises(name=None, type_=None, muscle=None, difficulty=None):
    params = {}
    if name:
        params["name"] = name
    if type_:
        params["type"] = type_
    if muscle:
        params["muscle"] = muscle
    if difficulty:
        results = []
        for d in difficulty:
            params["difficulty"] = d
            response = requests.get(API_URL, headers={"X-Api-Key": API_KEY}, params=params)
            if response.status_code == 200:
                results.extend(response.json())
        return results
    else:
        response = requests.get(API_URL, headers={"X-Api-Key": API_KEY}, params=params)
        if response.status_code == 200:
            return response.json()
    return []

def toggle_favorite(exercise):
    """Toggle favorite status for a given exercise."""
    favorites = get_user_favorites(user_id)
    # Check if the exercise is already a favorite by name
    if any(fav["name"] == exercise["name"] for fav in favorites):
        remove_favorite(user_id, exercise["name"])
    else:
        add_favorite(user_id, exercise)
    st.rerun()  # Refresh the page to update favorites

def is_favorite(exercise_name):
    """Check if a given exercise is a favorite."""
    favorites = get_user_favorites(user_id)
    return any(fav["name"] == exercise_name for fav in favorites)

def filter_exercises(exercises, name_query, type_filter, muscle_filter, difficulty_filters):
    filtered = exercises
    if name_query:
        filtered = [ex for ex in filtered if name_query.lower() in ex["name"].lower()]
    if type_filter:
        filtered = [ex for ex in filtered if type_filter.lower() == ex["type"].lower()]
    if muscle_filter:
        filtered = [ex for ex in filtered if muscle_filter.lower() == ex["muscle"].lower()]
    if difficulty_filters:
        filtered = [ex for ex in filtered if ex["difficulty"].lower() in difficulty_filters]
    return filtered

def render_exercise_card(ex, index):
    cols = st.columns([0.9, 0.1])
    with cols[0]:
        st.subheader(ex["name"])
        st.markdown(f"**Type:** {format_label(ex['type'])} | **Muscle:** {format_label(ex['muscle'])}")
        st.markdown(f"**Equipment:** {format_label(ex['equipment'])} | **Difficulty:** {format_label(ex['difficulty'])}")
        with st.expander("📋 Instructions"):
            st.write(ex["instructions"])
    with cols[1]:
        is_fav = is_favorite(ex["name"])
        # Use a unique key for the button by including the index
        if st.button("⭐" if is_fav else "☆", key=f"{ex['name']}_{index}"):
            toggle_favorite(ex)
    st.markdown("---")

selected_tab = st.sidebar.radio("Choose a Tab", ["Search", "Favorites"])

if selected_tab == "Search":
    results = fetch_exercises(
        name=search_query,
        type_=selected_type,
        muscle=selected_muscle,
        difficulty=selected_difficulties
    )

    st.markdown(f"### Found {len(results)} exercise(s)")
    for index, ex in enumerate(results):
        render_exercise_card(ex, index)

elif selected_tab == "Favorites":
    favorites = get_user_favorites(user_id)
    filtered_favorites = filter_exercises(
        favorites,
        search_query,
        selected_type,
        selected_muscle,
        selected_difficulties
    )

    st.markdown(f"### Found {len(filtered_favorites)} favorite(s)")

    if filtered_favorites:
        for index, ex in enumerate(filtered_favorites):
            render_exercise_card(ex, index)
    else:
        if len(favorites) > 0:
            st.info("No favorites match the filters yet. Try adjusting your filters!")