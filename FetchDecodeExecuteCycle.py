from MarieMemory import MarieMemory  # Import the memory class
from MarieRegister import *  # Import registers (PC, MAR, IR, etc.)
from AssemblyToMachineCodeTranslator import *
from ProgramExecuter import *
import time

from gui import update_text

from gui import update_text
import time

def executeProgram(marie_memory, outputTextbox, app):
    program_length = 0
    for i in range(4096):  # If size() gives the memory size
        entry = marie_memory.read(i)  # Read memory at index i
        if entry != 0:  # Check if the entry is non-zero
            program_length += 1
        else:
            break

    MarieRegisters.PC = 0
    MarieRegisters.MAR = 0
    MarieRegisters.IR = 0
    MarieRegisters.AC = 0
    MarieRegisters.MBR = 0

    # Refactor to use a loop with the GUI's after() to avoid blocking
    def fetch_decode_cycle():
        if MarieRegisters.PC >= 0:
            fetch(marie_memory)  # Fetch the instruction based on PC
            decode(marie_memory)
            update_text(outputTextbox)  # Update the textbox
            # Schedule the next cycle after 500ms (0.5s)
            app.after(100, fetch_decode_cycle)

    # Start the fetch-decode cycle
    fetch_decode_cycle()

def fetch(marie_memory):
    MarieRegisters.MAR = MarieRegisters.PC
    MarieRegisters.IR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.PC += 1

def decode(marie_memory):
    # Extract the last 12 bits for MAR
    MarieRegisters.MAR = int(MarieRegisters.IR[-12:], 2)  # Convert the last 12 bits to an integer

    # Extract the first 4 bits for the instruction (opcode)
    opcode = int(MarieRegisters.IR[:4], 2)  # Convert the first 4 bits to an integer

    # Check if the opcode exists in the executionFunctions dictionary
    if opcode in executionFunctions:
        function = executionFunctions[opcode]  # Get the corresponding function
        if function.__name__ in instructionsWithoutArguments or function.__name__ == "inputInstruction":
            function(marie_memory)
        else:
            function(MarieRegisters.MAR, marie_memory)
    else:
        print(f"Invalid opcode: {opcode}")


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
