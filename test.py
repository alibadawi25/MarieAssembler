import ErrorHandling
from AssemblyToMachineCodeTranslator import *
from MarieMemory import MarieMemory
from MarieRegister import *
import customtkinter as ctk
import re


marie_memory = MarieMemory()

'''
print("Enter 0 to exit!")
print("Write your code below:")
'''
program = "jns addition\nload sum\noutput\nhalt\naddition, dec 0\nload sum\nadd x\nadd y\nstore sum\njumpi addition\nsum, dec 0\nx, dec 24\ny, dec 36"

'''
while True:


    newInstruction = input().strip()

    if newInstruction != "0":
        program += newInstruction+"\n"

    else:
        program = program[:-1]
        break
'''

program2 = "load x\nadd y\nstore x\nx, dec 10\ny, dec 20"


def programReader(program):
    instructions = program.split("\n")
    programCounter = 0
    for instruction in instructions:
        if instruction == "":
            pass
        else:
            instructionSplitter = re.split(r"[ \t]+", instruction.strip())
            if instructionSplitter[0][-1] == ",":
                new_text = instructionSplitter[0][:-1]
                symbolTable[new_text] = format(programCounter, '012b')
            programCounter += 1


def programTranslator(program):
    marie_memory.clear()
    MarieRegisters.PC = 0
    instructions = program.split("\n")
    programCounter = 0
    empty_lines = 0
    for instruction in instructions:
        if instruction == "":
            empty_lines+=1
        else:
            print(instruction)
            if MarieRegisters.PC >= 0:
                instructionSplitter = re.split(r"[ \t]+", instruction.strip())
                if instructionSplitter[0][-1] == ",":
                    if len(instructionSplitter) < 2:
                        error_handling((programCounter + empty_lines), "No instruction was written.")
                        MarieRegisters.PC = -1
                    if instructionSplitter[1].lower() in instructionSet:
                        instructionCode = translate(instructionSplitter[1])
                        marie_memory.write(programCounter, instructionCode, 0)
                        if len(instructionSplitter) > 2:
                            if instructionSplitter[1].lower() in instructionsWithArguments:
                                if instructionSplitter[2] in symbolTable:
                                    symbolCode = translateSymbols(instructionSplitter[2])
                                    marie_memory.write(programCounter, symbolCode, 1)
                                else:
                                    error_handling((programCounter+empty_lines), ("Symbol " + instructionSplitter[2] + " is not found."))
                                    MarieRegisters.PC = -1
                            elif instructionSplitter[1].lower() == "skipcond":
                                if instructionSplitter[2] == "800" or instructionSplitter[2] == "400" or instructionSplitter[2] == "000":
                                    marie_memory.write(programCounter, format(int(instructionSplitter[2][0]), '04b'), 1)
                                    marie_memory.write(programCounter, format(int(instructionSplitter[2][1:]), '08b'), 1)

                                else:
                                    error_handling((programCounter+empty_lines), "Incorrect argument for " + instructionSplitter[1] + "!")
                                    MarieRegisters.PC = -1
                            else:
                                error_handling((programCounter+empty_lines), instructionSplitter[1] + " does not accept arguments!")
                                MarieRegisters.PC = -1
                        elif instructionSplitter[1].lower() in instructionsWithArguments:
                            error_handling((programCounter+empty_lines), instructionSplitter[1] + " requires an argument!")
                            MarieRegisters.PC = -1
                        else:
                            marie_memory.write(programCounter, format(0, '012b'), 1)
                    elif instructionSplitter[1].upper() == "DEC":
                        if len(instructionSplitter) < 3:
                            error_handling((programCounter + empty_lines), "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(programCounter, format(int(instructionSplitter[2]), '016b'), 0)
                    elif instructionSplitter[1].upper() == "HEX":
                        if len(instructionSplitter) < 3:
                            error_handling((programCounter + empty_lines), "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(programCounter, hex_to_bin(instructionSplitter[2]), 0)
                    else:
                        error_handling((programCounter+empty_lines), "Instruction " + instruction + " not found.")
                        MarieRegisters.PC = -1
                else:
                    if instructionSplitter[0].lower() in instructionSet:
                        instructionCode = translate(instructionSplitter[0])
                        marie_memory.write(programCounter, instructionCode, 0)

                        if len(instructionSplitter) > 1:
                            if instructionSplitter[0].lower() in instructionsWithArguments:
                                if instructionSplitter[1] in symbolTable:
                                    symbolCode = translateSymbols(instructionSplitter[1])
                                    marie_memory.write(programCounter, symbolCode, 1)
                                else:
                                    error_handling((programCounter+empty_lines), ("Symbol " + instructionSplitter[1] + " is not found."))
                                    MarieRegisters.PC = -1
                            elif instructionSplitter[0].lower() == "skipcond":
                                if instructionSplitter[1] == "800" or instructionSplitter[1] == "400" or instructionSplitter[1] == "000":
                                    marie_memory.write(programCounter, format(int(instructionSplitter[1][0]), '04b'), 1)
                                    marie_memory.write(programCounter, format(int(instructionSplitter[1][1:]), '08b'), 1)

                                else:
                                    error_handling((programCounter+empty_lines), "Incorrect argument for " + instructionSplitter[0] + "!")
                                    MarieRegisters.PC = -1
                            else:
                                error_handling((programCounter+empty_lines), instructionSplitter[0] + " does not accept arguments!")
                                MarieRegisters.PC = -1

                        elif instructionSplitter[0].lower() in instructionsWithArguments:
                            error_handling((programCounter+empty_lines), instructionSplitter[0] + " requires an argument!")
                            MarieRegisters.PC = -1

                        else:
                            marie_memory.write(programCounter, format(0, '012b'), 1)
                    elif instructionSplitter[0].upper() == "DEC":
                        if len(instructionSplitter) < 2:
                            error_handling((programCounter + empty_lines), "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(programCounter, format(int(instructionSplitter[1]), '016b'), 0)
                    elif instructionSplitter[0].upper() == "HEX":
                        if len(instructionSplitter) < 2:
                            error_handling((programCounter + empty_lines), "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(programCounter, hex_to_bin(instructionSplitter[1]), 0)
                    else:
                        error_handling((programCounter+empty_lines), "Instruction " + instruction + " not found.")
                        MarieRegisters.PC = -1
                programCounter += 1


def hex_to_bin(hex_string):
    decimal_value = int(hex_string, 16)

    binary_value = format(decimal_value, "016b")
    return binary_value

def dec_to_hex(dec_string):
    decimal_value = int(dec_string)
    hex_value = hex(decimal_value)[2:]
    print("string "+ hex_value)
    return hex_value.upper()


def error_handling(pc, error_message):
    print("error")
    # Set the global error flag to False
    ErrorHandling.ErrorHandling.no_error = False

    # Create a new Toplevel window for the error message
    error_popup = ctk.CTkToplevel()
    error_popup.title("Error")
    error_popup.geometry("400x200")

    # Add a label to show the error message
    error_label = ctk.CTkLabel(error_popup, text=f"Error in line {pc+1}, {error_message}", font=("Arial", 14))
    error_label.pack(pady=20)

    # Add a close button to dismiss the popup
    close_button = ctk.CTkButton(error_popup, text="Close", command=error_popup.destroy)
    close_button.pack(pady=10)

    # Optional: If you want to block interaction with the main window while the popup is open, use:
    error_popup.grab_set()

def input_value():
    # Create a top-level window
    root = ctk.CTkToplevel()
    root.title("Input Value")
    root.geometry("320x250")

    entered_value = ctk.StringVar(value="")
    type_var = ctk.StringVar(value="DEC")
    result = {"value": None}  # Dictionary to store the result

    def on_accept():
        try:
            input_val = entered_value.get()
            if type_var.get() == "DEC":
                result["value"] = int(input_val)
            elif type_var.get() == "HEX":
                result["value"] = int(input_val, 16)
            elif type_var.get() == "ASCII":
                result["value"] = ord(input_val)
        except Exception:
            result["value"] = None  # Handle invalid input
            root.destroy()
            show_alert(title="Error",message="Invalid input provided.")
            result["value"] = input_value()
        root.destroy()  # Close the popup

    # Add widgets
    label_title = ctk.CTkLabel(root, text="Please Input Value", font=("Arial", 18), fg_color="transparent")
    label_title.pack(pady=20)

    label_value = ctk.CTkLabel(root, text="Value:", font=("Arial", 14), fg_color="transparent", text_color="white")
    label_value.place(relx=0.23, rely=0.3, anchor="e")

    value_entry = ctk.CTkEntry(root, textvariable=entered_value, width=180, font=("Arial", 14))
    value_entry.place(relx=0.55, rely=0.3, anchor="center")

    label_type = ctk.CTkLabel(root, text="Type:", font=("Arial", 14), fg_color="transparent", text_color="white")
    label_type.place(relx=0.23, rely=0.5, anchor="e")

    type_menu = ctk.CTkOptionMenu(root, variable=type_var, values=["DEC", "HEX", "ASCII"])
    type_menu.place(relx=0.55, rely=0.5, anchor="center")

    accept_button = ctk.CTkButton(root, text="Accept", command=on_accept)
    accept_button.place(relx=0.5, rely=0.8, anchor="center")

    # Prevent interaction with the main window
    root.grab_set()

    # Block execution until this window is closed
    root.wait_window()

    # Return the result after the popup closes
    return result["value"]

def show_alert(title="Alert", message="This is an alert message!"):
    # Create a top-level window
    alert_window = ctk.CTkToplevel()
    alert_window.title(title)
    alert_window.geometry("300x150")
    alert_window.resizable(False, False)

    # Add a label for the alert message
    message_label = ctk.CTkLabel(alert_window, text=message, font=("Arial", 14), wraplength=280, justify="center")
    message_label.pack(pady=20)

    # Add a button to close the alert
    close_button = ctk.CTkButton(alert_window, text="OK", command=alert_window.destroy)
    close_button.pack(pady=10)

    # Prevent interaction with the main window
    alert_window.grab_set()

    # Block execution until the alert window is closed
    alert_window.wait_window()
