# memory.py
# This file handles the agent's memory.
# It stores user input and other information for future reference.

class Memory:
    """
    This class represents the agent's memory.
    It stores user input and other important information for future reference. 
    """

    def __init__(self):
        """
        Initializes the memory.
        The memory is represented as a dictionary, where keys are the user inputs
        and values are the corresponding agent responses.
        """
        self.memory = {}

    def add_to_memory(self, user_input, agent_response):
        """
        Adds a new entry to the memory.

        Args:
            user_input (str): The user's input.
            agent_response (str): The agent's response to the user input.

        Returns:
            None
        """
        self.memory[user_input] = agent_response

    def retrieve_from_memory(self, user_input):
        """
        Retrieves the agent's response to a given user input from the memory.

        Args:
            user_input (str): The user's input.

        Returns:
            str: The agent's response to the user input, if it exists in the memory.
            None: If the user input is not found in the memory.
        """
        if user_input in self.memory:
            return self.memory[user_input]
        else:
            return None
