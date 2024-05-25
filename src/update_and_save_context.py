import logging
from chat_loop_modules.context_manager import update_context

def update_and_save_context(user_input, response, chat_manager):
    """Updates the context and saves it to ChromaDB."""
    logging.info("Updating context...")
    update_context(user_input, response)
    logging.info("Context updated.")

    logging.info("Saving context to memory...")
    chat_manager.memory.save_context({"input": user_input}, {"output": response})
    logging.info("Context saved.") 
