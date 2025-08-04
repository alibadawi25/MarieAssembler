class MarieMemory:
    starting_pos = 0 
    """
    A class representing the memory of the Marie architecture.

    This class simulates a memory array with a specified size (default: 4096)
    and provides methods to read from, write to, and clear the memory. It supports
    two types of write modes: direct assignment (mode 0) and addition to the current value (mode 1).
    """
    def __init__(self, size=4096):
        """
        Initializes the memory with the given size, defaulting to 4096 locations.

        Args:
            size (int): The size of the memory array. Defaults to 4096.
        """
        self.memory = [0] * size

    def read(self, address):
        """
        Reads the value from the specified memory address.

        Args:
            address (int): The address to read from.

        Returns:
            int: The value stored at the given memory address.

        Raises:
            IndexError: If the address is out of range.
        """
        if 0 <= address < len(self.memory):
            return self.memory[address]
        else:
            raise IndexError("Address out of range")

    def write(self, address, value, mode):
        """
        Writes a value to the specified memory address.

        The method supports two modes of writing:
        - Mode 0: Direct assignment (writes the value directly).
        - Mode 1: Addition (adds the value to the current value at the address).

        Args:
            address (int): The address to write to.
            value (int): The value to write or add to the memory.
            mode (int): The write mode. 0 for direct assignment, 1 for addition.

        Raises:
            IndexError: If the address is out of range.
        """
        if 0 <= address < len(self.memory):
            if mode == 0:
                self.memory[address] = value
            elif mode == 1:
                self.memory[address] += value
            else:
                raise ValueError("Invalid mode. Mode must be 0 or 1.")
        else:
            raise IndexError("Address out of range")

    def clear(self):
        """
        Clears the memory by resetting all locations to 0.
        """
        self.memory = [0] * len(self.memory)

    def __str__(self):
        """
        Returns a string representation of the memory contents.

        Returns:
            str: The memory array as a string.
        """
        return str(self.memory)
