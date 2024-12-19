"""
This is a file that has the main functions of the assembler itself
"""

import ErrorHandling
from assembly_to_machine_code_translator import *
from marie_memory import MarieMemory
from marie_register import *
import customtkinter as ctk
import re

marie_memory = MarieMemory()


def program_reader(program):
    """
    Reads the assembly program line by line and populates the symbol table
    for labels (such as variables and addresses).
    """
    instructions = program.split("\n")
    program_counter = 0
    for instruction in instructions:
        if instruction != "":
            instruction_splitter = re.split(r"[ \t]+", instruction.strip())
            if instruction_splitter[0][-1] == ",":
                new_text = instruction_splitter[0][:-1]
                symbol_table[new_text] = format(program_counter, '012b')
            program_counter += 1


def program_translator(program):
    """
    Translates the given assembly program into machine code and writes it to memory.
    Also handles error checking, instruction argument validation, and symbol resolution.
    """
    marie_memory.clear()
    MarieRegisters.PC = 0
    instructions = program.split("\n")
    program_counter = 0
    empty_lines = 0
    for instruction in instructions:
        if instruction == "":
            empty_lines += 1
        else:
            print(instruction)
            if MarieRegisters.PC >= 0:
                instruction_splitter = re.split(r"[ \t]+", instruction.strip())
                if instruction_splitter[0][-1] == ",":
                    if len(instruction_splitter) < 2:
                        error_handling((program_counter + empty_lines),
                                       "No instruction was written.")
                        MarieRegisters.PC = -1
                    if instruction_splitter[1].lower() in instruction_set:
                        instruction_code = translate(instruction_splitter[1])
                        marie_memory.write(program_counter, instruction_code, 0)
                        if len(instruction_splitter) > 2:
                            if instruction_splitter[1].lower() in instructions_with_arguments:
                                if instruction_splitter[2] in symbol_table:
                                    symbol_code = translate_symbols(instruction_splitter[2])
                                    marie_memory.write(program_counter, symbol_code, 1)
                                else:
                                    error_handling((program_counter + empty_lines),
                                                   ("Symbol " + instruction_splitter[2]
                                                    + " is not found."))
                                    MarieRegisters.PC = -1
                            elif instruction_splitter[1].lower() == "skipcond":
                                if instruction_splitter[2] in ["800", "400", "000"]:
                                    marie_memory.write(
                                        program_counter,
                                                       format(int(instruction_splitter[2][0]),
                                                              '04b'), 1)
                                    marie_memory.write(program_counter,
                                                       format(int(instruction_splitter[2][1:]),
                                                              '08b'), 1)
                                else:
                                    error_handling((program_counter + empty_lines),
                                                   "Incorrect argument for " +
                                                   instruction_splitter[1] + "!")
                                    MarieRegisters.PC = -1
                            else:
                                error_handling((program_counter + empty_lines),
                                               instruction_splitter[1] +
                                               " does not accept arguments!")
                                MarieRegisters.PC = -1
                        elif instruction_splitter[1].lower() in instructions_with_arguments:
                            error_handling((program_counter + empty_lines),
                                           instruction_splitter[1] +
                                           " requires an argument!")
                            MarieRegisters.PC = -1
                        else:
                            marie_memory.write(program_counter, format(0, '012b'), 1)
                    elif instruction_splitter[1].upper() == "DEC":
                        if len(instruction_splitter) < 3:
                            error_handling((program_counter + empty_lines),
                                           "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(program_counter,
                                           format(int(instruction_splitter[2]), '016b'), 0)
                    elif instruction_splitter[1].upper() == "HEX":
                        if len(instruction_splitter) < 3:
                            error_handling((program_counter + empty_lines),
                                           "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(program_counter,
                                           hex_to_bin(instruction_splitter[2]), 0)
                    else:
                        error_handling((program_counter + empty_lines),
                                       "Instruction " + instruction + " not found.")
                        MarieRegisters.PC = -1
                else:
                    if instruction_splitter[0].lower() in instruction_set:
                        instruction_code = translate(instruction_splitter[0])
                        marie_memory.write(program_counter, instruction_code, 0)

                        if len(instruction_splitter) > 1:
                            if instruction_splitter[0].lower() in instructions_with_arguments:
                                if instruction_splitter[1] in symbol_table:
                                    symbol_code = translate_symbols(instruction_splitter[1])
                                    marie_memory.write(program_counter, symbol_code, 1)
                                else:
                                    error_handling((program_counter + empty_lines),
                                                   ("Symbol " + instruction_splitter[1] +
                                                    " is not found."))
                                    MarieRegisters.PC = -1
                            elif instruction_splitter[0].lower() == "skipcond":
                                if instruction_splitter[1] in ["800", "400", "000"]:
                                    marie_memory.write(program_counter,
                                                       format(int(instruction_splitter[1][0]),
                                                              '04b'), 1)
                                    marie_memory.write(program_counter,
                                                       format(int(instruction_splitter[1][1:]),
                                                              '08b'), 1)
                                else:
                                    error_handling((program_counter + empty_lines),
                                                   "Incorrect argument for " +
                                                   instruction_splitter[0] + "!")
                                    MarieRegisters.PC = -1
                            else:
                                error_handling((program_counter + empty_lines),
                                               instruction_splitter[0] +
                                               " does not accept arguments!")
                                MarieRegisters.PC = -1

                        elif instruction_splitter[0].lower() in instructions_with_arguments:
                            error_handling((program_counter + empty_lines),
                                           instruction_splitter[0] + " requires an argument!")
                            MarieRegisters.PC = -1

                        else:
                            marie_memory.write(program_counter, format(0, '012b'), 1)
                    elif instruction_splitter[0].upper() == "DEC":
                        if len(instruction_splitter) < 2:
                            error_handling((program_counter + empty_lines),
                                           "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(program_counter,
                                           format(int(instruction_splitter[1]),
                                                  '016b'), 0)
                    elif instruction_splitter[0].upper() == "HEX":
                        if len(instruction_splitter) < 2:
                            error_handling((program_counter + empty_lines),
                                           "No value was written.")
                            MarieRegisters.PC = -1
                        marie_memory.write(program_counter,
                                           hex_to_bin(instruction_splitter[1]), 0)
                    else:
                        error_handling((program_counter + empty_lines),
                                       "Instruction " + instruction + " not found.")
                        MarieRegisters.PC = -1
                program_counter += 1


