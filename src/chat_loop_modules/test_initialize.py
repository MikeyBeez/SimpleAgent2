import unittest
from unittest.mock import patch
from io import StringIO  
from initialize import initialize_user
from chat_manager import ChatManager

class InitializeTests(unittest.TestCase):

    @patch('builtins.input', return_value="Test User")
    @patch('sys.stdout', new_callable=StringIO)  
    def test_initialize_user(self, mock_stdout, mock_input):
        chat_manager = ChatManager()
        initialize_user(chat_manager)

        # Check if user_name is set correctly in ChatManager
        self.assertEqual(chat_manager.entities.get_user_name(), "Test User")

        # Check the printed output (optional)
        output = mock_stdout.getvalue().strip()
        self.assertIn("Hello, Test User!", output)
        self.assertIn("How can I help you?", output)

if __name__ == '__main__':
    unittest.main()
