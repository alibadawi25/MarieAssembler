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
import tkinter as tk
from marie_register import MarieRegisters
import ErrorHandling
from Output_Mode import OutputMode

# Global variables
output_textbox = None
line_numbers_enabled = True

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
    Also removes lines that have incomplete or malformed line numbers.

    Args:
        input_text (str): The text with line numbers.

    Returns:
        str: The text with line numbers removed.
    """
    lines = input_text.split("\n")
    clean_lines = []

    for line in lines:
        # More robust line number removal - handles various formats
        if ":" in line:
            # Split only on the first colon to preserve colons in code
            parts = line.split(":", 1)
            if len(parts) == 2 and parts[0].strip().isdigit():
                # Only remove if the part before colon is purely numeric
                content = parts[1].strip()
                clean_lines.append(content)
            else:
                # Check if this looks like a malformed line number (starts with digits but incomplete)
                stripped_line = line.strip()
                if stripped_line and (stripped_line[0].isdigit() or stripped_line.startswith(':')):
                    # This looks like a partially deleted line number - remove the entire line
                    continue
                else:
                    # Keep the line as is if it doesn't match line number pattern
                    clean_lines.append(line.strip())
        else:
            stripped_line = line.strip()
            # Check if line starts with just digits (incomplete line number)
            if stripped_line and stripped_line.isdigit():
                # This is likely a line number without colon - remove it
                continue
            else:
                clean_lines.append(stripped_line)

    return "\n".join(clean_lines)


def format_assembly_code(code_text):
    """
    Formats assembly code with proper indentation and spacing.
    
    Args:
        code_text (str): The assembly code to format.
        
    Returns:
        str: The formatted assembly code.
    """
    lines = code_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            formatted_lines.append("")
            continue
            
        # Check if line is a label (ends with comma)
        if stripped_line.endswith(','):
            formatted_lines.append(stripped_line)
        # Check if line is an ORG directive
        elif stripped_line.upper().startswith('ORG'):
            formatted_lines.append(stripped_line.upper())
        # Check if line is a DEC directive
        elif ' DEC ' in stripped_line.upper():
            parts = stripped_line.split()
            if len(parts) >= 3:
                label = parts[0]
                dec_keyword = 'DEC'
                value = ' '.join(parts[2:])
                formatted_lines.append(f"{label} {dec_keyword} {value}")
            else:
                formatted_lines.append(stripped_line)
        # Check if line is a HEX directive
        elif ' HEX ' in stripped_line.upper():
            parts = stripped_line.split()
            if len(parts) >= 3:
                label = parts[0]
                hex_keyword = 'HEX'
                value = ' '.join(parts[2:])
                formatted_lines.append(f"{label} {hex_keyword} {value}")
            else:
                formatted_lines.append(stripped_line)
        # Regular instruction - add some indentation
        else:
            if not stripped_line.endswith(','):
                formatted_lines.append(f"    {stripped_line}")
            else:
                formatted_lines.append(stripped_line)
    
    return '\n'.join(formatted_lines)


# Legacy functions - kept for compatibility but not used with gutter system
def add_line_numbers(input_text):
    """Legacy function - now handled by separate gutter display"""
    return input_text

def update_input_with_line_numbers(input_textbox):
    """Legacy function - now handled by separate gutter display"""
    pass


def assemble_function(input_textbox, assemble_button):
    """
    Assembles the input program from the clean code editor.

    Args:
        input_textbox (customtkinter.CTkTextbox):
         The input textbox widget with the program code.
        assemble_button (customtkinter.CTkButton):
         The button used to trigger the assembly process.

    Returns:
        None
    """
    ErrorHandling.ErrorHandling.no_error = True  # Reset the error flag before assembly

    # Get the clean input text (no line numbers in the editor)
    clean_text = input_textbox.get("0.0", "end").strip()

    # Send clean text to the assembler
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


def copy_clean_code(input_textbox):
    """
    Copies the assembly code to clipboard (already clean since no line numbers in editor).

    Args:
        input_textbox (customtkinter.CTkTextbox): The input textbox widget with the code.

    Returns:
        str: "break" to prevent default copy behavior.
    """
    # Get the current text from the input textbox (already clean)
    input_text = input_textbox.get("0.0", "end-1c").strip()
    
    # Copy to clipboard
    input_textbox.clipboard_clear()
    input_textbox.clipboard_append(input_text)
    
    # Optional: Show a brief confirmation
    print("Code copied to clipboard!")
    
    # Return "break" to prevent the default Ctrl+C behavior
    return "break"


def copy_code(input_textbox):
    """
    Copies the assembly code to clipboard without line numbers.

    Args:
        input_textbox (customtkinter.CTkTextbox): The input textbox widget with the code.

    Returns:
        str: "break" to prevent default copy behavior.
    """
    # Get the current text from the input textbox
    input_text = input_textbox.get("0.0", "end-1c").strip()
    
    # Remove line numbers to get clean code
    clean_text = remove_line_numbers(input_text)
    
    # Copy to clipboard
    input_textbox.clipboard_clear()
    input_textbox.clipboard_append(clean_text)
    
    # Optional: Show a brief confirmation (you could add a status label for this)
    print("Code copied to clipboard without line numbers!")
    
    # Return "break" to prevent the default Ctrl+C behavior
    return "break"


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
    global output_textbox, line_numbers_enabled
    line_numbers_enabled = True  # Global toggle for line numbers
    
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    # Create the main window
    app = customtkinter.CTk()
    app.geometry("1200x750")
    app.title("Marie Assembler")  # Title for the window
    app.minsize(800, 600)  # Set minimum window size
    
    # Configure grid weights for responsiveness
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=0)  # Title row
    app.grid_rowconfigure(1, weight=1)  # Main content row
    app.grid_rowconfigure(2, weight=0)  # Button row

    # Title
    title_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
    
    label = customtkinter.CTkLabel(title_frame,
                                   text="Marie Assembler",
                                   fg_color="transparent",
                                   font=("Normal", 50))
    label.pack()

    # Main content frame
    main_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 30))
    
    # Configure main frame grid
    main_frame.grid_columnconfigure(0, weight=1)  # Input section
    main_frame.grid_columnconfigure(1, weight=0)  # Middle spacer
    main_frame.grid_columnconfigure(2, weight=1)  # Output section
    main_frame.grid_rowconfigure(0, weight=0)     # Labels row
    main_frame.grid_rowconfigure(1, weight=1)     # Content row

    # Input section with line numbers gutter
    input_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
    input_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
    input_frame.grid_columnconfigure(0, weight=0)  # Line numbers (fixed width)
    input_frame.grid_columnconfigure(1, weight=1)  # Code editor (expandable)
    input_frame.grid_rowconfigure(0, weight=0)  # Label
    input_frame.grid_rowconfigure(1, weight=0)  # Controls
    input_frame.grid_rowconfigure(2, weight=1)  # Editor area

    # Input label and controls
    input_header_frame = customtkinter.CTkFrame(input_frame, fg_color="transparent")
    input_header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
    input_header_frame.grid_columnconfigure(0, weight=1)
    input_header_frame.grid_columnconfigure(1, weight=0)
    input_header_frame.grid_columnconfigure(2, weight=0)

    input_label = customtkinter.CTkLabel(input_header_frame, text="Input",
                                        fg_color="transparent", font=("Normal", 20))
    input_label.grid(row=0, column=0, sticky="w")

    def format_code():
        """Format the assembly code with proper indentation"""
        current_text = input_textbox.get("0.0", "end-1c").strip()
        if current_text:
            # Format the code
            formatted_text = format_assembly_code(current_text)
            # Update the textbox
            input_textbox.delete("0.0", "end")
            input_textbox.insert("0.0", formatted_text)
            # Update line numbers
            if line_numbers_enabled:
                update_line_number_display()

    def toggle_line_numbers():
        """Toggle line numbers on/off"""
        global line_numbers_enabled
        line_numbers_enabled = not line_numbers_enabled
        
        if line_numbers_enabled:
            line_number_display.grid(row=2, column=0, sticky="nsew", padx=(0, 5))
            update_line_number_display()
            toggle_button.configure(text="Hide Line #")
        else:
            line_number_display.grid_remove()
            toggle_button.configure(text="Show Line #")

    format_button = customtkinter.CTkButton(input_header_frame,
                                           text="Format",
                                           command=format_code,
                                           width=80,
                                           height=25,
                                           corner_radius=5,
                                           font=("Normal", 12))
    format_button.grid(row=0, column=1, sticky="e", padx=(0, 5))

    toggle_button = customtkinter.CTkButton(input_header_frame,
                                           text="Hide Line #",
                                           command=toggle_line_numbers,
                                           width=100,
                                           height=25,
                                           corner_radius=5,
                                           font=("Normal", 12))
    toggle_button.grid(row=0, column=2, sticky="e")

    # Editor container frame
    editor_frame = customtkinter.CTkFrame(input_frame, fg_color="transparent")
    editor_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
    editor_frame.grid_columnconfigure(0, weight=0)  # Line numbers
    editor_frame.grid_columnconfigure(1, weight=1)  # Code editor
    editor_frame.grid_rowconfigure(0, weight=1)

    # Line number display (read-only)
    line_number_display = customtkinter.CTkTextbox(editor_frame, 
                                                   corner_radius=10, 
                                                   width=50,
                                                   font=("Courier", 14),
                                                   fg_color=("gray85", "gray25"))
    line_number_display.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    
    # Main code editor (without line numbers)
    input_textbox = customtkinter.CTkTextbox(editor_frame, 
                                             corner_radius=10, 
                                             wrap="word",
                                             font=("Courier", 14))
    input_textbox.grid(row=0, column=1, sticky="nsew")

    def update_line_number_display():
        """Update the line number display to match the code content"""
        if not line_numbers_enabled:
            return
            
        # Get total lines in the code editor
        code_content = input_textbox.get("0.0", "end-1c")
        lines = code_content.split('\n')
        total_lines = len(lines)
        
        # Generate line numbers
        line_numbers = []
        for i in range(1, total_lines + 1):
            line_numbers.append(str(i))
        
        # Update the line number display
        line_number_display.configure(state="normal")
        line_number_display.delete("0.0", "end")
        line_number_display.insert("0.0", '\n'.join(line_numbers))
        line_number_display.configure(state="disabled")  # Make it read-only

    # Simple scroll synchronization
    def sync_to_line_numbers():
        """Sync line numbers to match code editor scroll position"""
        if line_numbers_enabled:
            try:
                top, bottom = input_textbox.yview()
                line_number_display.yview_moveto(top)
            except tk.TclError:
                pass

    def sync_to_code_editor():
        """Sync code editor to match line numbers scroll position"""
        if line_numbers_enabled:
            try:
                top, bottom = line_number_display.yview()
                input_textbox.yview_moveto(top)
            except tk.TclError:
                pass

    # Track if we're currently syncing to prevent loops
    is_syncing = False

    def on_input_scroll(*args):
        """Handle input textbox scroll events"""
        global is_syncing
        if not is_syncing and line_numbers_enabled:
            is_syncing = True
            app.after_idle(lambda: [sync_to_line_numbers(), setattr(__builtins__, 'is_syncing', False)])

    def on_line_scroll(*args):
        """Handle line number scroll events"""
        global is_syncing
        if not is_syncing and line_numbers_enabled:
            is_syncing = True
            app.after_idle(lambda: [sync_to_code_editor(), setattr(__builtins__, 'is_syncing', False)])

    # Bind scroll events
    input_textbox.bind("<MouseWheel>", lambda e: app.after_idle(sync_to_line_numbers))
    input_textbox.bind("<Button-4>", lambda e: app.after_idle(sync_to_line_numbers))
    input_textbox.bind("<Button-5>", lambda e: app.after_idle(sync_to_line_numbers))
    
    line_number_display.bind("<MouseWheel>", lambda e: app.after_idle(sync_to_code_editor))
    line_number_display.bind("<Button-4>", lambda e: app.after_idle(sync_to_code_editor))
    line_number_display.bind("<Button-5>", lambda e: app.after_idle(sync_to_code_editor))

    # Handle scrollbar dragging by monitoring yview changes
    def monitor_scroll_changes():
        """Periodically check for scroll changes and sync accordingly"""
        if line_numbers_enabled and not is_syncing:
            try:
                # Check if scroll positions are different
                code_top, code_bottom = input_textbox.yview()
                line_top, line_bottom = line_number_display.yview()
                
                # If positions differ by more than a small threshold, sync them
                if abs(code_top - line_top) > 0.01:
                    # Determine which one changed more recently and sync the other
                    line_number_display.yview_moveto(code_top)
                    
            except tk.TclError:
                pass
        
        # Schedule next check
        app.after(100, monitor_scroll_changes)

    # Start the scroll monitoring
    monitor_scroll_changes()

    # Output section
    output_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
    output_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(10, 0))
    output_frame.grid_columnconfigure(0, weight=1)
    output_frame.grid_columnconfigure(1, weight=0)  # Option menu
    output_frame.grid_rowconfigure(0, weight=0)  # Label row
    output_frame.grid_rowconfigure(1, weight=1)  # Textbox

    # Output label and option menu in same row
    output_label_frame = customtkinter.CTkFrame(output_frame, fg_color="transparent")
    output_label_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    output_label_frame.grid_columnconfigure(0, weight=1)
    output_label_frame.grid_columnconfigure(1, weight=0)

    output_label = customtkinter.CTkLabel(output_label_frame, text="Output",
                                          fg_color="transparent", font=("Normal", 20))
    output_label.grid(row=0, column=0, sticky="w")

    options = ["DEC", "HEX", "ASCII"]
    option_menu = customtkinter.CTkOptionMenu(
        output_label_frame,
        values=options,
        command=option_changed
    )
    option_menu.set("DEC")
    option_menu.grid(row=0, column=1, sticky="e")

    output_textbox = customtkinter.CTkTextbox(output_frame, corner_radius=10, wrap="word")
    output_textbox.grid(row=1, column=0, columnspan=2, sticky="nsew")
    output_textbox.configure(state="disabled")

    # Button frame
    button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=0)
    button_frame.grid_columnconfigure(2, weight=0)
    button_frame.grid_columnconfigure(3, weight=1)

    # Create buttons with responsive positioning
    assemble_button = customtkinter.CTkButton(button_frame,
                                              text="Assemble",
                                              command=lambda: assemble_function(input_textbox, assemble_button),
                                              width=200,
                                              height=40,
                                              corner_radius=10)
    assemble_button.grid(row=0, column=1, padx=(0, 10))

    run_button = customtkinter.CTkButton(button_frame, text="Run",
                                         command=lambda: run_function(output_textbox, app),
                                         width=200, height=40,
                                         corner_radius=10)
    run_button.grid(row=0, column=2, padx=(10, 0))

    # Bind keyboard events
    input_textbox.bind("<Tab>", lambda event: handle_tab(input_textbox))
    input_textbox.bind("<KeyPress>", lambda event: open_assemble_button(assemble_button))
    # Bind Ctrl+C to copy code (now clean without line numbers)
    input_textbox.bind("<Control-c>", lambda event: copy_clean_code(input_textbox))
    # Bind the paste operation (Ctrl+V or right-click paste) to handle_paste
    input_textbox.bind("<Control-v>", lambda event: handle_paste())
    input_textbox.bind("<Button-3>", lambda event: handle_paste())
    
    # Update line numbers on text changes
    def on_text_change(event):
        """Update line number display when text changes"""
        if line_numbers_enabled:
            # Small delay to let the text change complete
            app.after(10, update_line_number_display)
    
    # Bind text change events to update line numbers
    input_textbox.bind("<KeyRelease>", on_text_change)
    input_textbox.bind("<Button-1>", lambda event: app.after(10, update_line_number_display))
    input_textbox.bind("<FocusIn>", lambda event: app.after(10, update_line_number_display))
    
    # Initialize line numbers display
    update_line_number_display()

    # Run the application
    app.mainloop()


if __name__ == "__main__":
    main()
