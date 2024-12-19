# output_mode.py

"""
This module defines the OutputMode class, which stores the current output mode
for the program. The output mode can be set to "DEC" or other formats as needed.
"""


class OutputMode:
    """
    A class to represent the output mode for the program.

    Attributes:
        output_mode (str): The current output mode, default is "DEC".
    """

    output_mode = "DEC"

    def __init__(self, mode="DEC"):
        """
        Initializes the OutputMode with the given mode.

        Args:
            mode (str): The output mode to set (default is "DEC").
        """
        self.output_mode = mode

    def get_output_mode(self):
        """
        Returns the current output mode.

        Returns:
            str: The current output mode.
        """
        return self.output_mode

    def set_output_mode(self, mode):
        """
        Sets the output mode to a new value.

        Args:
            mode (str): The output mode to set.
        """
        self.output_mode = mode
