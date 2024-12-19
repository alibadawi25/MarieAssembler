class MarieRegisters:
    """
    Represents the registers of the Marie machine architecture.

    The Marie machine has a set of registers that hold
    various values during the execution of a program.
    These registers are used for the program's
    operations such as loading data, storing data,
    performing arithmetic operations, and managing program flow.

    Attributes:
        AC (int): The Accumulator register used for
        arithmetic and logic operations.
        IR (int): The Instruction Register which holds the
        current instruction being executed.
        MAR (int): The Memory Address Register used to hold addresses in memory.
        PC (int): The Program Counter register that
        holds the address of the next instruction to be executed.
        MBR (int): The Memory Buffer Register used to
        store data being transferred to or from memory.
        IN (str): The input data register for receiving input.
        OUT (str): The output data register for storing output.
        I_O (bool): A flag indicating if an
        input/output operation is ongoing.
    """

    AC = 0  # Accumulator Register
    IR = 0  # Instruction Register
    MAR = 0  # Memory Address Register
    PC = 0  # Program Counter
    MBR = 0  # Memory Buffer Register
    IN = ""  # Input Register
    OUT = ""  # Output Register
    I_O = False  # Input/Output flag (True if I/O operation is happening)
