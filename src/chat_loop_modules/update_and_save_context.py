import logging
from .context_manager import update_context

def update_and_save_context(user_input, response, chat_manager):
    """Updates the context with user input and response then saves it to ChromaDB."""

    # Updating the context by passing both 'input' and 'output' as a dictionary.
    update_context({"input": user_input, "output": response})

    logging.info("Context updated with input: %s and output: %s", user_input, response)

    # Saving the context to ChromaDB by passing both 'input' and 'output'.
    chat_manager.memory.save_context({"input": user_input, "output": response})

    logging.info("Context saved successfully.")
