import asyncio
import json
from langchain.memory import ConversationBufferMemory
import os
from entities import Entities 

MEMORY_FILE = "conversation_memory.json"

async def save_memory(memory):
    """Saves the conversation memory to a JSON file asynchronously."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory.to_json(), f)

async def clear_memory():
    """Clears the conversation memory file asynchronously."""
    try:
        os.remove(MEMORY_FILE)
        print("Conversation memory cleared.")
    except FileNotFoundError:
        print("Memory file not found.")

def load_memory(llm):
    """
    Loads the conversation memory from a JSON file (blocking).

    Args:
        llm: The language model instance used by the memory.

    Returns:
        ConversationBufferMemory: The loaded conversation memory object.
    """
    try:
        # Attempt to load memory from the JSON file
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
        # Create a ConversationBufferMemory object using the loaded data and the LLM
        memory = ConversationBufferMemory(llm=llm, **memory_data)
    except FileNotFoundError:
        # If the memory file doesn't exist, create a new ConversationBufferMemory object
        memory = ConversationBufferMemory(llm=llm, memory_key="chat_history")
    return memory

async def update_memory_async(memory, question, response, entities):
    """Updates the memory asynchronously."""
    memory.save_context({"input": question}, {"output": response})
    await save_memory(memory)
    entities.set_user_name(question.split(" ")[0]) # Assuming the first word is the name
