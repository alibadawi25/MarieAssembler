from MarieRegister import *
from MarieMemory import MarieMemory

def jns(loc, marie_memory):
    print(f"Function 'jns' called with loc = {loc}")
    MarieRegisters.MBR = MarieRegisters.PC
    MarieRegisters.MAR = loc
    marie_memory.write(MarieRegisters.MAR, MarieRegisters.MBR, 0)
    MarieRegisters.MBR = loc
    MarieRegisters.AC = 1
    MarieRegisters.AC += MarieRegisters.MBR
    MarieRegisters.PC = MarieRegisters.AC

def load(loc, marie_memory):
    print(f"Function 'load' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC = int(MarieRegisters.MBR, 2)

def store(loc, marie_memory):
    print(f"Function 'store' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = format(MarieRegisters.AC, '016b')
    marie_memory.write(MarieRegisters.MAR, MarieRegisters.MBR, 0)

def add(loc, marie_memory):
    print(f"Function 'add' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC += int(MarieRegisters.MBR, 2)

def subt(loc, marie_memory):
    print(f"Function 'subt' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC -= int(MarieRegisters.MBR, 2)

def inputInstruction(marie_memory):
    print("Function 'inputInstruction' called.")
    MarieRegisters.AC = int(input("Enter a value: "))

def output(marie_memory):
    print("Function 'output' called.")
    MarieRegisters.OUT = MarieRegisters.AC

def halt(marie_memory):
    print("Function 'halt' called.")
    print("Program halted.")
    MarieRegisters.PC = -1

def skipcond(condition, marie_memory):
    print(f"Function 'skipcond' called with condition = {condition}")
    if (condition == 0 and MarieRegisters.AC < 0) or \
            (condition == 1024 and MarieRegisters.AC == 0) or \
            (condition == 2048 and MarieRegisters.AC > 0):
        MarieRegisters.PC += 1  # Simulate skip

def jump(loc, marie_memory):
    print(f"Function 'jump' called with loc = {loc}")
    MarieRegisters.PC = loc

def clear(marie_memory):
    print("Function 'clear' called.")
    MarieRegisters.AC = 0

def addI(loc, marie_memory):
    print(f"Function 'addI' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.MAR = int(MarieRegisters.MBR, 2)
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.AC += int(MarieRegisters.MBR, 2)

def jumpI(loc, marie_memory):
    print(f"Function 'jumpI' called with loc = {loc}")
    MarieRegisters.MAR = loc
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.PC = MarieRegisters.MBR

def loadI(loc, marie_memory):
    print(f"Function 'loadI' called with loc = {loc}")
    MarieRegisters.MAR = loc
    print(f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC}, MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    print(f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC}, MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    MarieRegisters.MAR = int(MarieRegisters.MBR, 2)
    print(f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC}, MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    print(MarieRegisters.MAR)
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    print(f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC}, MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")
    print(MarieRegisters.MBR)
    MarieRegisters.AC = int(MarieRegisters.MBR,2)
    print(f"AC: {MarieRegisters.AC}, PC: {MarieRegisters.PC}, MBR: {MarieRegisters.MBR}, MAR: {MarieRegisters.MAR}, OUT: {MarieRegisters.OUT}")

def storeI(loc, marie_memory):
    print(f"Function 'storeI' called with loc = {loc}")
    MarieRegisters.MAR = marie_memory.read(loc)
    MarieRegisters.MBR = marie_memory.read(MarieRegisters.MAR)
    MarieRegisters.MAR = int(MarieRegisters.MBR, 2)
    MarieRegisters.MBR = MarieRegisters.AC
    marie_memory.write(MarieRegisters.MAR, MarieRegisters.MBR, 0)
