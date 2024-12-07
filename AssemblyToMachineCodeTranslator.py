import sys

def translate(instruction):
    instruction = instruction.lower()
    if instruction in instructionSet:
        instructionCode = instructionSet[instruction]
        instructionCodeStr = format(instructionCode, '04b')
        return instructionCodeStr
    else:
        pass

def translateSymbols(symbol):
    if symbol in symbolTable:
        symbolCode = symbolTable[symbol]
        return symbolCode
    else:
        print("Symbol "+symbol+" is not found.", end="")
        print("\nExiting The Program...")
        sys.exit(1)

instructionSet = {
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

instructionsWithArguments = [
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

instructionsWithoutArguments = [
    "input",
    "output",
    "halt",
    "clear"
]

symbolTable = {

}

