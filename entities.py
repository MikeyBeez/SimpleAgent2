class Entities:
    """
    Handles user names and other entities.
    """

    def __init__(self):
        self.user_name = None

    def set_user_name(self, name):
        """
        Sets the user's name.

        Args:
            name (str): The user's name.
        """
        self.user_name = name

    def get_user_name(self):
        """
        Returns the user's name.

        Returns:
            str: The user's name, or None if it hasn't been set.
        """
        return self.user_name
