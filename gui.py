"""
This module implements the graphical user interface (GUI) for the Marie Assembler.

The GUI allows users to input assembly code, add/remove line numbers,
assemble the code into machine instructions, and execute the program.
It also provides options to view the output in different formats (DEC, HEX, ASCII).

Modules and Features:
- Line number management for input text.
- Integration with the assembler and memory modules.
- Output display and formatting options.
- Auto-completion of assembly instructions.
- Buttons for "Assemble" and "Run" actions.

Dependencies:
- customtkinter for the GUI components.
- MarieRegisters, OutputMode, and ErrorHandling for assembly and execution logic.

Usage:
Run this script to launch the GUI for the Marie Assembler.
"""


import test
import customtkinter
from marie_register import MarieRegisters
import ErrorHandling
from Output_Mode import OutputMode

# Instruction set with binary opcodes
instruction_set = ['jns', 'load', 'store', 'add',
                   'subt', 'input', 'output', 'halt',
                   'skipcond', 'jump', 'clear', 'addi',
                   'jumpi', 'loadi', 'storei', 'hex', 'dec']


#s => function | variable | class | ...
#function => def $func_name(prams): | def $func_name():
#prams =>  pram_name, prams| pram_name
def remove_line_numbers(input_text):
    """
    Removes line numbers from the input text.

    Args:
        input_text (str): The text with line numbers.

    Returns:
        str: The text with line numbers removed.
    """
    lines = input_text.split("\n")
    clean_lines = []

    for line in lines:
        # Remove any existing line number (text before the first colon) and return the actual code
        clean_lines.append(line.split(":",
                                      1)[-1].strip())
        # Remove line number and return the actual code

    return "\n".join(clean_lines)


def add_line_numbers(input_text):
    """
    Adds line numbers to the input text.

    Args:
        input_text (str): The text to which line numbers should be added.

    Returns:
        str: The text with line numbers added.
    """
    lines = input_text.split("\n")
    numbered_lines = []

    for i, line in enumerate(lines, start=1):
        # Only add the line number if it's not already there
        if not line.strip().startswith(str(i) + ":"):
            numbered_lines.append(f"{i}: {line}")
        else:
            # If the line already starts with a number, keep it as is
            numbered_lines.append(line.strip())  # Remove any excess spaces or characters

    return "\n".join(numbered_lines)


def update_input_with_line_numbers(input_textbox):
    """
    Updates the input textbox with fresh line numbers.

    Args:
        input_textbox (customtkinter.CTkTextbox): The input textbox widget to be updated.

    Returns:
        None
    """
    cursor_index = input_textbox.index("insert")  # e.g., "1.0"

    # Get the current text from the input textbox
    input_text = input_textbox.get("0.0", "end-1c").strip()  # Remove any extra newlines

    # Remove existing line numbers and then add fresh ones
    clean_text = remove_line_numbers(input_text)
    numbered_text = add_line_numbers(clean_text)

    # Clear the textbox and insert the newly formatted text with line numbers
    input_textbox.delete("0.0", "end")
    input_textbox.insert("0.0", numbered_text)

    counter = 3
    # Split the cursor index into line and character components
    line, char = cursor_index.split(".")
    line = int(line)  # Convert line to integer
    char = int(char)  # Convert character to integer

    if line > 9:
        counter = 4
    elif line > 99:
        counter = 5

    # Add 2 to the character position (for new number and dash added)
    new_cursor_index = f"{line}.{char + counter}"  # Reconstruct the position string

    # Restore the cursor position
    input_textbox.mark_set("insert", new_cursor_index)
    input_textbox.see("insert")  # Ensure the cursor remains in view