def hex_to_bin(hex_string):
    """
    Converts a hexadecimal string to a 16-bit binary string.
    """
    decimal_value = int(hex_string, 16)
    binary_value = format(decimal_value, "016b")
    return binary_value


def dec_to_hex(dec_string):
    """
    Converts a decimal string to a hexadecimal string.
    """
    decimal_value = int(dec_string)
    hex_value = hex(decimal_value)[2:]
    print("string " + hex_value)
    return hex_value.upper()


def error_handling(pc, error_message):
    """
    Handles errors by displaying an error message in a popup window.
    """
    print("error")
    ErrorHandling.ErrorHandling.no_error = False
    error_popup = ctk.CTkToplevel()
    error_popup.title("Error")
    error_popup.geometry("400x200")
    error_label = ctk.CTkLabel(error_popup,
                               text=f"Error in line {pc + 1},"
                                                 f" {error_message}",
                               font=("Arial", 14))
    error_label.pack(pady=20)
    close_button = ctk.CTkButton(error_popup,
                                 text="Close",
                                 command=error_popup.destroy)
    close_button.pack(pady=10)
    error_popup.grab_set()


def input_value():
    """
    Prompts the user to input a value in
     different formats (DEC, HEX, or ASCII)
    through a graphical user interface.
    """
    root = ctk.CTkToplevel()
    root.title("Input Value")
    root.geometry("320x250")

    entered_value = ctk.StringVar(value="")
    type_var = ctk.StringVar(value="DEC")
    result = {"value": None}

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
            result["value"] = None
            root.destroy()
            show_alert(title="Error", message="Invalid input provided.")
            result["value"] = input_value()
        root.destroy()

    label_title = ctk.CTkLabel(root, text="Please Input Value",
                               font=("Arial", 18), fg_color="transparent")
    label_title.pack(pady=20)

    label_value = ctk.CTkLabel(root, text="Value:",
                               font=("Arial", 14),
                               fg_color="transparent", text_color="white")
    label_value.place(relx=0.23, rely=0.3, anchor="e")

    value_entry = ctk.CTkEntry(root, textvariable=entered_value,
                               width=180, font=("Arial", 14))
    value_entry.place(relx=0.55, rely=0.3, anchor="center")

    label_type = ctk.CTkLabel(root, text="Type:", font=("Arial", 14),
                              fg_color="transparent", text_color="white")
    label_type.place(relx=0.23, rely=0.5, anchor="e")

    type_menu = ctk.CTkOptionMenu(root, variable=type_var,
                                  values=["DEC", "HEX", "ASCII"])
    type_menu.place(relx=0.55, rely=0.5, anchor="center")

    accept_button = ctk.CTkButton(root, text="Accept", command=on_accept)
    accept_button.place(relx=0.5, rely=0.8, anchor="center")

    root.grab_set()
    root.wait_window()
    return result["value"]


def show_alert(title="Alert", message="This is an alert message!"):
    """
    Displays an alert message in a popup window.
    """
    alert_window = ctk.CTkToplevel()
    alert_window.title(title)
    alert_window.geometry("300x150")
    alert_window.resizable(False, False)
    alert_label = ctk.CTkLabel(alert_window, text=message, font=("Arial", 14), wraplength=250)
    alert_label.pack(pady=20)
    close_button = ctk.CTkButton(alert_window, text="Close", command=alert_window.destroy)
    close_button.pack(pady=10)
    alert_window.grab_set()
    alert_window.wait_window()
