import logging

def handle_special_commands(user_input, chat_manager):
    """Handles special commands like 'clear memory' and exit commands."""
    logging.info("Handling special commands...")
    if user_input.lower() == "clear memory":
        logging.info("Clearing memory...")
        chat_manager.memory.vectorstore.delete_collection()
        print("Conversation memory cleared.")
        logging.info("Memory cleared.")
        return True

    if user_input.lower() in ["quit", "exit", "bye"]:
        logging.info("Exiting conversation loop...")
        exit()  # Exit the program
        return True

    return False
