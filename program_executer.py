from test import *


def jns(loc):
    """
    Performs the 'JNS' (Jump and Save) instruction.

    Args:
        loc (int): The location to jump to.

    Returns:
        None
    """
    print(f"Function 'jns' called with loc = {loc}")
    MarieRegisters.MBR = MarieRegisters.PC
    MarieRegisters.MAR = loc
    marie_memory.write(MarieRegisters.MAR, MarieRegisters.MBR, 0)
    MarieRegisters.MBR = loc
    MarieRegisters.AC = 1
    MarieRegisters.AC += MarieRegisters.MBR
    MarieRegisters.PC = MarieRegisters.AC


def load(loc):
    """
    Loads the value from the given location into the accumulator (AC).

    Args:
        loc (int): The location to load the value from.

    Returns:
        None
    """
    print(f"Function 'load' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC = int(MarieRegisters.MBR, 2)


def store(loc):
    """
    Stores the value in the accumulator (AC) to the specified location.

    Args:
        loc (int): The location to store the value in.

    Returns:
        None
    """
    print(f"Function 'store' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = format(MarieRegisters.AC, '016b')
    marie_memory.write(MarieRegisters.MAR, MarieRegisters.MBR, 0)


def add(loc):
    """
    Adds the value from the given location to the accumulator (AC).

    Args:
        loc (int): The location to add the value from.

    Returns:
        None
    """
    print(f"Function 'add' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    print(f"MBR: {MarieRegisters.MBR}")
    MarieRegisters.AC += int(MarieRegisters.MBR, 2)


def subt(loc):
    """
    Subtracts the value from the given location from the accumulator (AC).

    Args:
        loc (int): The location to subtract the value from.

    Returns:
        None
    """
    print(f"Function 'subt' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC -= int(MarieRegisters.MBR, 2)


def inputInstruction():
    """
    Loads the value entered by the user into the input register (IN).

    Returns:
        None
    """
    print("Function 'input' called.")
    MarieRegisters.IN = int(input_value())


def output():
    """
    Stores the value in the accumulator (AC) into the output register (OUT).

    Returns:
        None
    """
    print("Function 'output' called.")
    MarieRegisters.OUT = MarieRegisters.AC


def halt():
    """
    Halts the program and sets the program counter (PC) to -1.

    Returns:
        None
    """
    print("Function 'halt' called.")
    print("Program halted.")
    MarieRegisters.PC = -1


def skipcond(condition):
    """
    Skips the next instruction based on the given condition.

    Args:
        condition (int): The condition to evaluate for skipping.

    Returns:
        None
    """
    print(f"Function 'skipcond' called with condition = {condition}")
    if (condition == 0 and MarieRegisters.AC < 0) or \
            (condition == 1024 and MarieRegisters.AC == 0) or \
            (condition == 2048 and MarieRegisters.AC > 0):
        MarieRegisters.PC += 1  # Simulate skip


def jump(loc):
    """
    Jumps to the specified location by updating the program counter (PC).

    Args:
        loc (int): The location to jump to.

    Returns:
        None
    """
    print(f"Function 'jump' called with loc = {loc}")
    MarieRegisters.PC = loc


def clear():
    """
    Clears the accumulator (AC) by setting it to 0.

    Returns:
        None
    """
    print("Function 'clear' called.")
    MarieRegisters.AC = 0


def addI(loc):
    """
    Performs the 'ADD Indirect' instruction.

    Args:
        loc (int): The location to fetch the indirect value from.

    Returns:
        None
    """
    print(f"Function 'addI' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.MAR = int(MarieRegisters.MBR, 2)
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC += int(MarieRegisters.MBR, 2)


def jumpI(loc):
    """
    Performs the 'Jump Indirect' instruction.

    Args:
        loc (int): The location to fetch the indirect jump address from.

    Returns:
        None
    """
    print(f"Function 'jumpI' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.PC = MarieRegisters.MBR


def loadI(loc):
    """
    Loads the value from the location specified by the indirect address.

    Args:
        loc (int): The location of the indirect address.

    Returns:
        None
    """
    print(f"Function 'loadI' called with loc = {loc}")
    MarieRegisters.MAR = loc
    print(
        f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC},"
        f" MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    print(
        f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC},"
        f" MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    MarieRegisters.MAR = int(MarieRegisters.MBR, 2)
    print(
        f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC},"
        f" MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    print(MarieRegisters.MAR)
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    print(
        f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC},"
        f" MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    print(MarieRegisters.MBR)
    MarieRegisters.AC = int(MarieRegisters.MBR, 2)
    print(
        f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC},"
        f" MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")


def storeI(loc):
    """
    Performs the 'Store Indirect' instruction.

    Args:
        loc (int): The location to store the value in via indirect addressing.

    Returns:
        None
    """
    print(f"Function 'storeI' called with loc = {loc}")
    MarieRegisters.MAR = marie_memory.read(loc)
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.MAR = int(MarieRegisters.MBR, 2)
    MarieRegisters.MBR = MarieRegisters.AC
    marie_memory.write(MarieRegisters.MAR, MarieRegisters.MBR, 0)
