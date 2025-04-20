import unittest
from unittest.mock import patch, MagicMock
from exercises_page import filter_exercises, is_favorite, toggle_favorite

user_id = "user1"

class TestExercisePage(unittest.TestCase):

    def test_filter_exercises(self):
        exercises = [
            {"name": "Push Up", "type": "strength", "muscle": "chest", "difficulty": "beginner"},
            {"name": "Jogging", "type": "cardio", "muscle": "legs", "difficulty": "intermediate"},
            {"name": "Deadlift", "type": "strength", "muscle": "back", "difficulty": "expert"}
        ]

        # Filter by name
        result = filter_exercises(exercises, "push", None, None, [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Push Up")

        # Filter by type
        result = filter_exercises(exercises, "", "strength", None, [])
        self.assertEqual(len(result), 2)

        # Filter by muscle
        result = filter_exercises(exercises, "", None, "chest", [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Push Up")

        # Filter by difficulty
        result = filter_exercises(exercises, "", None, None, ["expert"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Deadlift")

        # Combined filters
        result = filter_exercises(exercises, "dead", "strength", "back", ["expert"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Deadlift")

    @patch('exercises_page.get_user_favorites')
    def test_is_favorite_true(self, mock_get_user_favorites):
        mock_get_user_favorites.return_value = [{"name": "Squat"}, {"name": "Push Up"}]
        self.assertTrue(is_favorite("Push Up"))

    @patch('exercises_page.get_user_favorites')
    def test_is_favorite_false(self, mock_get_user_favorites):
        mock_get_user_favorites.return_value = [{"name": "Squat"}, {"name": "Bench Press"}]
        self.assertFalse(is_favorite("Deadlift"))

    @patch('exercises_page.st.rerun')
    @patch('exercises_page.remove_favorite')
    @patch('exercises_page.add_favorite')
    @patch('exercises_page.get_user_favorites')
    def test_toggle_favorite_adds_new(self, mock_get_user_favorites, mock_add_favorite, mock_remove_favorite, mock_rerun):
        mock_get_user_favorites.return_value = [{"name": "Push Up"}]
        new_ex = {"name": "Squat"}
        toggle_favorite(new_ex)
        mock_add_favorite.assert_called_once_with(user_id, new_ex)
        mock_remove_favorite.assert_not_called()
        mock_rerun.assert_called_once()

    @patch('exercises_page.st.rerun')
    @patch('exercises_page.remove_favorite')
    @patch('exercises_page.add_favorite')
    @patch('exercises_page.get_user_favorites')
    def test_toggle_favorite_removes_existing(self, mock_get_user_favorites, mock_add_favorite, mock_remove_favorite, mock_rerun):
        mock_get_user_favorites.return_value = [{"name": "Push Up"}]
        toggle_favorite({"name": "Push Up"})
        mock_remove_favorite.assert_called_once_with(user_id, "Push Up")
        mock_add_favorite.assert_not_called()
        mock_rerun.assert_called_once()

if __name__ == '__main__':
    unittest.main()
