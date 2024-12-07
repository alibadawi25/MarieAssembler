class MarieMemory:
    def __init__(self, size=4096):
        self.memory = [0] * size

    def read(self, address):
        if 0 <= address < len(self.memory):
            return self.memory[address]
        else:
            raise IndexError("Address out of range")

    def write(self, address, value, mode):
        if 0 <= address < len(self.memory) and mode == 0:
            self.memory[address] = value
        elif 0 <= address < len(self.memory) and mode == 1:
            self.memory[address] = self.memory[address]+value
        else:
            raise IndexError("Address out of range")

    def clear(self):
        self.memory = [0] * len(self.memory)

    def __str__(self):
        return str(self.memory)