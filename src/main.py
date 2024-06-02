import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import asyncio
import warnings
from chat_loop_modules.chat_loop import run_conversation
from chat_loop_modules.initialize import initialize_chatbot

async def main():
    """Initializes and runs the chatbot."""
    chat_manager = initialize_chatbot()
    await run_conversation(chat_manager)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=FutureWarning)
    asyncio.run(main())
