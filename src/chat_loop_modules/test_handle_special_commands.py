import unittest
from unittest.mock import patch
from handle_special_commands import handle_special_commands
#from chat_manager import ChatManager
import chat_manager

class TestHandleSpecialCommands(unittest.TestCase):
    @patch('handle_special_commands.exit')  
    @patch('chat_manager.ChatManager.memory.vectorstore.delete_collection')
    def test_handle_clear_memory(self, mock_delete_collection, mock_exit):
        chat_manager = ChatManager()
        result = handle_special_commands("clear memory", chat_manager)
        self.assertTrue(result)  
        mock_delete_collection.assert_called_once() 

    @patch('handle_special_commands.exit')
    def test_handle_exit_commands(self, mock_exit):
        chat_manager = ChatManager()
        for command in ["quit", "exit", "bye"]:
            result = handle_special_commands(command, chat_manager)
            self.assertTrue(result)
            mock_exit.assert_called_once()  
            mock_exit.reset_mock()  

    def test_handle_other_commands(self):
        chat_manager = ChatManager()
        result = handle_special_commands("What is the weather?", chat_manager)
        self.assertFalse(result)  

if __name__ == "__main__":
    unittest.main()
