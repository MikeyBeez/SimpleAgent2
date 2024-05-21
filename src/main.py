import asyncio
import warnings
from chat_loop import run_conversation
from initialize import initialize_chatbot

async def main():
    chat_manager = initialize_chatbot() # Initialize chatbot (including user and ChromaDB)
    await run_conversation(chat_manager)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=FutureWarning)
    asyncio.run(main())
