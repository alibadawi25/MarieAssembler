from program_executer import *  # Import execution functions (e.g., jns, load, store, etc.)
from gui import update_text  # Import function to update the GUI textbox


def executeProgram(output_textbox, app):
    """
    Executes the loaded program by simulating the fetch-decode cycle of the Marie
    architecture. It reads the program from memory and processes each instruction.

    Args:
        output_textbox (tkinter Text widget): The textbox in the GUI to update with
                                              execution details.
        app (tkinter Tk instance): The main application instance, used to schedule
                                   the next fetch-decode cycle.
    """
    program_length = 0
    # Calculate the program length by reading memory until a zero entry is found
    for i in range(0,4096):  # Memory size of 4096
        entry = marie_memory.read(i)  # Read memory at index i
        if entry != 0:  # Non-zero entry means part of the program
            program_length += 1
        else:
            break

    # Initialize the registers to zero before starting program execution
    MarieRegisters.PC = marie_memory.starting_pos  # Set Program Counter to starting position
    MarieRegisters.MAR = 0
    MarieRegisters.IR = 0
    MarieRegisters.AC = 0
    MarieRegisters.MBR = 0

    def fetch_decode_cycle():
        """
        Executes one fetch-decode cycle and schedules the next cycle.

        This function simulates the fetch and decode steps of the Marie architecture.
        It updates the output textbox after each cycle and schedules the next cycle.
        """

        
        if MarieRegisters.PC >= 0:
            confirmation = fetch()  # Fetch the instruction based on PC
            if confirmation == -1:
                app.after(1, fetch_decode_cycle)
            decode()  # Decode the instruction
            update_text(output_textbox)  # Update the GUI textbox with current state
            # Schedule the next cycle after 100ms (0.1s)
            app.after(1, fetch_decode_cycle)

    # Start the fetch-decode cycle
    fetch_decode_cycle()

def fetch():
    """
    Fetches the next instruction from memory into the Instruction Register (IR)
    and updates the Program Counter (PC).

    The address to fetch from is determined by
    the value of the Program Counter (PC).
    The MAR (Memory Address Register) is updated with the PC value,
    and the IR (Instruction Register) receives the instruction from memory at
    that address. The PC is then incremented.
    """
    MarieRegisters.MAR = MarieRegisters.PC
    MarieRegisters.IR = marie_memory.read(MarieRegisters.MAR)
    if MarieRegisters.IR == 0:
        print("Program execution completed.")
        MarieRegisters.PC += 1
        return -1
    MarieRegisters.PC += 1

def decode():
    """
    Decodes the current instruction in the Instruction Register (IR).

    The instruction in the IR is split into an opcode and operand.
    The opcode is used to select the appropriate execution function from the
    executionFunctions dictionary. If the function requires an argument
    (such as a memory address), it is passed accordingly.
    """
    # Extract the last 12 bits for the memory address (MAR)
    MarieRegisters.MAR = int(MarieRegisters.IR[-12:], 2)  # Convert the last 12 bits to an integer

    # Extract the first 4 bits for the opcode
    opcode = int(MarieRegisters.IR[:4], 2)  # Convert the first 4 bits to an integer

    # Check if the opcode exists in the executionFunctions dictionary
    if opcode in executionFunctions:
        function = executionFunctions[opcode]  # Get the corresponding function
        # If the function doesn't require arguments or is a special input function
        if (function.__name__ in instructions_without_arguments
                or function.__name__ == "inputInstruction"):
            function()
        else:
            function(MarieRegisters.MAR)
    else:
        print(f"Invalid opcode: {opcode}")

# Dictionary of opcodes and their corresponding execution functions
executionFunctions = {
    0b0000: jns,
    0b0001: load,
    0b0010: store,
    0b0011: add,
    0b0100: subt,
    0b0101: inputInstruction,
    0b0110: output,
    0b0111: halt,
    0b1000: skipcond,
    0b1001: jump,
    0b1010: clear,
    0b1011: addI,
    0b1100: jumpI,
    0b1101: loadI,
    0b1110: storeI
}
