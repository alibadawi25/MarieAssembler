# error_handling.py

"""
This module contains the ErrorHandling class, which is responsible for managing
error states and reporting in the Marie assembler simulation.
"""

class ErrorHandling:
    """
    This class manages error states and provides functionality to report errors
    during the assembly process.
    """
    no_error = True

    @staticmethod
    def set_error(state: bool):
        """Set the error state to either True or False."""
        ErrorHandling.no_error = state

    @staticmethod
    def has_error() -> bool:
        """Return whether an error has occurred."""
        return not ErrorHandling.no_error

    @staticmethod
    def report_error(message: str):
        """Report an error message."""
        print(f"Error: {message}")
        ErrorHandling.set_error(False)
