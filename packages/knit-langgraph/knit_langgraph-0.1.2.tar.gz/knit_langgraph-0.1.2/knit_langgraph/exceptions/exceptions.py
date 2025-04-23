"""
This module defines custom exception classes for the Knit OpenAI client.
"""

class KnitException(Exception):
    """
    A base exception class for all Knit-related errors.

    This class extends the built-in Exception class and serves as
    the base class for other custom exceptions in the Knit module.
    """
    def __init__(self, message, *args):
        """
        Initialize a KnitException with a message and optional arguments.
        Args:
            message (str): A descriptive error message.
            *args: Additional positional arguments.

        The message is stored as an instance attribute and the base
        Exception class is initialized with the provided arguments.
        """
        super().__init__(message, *args)
        self.message = message


class InvalidKnitAPIKey(KnitException):
    """
    Exception raised for errors related to invalid Knit API keys.

    This exception is derived from KnitException and is raised when
    an API key is determined to be invalid or incorrect.
    """

    def __init__(self, message, *args):
        """
        Initialize an InvalidKnitAPIKey exception with a message and optional arguments.

        Args:
            message (str): A descriptive error message about the invalid API key.
            *args: Additional positional arguments.

        This constructor calls the base KnitException initializer to ensure
        proper exception setup and stores the message as an instance attribute.
        """
        super().__init__(message, *args)
        self.message = message
