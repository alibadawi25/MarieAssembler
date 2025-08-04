# Marie Assembler

A complete implementation of a MARIE (Machine Architecture that is Really Intuitive and Easy) computer simulator with a modern graphical user interface.

## 🚀 Features

- **Complete MARIE Implementation**: Full instruction set with 16-bit architecture
- **Modern GUI**: Built with CustomTkinter for a sleek, dark-themed interface
- **Multiple Output Formats**: Support for Decimal, Hexadecimal, and ASCII output
- **Advanced Assembly Features**:
  - ORG directive support for memory organization
  - Label-based programming with symbol table
  - Comprehensive error handling and validation
- **Real-time Execution**: Step-by-step program execution with visual feedback
- **Auto-completion**: Intelligent instruction completion with Tab key
- **Line Management**: Automatic line numbering and formatting

## 📋 Requirements

- Python 3.x
- CustomTkinter (`pip install customtkinter`)

## 🛠️ Installation

1. Clone or download this repository
2. Install the required dependency:
   ```bash
   pip install customtkinter
   ```
3. Run the application:
   ```bash
   python gui.py
   ```

## 🎯 Quick Start

1. **Launch the application** by running `python gui.py`
2. **Write your assembly code** in the input area (left side)
3. **Click "Assemble"** to convert your code to machine language
4. **Click "Run"** to execute your program
5. **View output** in the output area (right side)

### Simple Example

```assembly
LOAD X
ADD Y
STORE RESULT
OUTPUT
HALT
X, DEC 10
Y, DEC 5
RESULT, DEC 0
```

## 📚 MARIE Instruction Set

### Core Instructions

| Instruction  | Opcode | Description                            |
| ------------ | ------ | -------------------------------------- |
| `LOAD addr`  | 0001   | Load value from memory address into AC |
| `STORE addr` | 0010   | Store AC value to memory address       |
| `ADD addr`   | 0011   | Add memory value to AC                 |
| `SUBT addr`  | 0100   | Subtract memory value from AC          |
| `INPUT`      | 0101   | Read input into AC                     |
| `OUTPUT`     | 0110   | Output AC value                        |
| `HALT`       | 0111   | Stop program execution                 |
| `JUMP addr`  | 1001   | Unconditional jump to address          |
| `CLEAR`      | 1010   | Clear AC (set to 0)                    |

### Advanced Instructions

| Instruction   | Opcode | Description                              |
| ------------- | ------ | ---------------------------------------- |
| `JNS addr`    | 0000   | Jump and Store subroutine                |
| `SKIPCOND`    | 1000   | Skip next instruction based on condition |
| `LOADI addr`  | 1101   | Load indirect                            |
| `STOREI addr` | 1110   | Store indirect                           |
| `JUMPI addr`  | 1100   | Jump indirect                            |
| `ADDI addr`   | 1011   | Add indirect                             |

### Data Directives

| Directive   | Description                | Example     |
| ----------- | -------------------------- | ----------- |
| `DEC value` | Declare decimal number     | `X, DEC 42` |
| `HEX value` | Declare hexadecimal number | `Y, HEX 2A` |
| `ORG addr`  | Set origin address         | `ORG 100`   |

## 🔧 Assembly Language Syntax

### Basic Format

```
[LABEL,] INSTRUCTION [OPERAND]
```

### Key Features

- **Labels**: End with comma (`,`) to define memory locations
- **Comments**: Use `//` for inline comments
- **Case Insensitive**: Instructions can be uppercase or lowercase
- **Flexible Spacing**: Tabs and spaces are handled automatically

### Simple Example with Labels

```assembly
// Simple calculator that adds two numbers
LOAD NUM1              // Load first number into AC
ADD NUM2               // Add second number to AC
STORE RESULT           // Store the sum
LOAD RESULT            // Load result for output
OUTPUT                 // Display the result
HALT                   // Stop program

// Data section
NUM1, DEC 15           // First number
NUM2, DEC 25           // Second number
RESULT, DEC 0          // Storage for result
```

## 🏗️ Architecture

### Registers

- **AC (Accumulator)**: Primary arithmetic register
- **IR (Instruction Register)**: Current instruction
- **MAR (Memory Address Register)**: Memory addressing
- **PC (Program Counter)**: Next instruction address
- **MBR (Memory Buffer Register)**: Data transfer buffer

### Memory

- **4096 words** of 16-bit memory
- **12-bit addressing** (0-4095)
- **Binary representation** with automatic conversion

## 🎮 GUI Controls

### Input Panel (Left)

- **Text Area**: Write assembly code with automatic line numbering
- **Auto-complete**: Press `Tab` to complete instruction names
- **Smart Formatting**: Automatic indentation and spacing

### Output Panel (Right)

- **Format Selection**: Choose DEC, HEX, or ASCII output
- **Real-time Display**: See program output as it executes
- **Clear Display**: Automatically cleared on each run

### Control Buttons

- **Assemble**: Compile assembly code to machine language
- **Run**: Execute the assembled program with visual feedback

## 🐛 Error Handling

The assembler provides comprehensive error detection:

- **Syntax Errors**: Invalid instructions, missing operands
- **Semantic Errors**: Undefined labels, incorrect arguments
- **Runtime Errors**: Invalid memory access, type mismatches
- **Data Validation**: Invalid numbers in DEC/HEX declarations

Error messages include line numbers and detailed descriptions.

## 📁 Project Structure

```
MarieAssembler/
├── gui.py                              # Main GUI application
├── test.py                             # Assembly and translation engine
├── assembly_to_machine_code_translator.py  # Instruction translation
├── marie_register.py                   # Register definitions
├── marie_memory.py                     # Memory simulation
├── fetch_decode_execute.py             # CPU execution cycle
├── program_executer.py                 # Individual instruction execution
├── Output_Mode.py                      # Display format management
├── ErrorHandling.py                    # Error handling utilities
├── test_cases.py                       # Test suite
└── README.md                           # This file
```

## 🧪 Example Programs

### Loop Example

```assembly
// Count from 1 to 5
LOAD COUNTER
LOOP, OUTPUT
ADD ONE
STORE COUNTER
SUBT LIMIT
SKIPCOND 800
JUMP LOOP
HALT

COUNTER, DEC 1
ONE, DEC 1
LIMIT, DEC 6
```

### String Output

```assembly
// Display "HELLO" using ASCII
ORG 100

LOAD H
OUTPUT
LOAD E
OUTPUT
LOAD L
OUTPUT
LOAD L
OUTPUT
LOAD O
OUTPUT
HALT

H, HEX 48    // 'H'
E, HEX 45    // 'E'
L, HEX 4C    // 'L'
O, HEX 4F    // 'O'
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Based on the MARIE architecture by Linda Null and Julia Lobur
- Built with Python and CustomTkinter for modern UI design
- Implements a complete fetch-decode-execute cycle simulation

---

**Happy Coding!** 🚀

For more detailed documentation, see [Marie Documentation](Marie%20Documentation).
