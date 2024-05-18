import json
from langchain.memory import ConversationSummaryMemory

MEMORY_FILE = "conversation_memory.json"


def load_memory(llm):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
        memory = ConversationSummaryMemory(llm=llm, **memory_data)
        # Fix: No need to initialize 'chat_history' here 
    except FileNotFoundError:
        memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history")
    return memory


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory.to_json(), f)

def clear_memory():
    """Clears the conversation memory file."""
    try:
        os.remove(MEMORY_FILE)
        print("Conversation memory cleared.")
    except FileNotFoundError:
        print("Memory file not found.")
