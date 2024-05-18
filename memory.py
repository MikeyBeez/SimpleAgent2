import asyncio
import json
from langchain.memory import ConversationSummaryMemory
import os # Import os to use os.remove()

MEMORY_FILE = "conversation_memory.json"

async def save_memory_async(memory):
    """Saves the conversation memory to a JSON file asynchronously."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory.to_json(), f)

async def load_memory_async(llm):
    """Loads the conversation memory from a JSON file asynchronously."""
    try:
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
        memory = ConversationSummaryMemory(llm=llm, **memory_data)
    except FileNotFoundError:
        memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history")
    return memory

async def clear_memory_async():
    """Clears the conversation memory file asynchronously."""
    try:
        os.remove(MEMORY_FILE)
        print("Conversation memory cleared.")
    except FileNotFoundError:
        print("Memory file not found.")

async def main():
    llm = ...  # Your LLM instance
    memory = await load_memory_async(llm) 

    while True:
        user_input = input(":you: ")
        if user_input.lower() == "clear memory":
            # Call the clear_memory_async function asynchronously
            await clear_memory_async()
            memory = await load_memory_async(llm)
            continue

        # ... (your logic for prompting the agent and generating a response)

        # Save the memory asynchronously
        asyncio.create_task(save_memory_async(memory)) 

        # ... (handle the response, update the memory, etc.)

if __name__ == "__main__":
    asyncio.run(main())
