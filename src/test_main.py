import unittest
from unittest.mock import patch
from io import StringIO
from initialize import initialize_chatbot, initialize_user
from chat_manager import ChatManager
import config  # Import your config.py 

class InitializeTests(unittest.TestCase):

    # ... (Your existing test_initialize_user function) ...

    @patch('builtins.input', return_value="Test User") # For initialize_user call
    @patch('sys.stdout', new_callable=StringIO)
    def test_initialize_chatbot(self, mock_stdout, mock_input):
        chat_manager = ChatManager()
        initialize_chatbot(chat_manager)

        # Assertions for variables loaded from config.py
        self.assertEqual(chat_manager.zip_code, config.zip_code)
        self.assertEqual(chat_manager.latitude, config.latitude)
        self.assertEqual(chat_manager.longitude, config.longitude)
        self.assertEqual(chat_manager.noaa_weather_token, config.noaa_weather_token)
        self.assertEqual(chat_manager.embedding_model_name, config.embedding_model_name)

        # Check printed output (welcome message and "Ready to chat!")
        output = mock_stdout.getvalue().strip()
        self.assertIn(config.WELCOME_MESSAGE.strip(), output)
        self.assertIn("Chatbot initialized. Ready to chat!", output)

if __name__ == '__main__':
    unittest.main()
