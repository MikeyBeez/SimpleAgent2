import json
from langchain.memory import ConversationSummaryMemory

# Define the file name for storing conversation memory
MEMORY_FILE = "conversation_memory.json"


def load_memory(llm):
    """
    Loads the conversation memory from a JSON file.

    Args:
        llm: The language model instance used by the memory.

    Returns:
        ConversationSummaryMemory: The loaded conversation memory object.
    """
    try:
        # Attempt to load memory from the JSON file
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
        # Create a ConversationSummaryMemory object using the loaded data and the LLM
        memory = ConversationSummaryMemory(llm=llm, **memory_data)
        # Fix: No need to initialize 'chat_history' here
    except FileNotFoundError:
        # If the memory file doesn't exist, create a new ConversationSummaryMemory object
        memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history")
    return memory


def save_memory(memory):
    """
    Saves the conversation memory to a JSON file.

    Args:
        memory: The conversation memory object.
    """
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory.to_json(), f)

def clear_memory():
    """Clears the conversation memory file."""
    try:
        os.remove(MEMORY_FILE)
        print("Conversation memory cleared.")
    except FileNotFoundError:
        print("Memory file not found.")
