import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import MagicMock, patch
from context_manager import update_context
#from chat_loop_modules.update_and_save_context import update_and_save_context
from chat_manager import ChatManager

class TestUpdateAndSaveContext(unittest.TestCase):
    @patch('chat_manager.ChatManager.memory.save_context') 
    @patch('context_manager.update_context')  
    def test_update_and_save_context(self, mock_update_context, mock_save_context):
        chat_manager = ChatManager()
        update_and_save_context("Test input", "Test response", chat_manager)
        mock_update_context.assert_called_once_with("Test input", "Test response")
        mock_save_context.assert_called_once_with(
            {"input": "Test input"}, {"output": "Test response"}
        )

if __name__ == "__main__":
    unittest.main()
