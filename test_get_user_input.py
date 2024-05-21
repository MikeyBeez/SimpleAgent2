import unittest
from unittest.mock import patch
from io import StringIO
from get_user_input import get_user_input
from chat_manager import ChatManager

class TestGetUserInput(unittest.TestCase):
    @patch('builtins.input', return_value="Test input")
    def test_get_user_input_with_name(self, mock_input):
        chat_manager = ChatManager()
        chat_manager.entities.set_user_name("Test User")
        user_input = get_user_input(chat_manager)
        self.assertEqual(user_input, "Test input")

    @patch('builtins.input', return_value="Test input")
    def test_get_user_input_without_name(self, mock_input):
        chat_manager = ChatManager()
        user_input = get_user_input(chat_manager)
        self.assertEqual(user_input, "Test input")

if __name__ == "__main__":
    unittest.main()
