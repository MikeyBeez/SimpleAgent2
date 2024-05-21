import logging

def get_user_input(chat_manager):
    """Gets user input from the command line."""
    logging.info("Getting user input...")
    user_name = chat_manager.entities.get_user_name()
    if user_name:
        user_input = input(f"{user_name}: ")
    else:
        user_input = input("You: ")
    logging.info(f"User Input: {user_input}")
    return user_input
