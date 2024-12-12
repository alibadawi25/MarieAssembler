import customtkinter 
import test
from MarieRegister import MarieRegisters
import ErrorHandling


# Instruction set with binary opcodes
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
    "hex": 0,
    "dec": 0
}

output_mode = "DEC"

# Function to check and remove line numbers from the input text
def remove_line_numbers(input_text):
    lines = input_text.split("\n")
    clean_lines = []

    for line in lines:
        # Remove any existing line number (text before the first colon) and return the actual code
        clean_lines.append(line.split(":", 1)[-1].strip())  # Remove line number and return the actual code

    return "\n".join(clean_lines)


# Function to add line numbers only if they don't exist
def add_line_numbers(input_text):
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


# Function that updates the input textbox with correct line numbers
def update_input_with_line_numbers(event, inputTextbox):
    # Get the current cursor position
    cursor_index = inputTextbox.index("insert")  # e.g., "1.0"

    # Get the current text from the input textbox
    input_text = inputTextbox.get("0.0", "end-1c").strip()  # Remove any extra newlines

    # Remove existing line numbers and then add fresh ones
    clean_text = remove_line_numbers(input_text)
    numbered_text = add_line_numbers(clean_text)

    # Clear the textbox and insert the newly formatted text with line numbers
    inputTextbox.delete("0.0", "end")
    inputTextbox.insert("0.0", numbered_text)

    # Split the cursor index into line and character components
    line, char = cursor_index.split(".")
    line = int(line)  # Convert line to integer
    char = int(char)  # Convert character to integer

    # Add 2 to the character position (for new number and dash added)
    new_cursor_index = f"{line}.{char + 3}"  # Reconstruct the position string

    # Restore the cursor position
    inputTextbox.mark_set("insert", new_cursor_index)
    inputTextbox.see("insert")  # Ensure the cursor remains in view

    return None  # Prevent the default behavior




def assemble_function(inputTextbox, assembleButton):
    ErrorHandling.ErrorHandling.no_error = True  # Reset the error flag before assembly

    # Get the input text and add line numbers
    input_text = inputTextbox.get("0.0", "end").strip()  # Get the text and remove extra new lines
    numbered_text = add_line_numbers(input_text)  # Add line numbers to each line

    # Now remove line numbers before sending the text to the assembler
    clean_text = remove_line_numbers(numbered_text)  # Remove line numbers

    # Pass the cleaned text to the assembler
    test.programReader(clean_text)  # Reader function to handle the assembly process
    test.programTranslator(clean_text)
    if ErrorHandling.ErrorHandling.no_error:  # Only disable the button if there were no errors
        assembleButton.configure(state="disabled")
        assembleButton.configure(text="Assembled")
    else:
        assembleButton.configure(state="normal")
        assembleButton.configure(text="Assemble")


def update_text(outputTextbox):
    global output_mode
    print(output_mode)
    outputTextbox.configure(state="normal")  # Temporarily enable editing
    print(MarieRegisters.OUT)  # Clear previous text

    if MarieRegisters.OUT != "":
        if output_mode == "DEC":
            outputTextbox.insert("end", str(MarieRegisters.OUT) + "\n")  # Insert new text
            MarieRegisters.OUT = ""
        elif output_mode == "HEX":
            outputTextbox.insert("end", test.dec_to_hex(str(MarieRegisters.OUT)) + "\n")  # Insert new text
            MarieRegisters.OUT = ""   
    print(output_mode)
    outputTextbox.configure(state="disabled")  # Disable editing again


def run_function(outputTextbox, app):
    global output_mode
    outputTextbox.configure(state="normal")
    outputTextbox.delete("0.0", "end-1c")
    outputTextbox.configure(state="disabled")
    from FetchDecodeExecuteCycle import executeProgram
    executeProgram(test.marie_memory, outputTextbox, app)


def option_changed(new_option): 
    global output_mode
    output_mode = new_option

