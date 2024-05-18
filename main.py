import asyncio
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)  # Suppress the warnings

from chat_manager import ChatManager  # Import the ChatManager

async def main():
    chat_manager = ChatManager()
    await chat_manager.run_conversation()

if __name__ == "__main__":
    asyncio.run(main())
