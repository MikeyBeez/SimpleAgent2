class Router:
    """
    Determines if a search is needed for a given question.
    """

    def __init__(self, llm):
        self.llm = llm
        self.should_search_prompt = SHOULD_SEARCH_PROMPT

    def should_search(self, question, chat_history):
        """
        Determines if a search is needed for the given question.

        Args:
            question (str): The user's question.
            chat_history (str): The conversation history.

        Returns:
            bool: True if a search is needed, False otherwise.
        """
        response = self.llm.invoke(
            self.should_search_prompt.format(question=question, chat_history=chat_history)
        ).strip()
        return response.lower() == "yes" 