def assemble_function(input_textbox, assemble_button):
    """
    Assembles the input program by adding line numbers,
     removing them, and passing the code to the assembler.

    Args:
        input_textbox (customtkinter.CTkTextbox):
         The input textbox widget with the program code.
        assemble_button (customtkinter.CTkButton):
         The button used to trigger the assembly process.

    Returns:
        None
    """
    ErrorHandling.ErrorHandling.no_error = True  # Reset the error flag before assembly

    # Get the input text and add line numbers
    input_text = input_textbox.get("0.0", "end").strip()
    numbered_text = add_line_numbers(input_text)  # Add line numbers to each line

    # Now remove line numbers before sending the text to the assembler
    clean_text = remove_line_numbers(numbered_text)  # Remove line numbers
    # Pass the cleaned text to the assembler
    test.program_reader(clean_text)  # Reader function to handle the assembly process
    test.program_translator(clean_text)
    print(test.marie_memory)
    print(test.symbol_table)
    print(test.marie_memory.read(268))
    if ErrorHandling.ErrorHandling.no_error:
        assemble_button.configure(state="disabled")
        assemble_button.configure(text="Assembled")
    else:
        assemble_button.configure(state="normal")
        assemble_button.configure(text="Assemble")


def update_text(output_textbox):
    """
    Updates the output textbox based on the current output mode (DEC, HEX, or ASCII).

    Args:
        output_textbox (customtkinter.CTkTextbox): The output textbox widget to display the results.

    Returns:
        None
    """
    print(OutputMode.output_mode)
    output_textbox.configure(state="normal")  # Temporarily enable editing
    if MarieRegisters.OUT != "":
        if OutputMode.output_mode == "DEC":
            output_textbox.insert("end", str(MarieRegisters.OUT) + "\n")  # Insert new text
            MarieRegisters.OUT = ""
        elif OutputMode.output_mode == "HEX":
            output_textbox.insert("end",
                                  test.dec_to_hex(
                                      str(MarieRegisters.OUT)) + "\n")  # Insert new text
            MarieRegisters.OUT = ""
        elif OutputMode.output_mode == "ASCII":
            print(MarieRegisters.OUT)
            output_textbox.insert("end", chr(MarieRegisters.OUT))  # Insert new text
            MarieRegisters.OUT = ""

    if MarieRegisters.IN != "":
        MarieRegisters.AC = MarieRegisters.IN
        MarieRegisters.IN = ""
    output_textbox.configure(state="disabled")  # Disable editing again


def run_function(output_textbox, app):
    """
    Runs the program execution cycle and updates the output textbox.

    Args:
        output_textbox (customtkinter.CTkTextbox): The output textbox widget.
        app (customtkinter.Tk): The main application instance to schedule the fetch-decode cycle.

    Returns:
        None
    """
    output_textbox.configure(state="normal")
    output_textbox.delete("0.0", "end-1c")
    output_textbox.configure(state="disabled")
    from fetch_decode_execute import executeProgram
    executeProgram(output_textbox, app)


def option_changed(new_option):
    """
    Changes the output mode based on the selected option.

    Args:
        new_option (str): The new output mode option (DEC, HEX, or ASCII).

    Returns:
        None
    """
    print(new_option)
    OutputMode.output_mode = new_option


def auto_complete(input_textbox):
    """
    Automatically completes the instruction based on the last typed word.

    Args:
        input_textbox (customtkinter.CTkTextbox): The input textbox widget.

    Returns:
        None
    """
    # Get the text from the input_textbox and split it by spaces to find the last word
    current_text = input_textbox.get("0.0", "end-1c")
    words = current_text.split()

    if words:  # Check if there's any text in the input
        last_word = words[-1].lower()  # The last word typed
        # Find instructions that start with the last word typed
        matching_instructions = [instruction
                                 for instruction in instruction_set
                                 if instruction.startswith(last_word)]

        if matching_instructions:
            # Insert the closest match into the textbox
            closest_match = matching_instructions[0]
            input_textbox.delete("1.0", "end")  # Clear the current text
            input_textbox.insert("0.0",
                                 current_text
                                 + closest_match[len(last_word):])