def auto_complete(inputTextbox):
    # Get the text from the inputTextbox and split it by spaces to find the last word
    current_text = inputTextbox.get("0.0", "end-1c")
    words = current_text.split()

    if words:  # Check if there's any text in the input
        last_word = words[-1]  # The last word typed
        # Find instructions that start with the last word typed
        matching_instructions = [instruction for instruction in instructionSet if instruction.startswith(last_word)]

        if matching_instructions:
            # Insert the closest match into the textbox
            closest_match = matching_instructions[0]
            inputTextbox.delete("1.0", "end")  # Clear the current text
            inputTextbox.insert("0.0", current_text + closest_match[len(last_word):])  # Add the rest of the instruction


def handle_tab(event, inputTextbox):
    auto_complete(inputTextbox)
    return "break"


def handle_paste(event, inputTextbox):
    return None

def open_assemble_button(event, assembleButton):
    assembleButton.configure(state="enabled")
    assembleButton.configure(text="Assemble")


def main():
    global outputTextbox
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    # Create the main window
    app = customtkinter.CTk()
    app.geometry("1000x700")
    app.title("Marie Assembler")  # Title for the window
    
    label = customtkinter.CTkLabel(app, text="Marie Assembler", fg_color="transparent", font=("Normal",50))
    label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

    inputLabel = customtkinter.CTkLabel(app, text="Input", fg_color="transparent", font=("Normal",20))
    inputLabel.place(relx=0.1, rely=0.25, anchor=customtkinter.E)
    inputTextbox = customtkinter.CTkTextbox(master=app, width=400, height=300, corner_radius=10, wrap="word")
    inputTextbox.place(relx=0.45, rely=0.5, anchor=customtkinter.E)


    options = ["DEC", "HEX"]

    # Create a CTkOptionMenu
    option_menu = customtkinter.CTkOptionMenu(
        master=app,
        values=options,               # List of options
        command=option_changed        # Callback function
    )

    # Set default option
    option_menu.set("DEC")  # Optional: Sets the default displayed option

    # Place the menu in the window
    option_menu.place(relx=0.80, rely=0.25, anchor=customtkinter.W)

    outputLabel = customtkinter.CTkLabel(app, text="Output", fg_color="transparent", font=("Normal",20))
    outputLabel.place(relx=0.55, rely=0.25, anchor=customtkinter.W)
    outputTextbox = customtkinter.CTkTextbox(master=app, width=400, height=300, corner_radius=10, wrap="word")
    outputTextbox.place(relx=0.55, rely=0.5, anchor=customtkinter.W)
    outputTextbox.configure(state="disabled")



    # Bind the Tab key to handle_tab
    inputTextbox.bind("<Tab>", lambda event: handle_tab(event, inputTextbox))
    inputTextbox.bind("<KeyPress>", lambda event: open_assemble_button(event, assembleButton))
    # Bind the paste operation (Ctrl+V or right-click paste) to handle_paste
    inputTextbox.bind("<Control-v>", lambda event: handle_paste(event, inputTextbox))  # For Ctrl+V paste
    inputTextbox.bind("<Button-3>", lambda event: handle_paste(event, inputTextbox))  # For right-click paste
    inputTextbox.bind("<Return>", lambda event: update_input_with_line_numbers(event, inputTextbox))

    # Create and style the button
    assembleButton = customtkinter.CTkButton(master=app,
                                             text="Assemble",
                                             command=lambda: assemble_function(inputTextbox, assembleButton),
                                             width=200,
                                             height=40,
                                             corner_radius=10)
    assembleButton.place(relx=0.35, rely=0.85, anchor=customtkinter.E)

    runButton = customtkinter.CTkButton(master=app, text="Run", command=lambda: run_function(outputTextbox, app),
                                        width=200, height=40,
                                        corner_radius=10)
    runButton.place(relx=0.65, rely=0.85, anchor=customtkinter.W)

    # Run the application
    app.mainloop()


if __name__ == "__main__":
    main()
