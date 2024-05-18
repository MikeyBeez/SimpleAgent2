import asyncio
import json
from langchain.memory import ConversationSummaryMemory

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

async def main():
    llm = ...  # Your LLM instance
    memory = await load_memory_async(llm) 

    while True:
        user_input = input(":you: ")
        # ... (your logic for prompting the agent and generating a response)

        # Save the memory asynchronously
        asyncio.create_task(save_memory_async(memory)) 

        # ... (handle the response, update the memory, etc.)

if __name__ == "__main__":
    asyncio.run(main())