def handle_tab(input_textbox):
    """
    Handles the Tab key event to trigger auto-completion of instructions.

    Args:
        input_textbox (customtkinter.CTkTextbox): The input textbox widget.

    Returns:
        str: "break" to prevent default behavior.
    """
    auto_complete(input_textbox)
    return "break"


def handle_paste():
    """
       Handles the paste event (Ctrl+V or right-click paste) in the input textbox.
       Returns:
           None
       """
    return None


def open_assemble_button(assemble_button):
    """
    Enables the assemble button when the input textbox is updated.

    Args:
        assemble_button (customtkinter.CTkButton): The assemble button widget.

    Returns:
        None
    """
    assemble_button.configure(state="enabled")
    assemble_button.configure(text="Assemble")


def main():
    """
    Initializes and runs the main application for the Marie assembler.

    Creates the GUI, binds events, and starts the Tkinter main loop.

    Returns:
        None
    """
    global output_textbox
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    # Create the main window
    app = customtkinter.CTk()
    app.geometry("1000x700")
    app.title("Marie Assembler")  # Title for the window

    label = customtkinter.CTkLabel(app,
                                   text="Marie Assembler",
                                   fg_color="transparent",
                                   font=("Normal", 50))
    label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

    input_label = customtkinter.CTkLabel(app, text="Input",
                                        fg_color="transparent", font=("Normal", 20))
    input_label.place(relx=0.1, rely=0.25, anchor=customtkinter.E)
    input_textbox = customtkinter.CTkTextbox(master=app, width=400,
                                             height=300, corner_radius=10, wrap="word",
                                             font=("Normal", 14))
    input_textbox.place(relx=0.45, rely=0.5, anchor=customtkinter.E)

    options = ["DEC", "HEX", "ASCII"]

    # Create a CTkOptionMenu
    option_menu = customtkinter.CTkOptionMenu(
        master=app,
        values=options,  # List of options
        command=option_changed  # Callback function
    )

    # Set default option
    option_menu.set("DEC")  # Optional: Sets the default displayed option

    # Place the menu in the window
    option_menu.place(relx=0.80, rely=0.25, anchor=customtkinter.W)

    output_label = customtkinter.CTkLabel(app, text="Output",
                                          fg_color="transparent", font=("Normal", 20))
    output_label.place(relx=0.55, rely=0.25, anchor=customtkinter.W)
    output_textbox = customtkinter.CTkTextbox(master=app, width=400,
                                              height=300, corner_radius=10, wrap="word")
    output_textbox.place(relx=0.55, rely=0.5, anchor=customtkinter.W)
    output_textbox.configure(state="disabled")

    # Bind the Tab key to handle_tab
    input_textbox.bind("<Tab>", lambda event: handle_tab(input_textbox))
    input_textbox.bind("<KeyPress>", lambda event: open_assemble_button(assemble_button))
    # Bind the paste operation (Ctrl+V or right-click paste) to handle_paste
    input_textbox.bind("<Control-v>",
                       lambda event: handle_paste())  # For Ctrl+V paste
    input_textbox.bind("<Button-3>",
                       lambda event: handle_paste())  # For right-click paste
    input_textbox.bind("<Return>",
                       lambda event: update_input_with_line_numbers(input_textbox))

    # Create and style the button
    assemble_button = customtkinter.CTkButton(master=app,
                                              text="Assemble",
                                              command=
                                              lambda: assemble_function
                                              (input_textbox, assemble_button),
                                              width=200,
                                              height=40,
                                              corner_radius=10)
    assemble_button.place(relx=0.35, rely=0.85, anchor=customtkinter.E)

    run_button = customtkinter.CTkButton(master=app, text="Run",
                                         command=lambda: run_function(output_textbox, app),
                                         width=200, height=40,
                                         corner_radius=10)
    run_button.place(relx=0.65, rely=0.85, anchor=customtkinter.W)

    # Run the application
    app.mainloop()


if __name__ == "__main__":
    main()
