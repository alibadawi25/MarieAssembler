"""
Assembly Instruction Translator

This module provides functionality to translate assembly language instructions
into their corresponding machine code for a hypothetical MARIE-like architecture.

Features:
- `translate`: Converts an assembly instruction into a binary opcode.
- `translate_symbols`: Resolves symbols into their memory addresses.
- Predefined instruction set for translation, including instructions with and without arguments.
- Symbol table for resolving variable and label addresses.

Key Components:
- `instruction_set`: Dictionary mapping assembly instructions to opcode values.
- `instructions_with_arguments`: List of instructions requiring additional arguments.
- `instructions_without_arguments`: List of instructions that do not take arguments.
- `symbol_table`: Lookup table for translating labels or variables into binary addresses.
"""

import sys

def translate(instruction):
    """
    Translates an assembly instruction into its corresponding binary machine code.

    Args:
        instruction (str): The assembly instruction to translate.

    Returns:
        str: The binary string representation of the instruction's machine code,
             or None if the instruction is not found in the instruction set.
    """
    instruction = instruction.lower()
    if instruction in instruction_set:
        instruction_code = instruction_set[instruction]
        instruction_code_str = format(instruction_code, '04b')
        return instruction_code_str
    return None

def translate_symbols(symbol):
    """
    Resolves the address of a symbol by looking it up in the symbol table.

    Args:
        symbol (str): The symbol to translate into its machine code address.

    Returns:
        str: The binary string representation of the symbol's address.

    Raises:
        SystemExit: If the symbol is not found in the symbol table, exits the program
                    with an error message.
    """
    if symbol in symbol_table:
        symbol_code = symbol_table[symbol]
        return symbol_code
    print(f"Symbol {symbol} is not found.")
    print("\nExiting The Program...")
    sys.exit(1)

# The instruction set defines the opcode for each instruction.
instruction_set = {
    "jns": 0b0000,
    "load": 0b0001,
    "store": 0b0010,
    "add": 0b0011,
    "subt": 0b0100,
    "input": 0b0101,
    "output": 0b0110,
    "halt": 0b0111,
    "skipcond": 0b1000,
    "jump": 0b1001,
    "clear": 0b1010,
    "addi": 0b1011,
    "jumpi": 0b1100,
    "loadi": 0b1101,
    "storei": 0b1110,
}

# Instructions that require arguments (e.g., addresses or values).
instructions_with_arguments = [
    "jns",
    "load",
    "store",
    "add",
    "subt",
    "jump",
    "addi",
    "jumpi",
    "loadi",
    "storei"
]

# Instructions that do not require arguments.
instructions_without_arguments = [
    "input",
    "output",
    "halt",
    "clear"
]

# The symbol table holds the address of each symbol in binary form.
symbol_table = {}
