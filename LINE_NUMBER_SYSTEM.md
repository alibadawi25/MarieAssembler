# Enhanced Line Number System - Feature Guide

## Overview

The Marie Assembler now features a significantly improved line number system that provides better user experience, more robust functionality, and additional code formatting capabilities.

## New Features

### 1. Smart Line Number Management

#### Improved Line Number Addition

- **Consistent Padding**: Line numbers are padded based on total line count for proper alignment
- **Smart Detection**: Automatically detects existing line numbers and updates them correctly
- **Empty Line Handling**: Handles empty lines gracefully without adding unnecessary numbers

#### Robust Line Number Removal

- **Pattern Matching**: Uses intelligent pattern matching to distinguish line numbers from code content
- **Colon Preservation**: Preserves colons that are part of assembly code (labels, comments)
- **Multiple Format Support**: Handles various line number formats consistently

### 2. Toggle Functionality

#### Line Number Toggle Button

- **Show/Hide**: Easily toggle line numbers on and off with a single button
- **Real-time Updates**: Instant visual feedback when toggling
- **State Persistence**: Remembers user preference during the session

#### Smart Auto-Updates

- **Conditional Updates**: Line numbers only update when the feature is enabled
- **Event-Driven**: Updates triggered by relevant editing actions (Enter, Backspace, Delete)
- **Performance Optimized**: Minimal overhead when line numbers are disabled

### 3. Code Formatting

#### Assembly Code Formatter

- **Automatic Indentation**: Proper indentation for instructions vs. labels
- **Keyword Standardization**: Converts DEC/HEX keywords to uppercase
- **Label Recognition**: Identifies and properly formats labels ending with commas
- **ORG Directive Support**: Special handling for ORG directives

#### Format Button

- **One-Click Formatting**: Instantly format your assembly code
- **Integration**: Works seamlessly with line number system
- **Preservation**: Maintains line numbers if they're enabled

### 4. Enhanced User Experience

#### Improved Cursor Handling

- **Position Preservation**: Maintains cursor position when updating line numbers
- **Smart Positioning**: Accounts for line number formatting when restoring cursor
- **Error Recovery**: Falls back to safe positions if positioning fails

#### Copy Functionality Enhancement

- **Clean Copy**: Ctrl+C automatically removes line numbers before copying
- **Clipboard Ready**: Code copied is immediately usable in other editors
- **Seamless Integration**: Works transparently with existing workflow

## Usage Examples

### Basic Line Number Operations

```python
# Original code
code = "LOAD X\nADD Y\nSTORE Z"

# Add line numbers
numbered = add_line_numbers(code)
# Result: "1: LOAD X\n2: ADD Y\n3: STORE Z"

# Remove line numbers
clean = remove_line_numbers(numbered)
# Result: "LOAD X\nADD Y\nSTORE Z"
```

### Code Formatting

```python
# Unformatted code
messy_code = "loop,load x\nadd y\nstore z\nx dec 5"

# Format the code
formatted = format_assembly_code(messy_code)
# Result: "loop,load x\n    add y\n    store z\nx DEC 5"
```

### GUI Integration

```python
# Toggle line numbers
def toggle_line_numbers():
    global line_numbers_enabled
    line_numbers_enabled = not line_numbers_enabled
    # Update display accordingly...

# Format code with button
def format_code():
    current_text = input_textbox.get("0.0", "end-1c")
    formatted_text = format_assembly_code(current_text)
    input_textbox.delete("0.0", "end")
    input_textbox.insert("0.0", formatted_text)
```

## Technical Implementation

### Key Functions

1. **`add_line_numbers(input_text)`**

   - Adds properly formatted line numbers
   - Handles padding and alignment
   - Manages empty lines

2. **`remove_line_numbers(text)`**

   - Removes line numbers intelligently
   - Preserves colons in code content
   - Uses robust pattern matching

3. **`format_assembly_code(code_text)`**

   - Formats assembly code with proper indentation
   - Standardizes keywords and syntax
   - Maintains code structure

4. **`update_input_with_line_numbers(input_textbox)`**
   - Updates textbox with fresh line numbers
   - Preserves cursor position
   - Handles errors gracefully

### Event Handling

- **Real-time Updates**: Line numbers update automatically during editing
- **Conditional Processing**: Updates only occur when line numbers are enabled
- **Performance Optimization**: Minimal processing overhead

### Error Handling

- **Graceful Degradation**: System continues working even if some features fail
- **Safe Defaults**: Falls back to safe positions and states
- **User Feedback**: Clear visual indicators of system state

## Benefits

### For Users

- **Improved Readability**: Clear, consistently formatted line numbers
- **Better Control**: Easy toggle and formatting options
- **Seamless Workflow**: Copy/paste works intuitively
- **Professional Appearance**: Clean, well-formatted code display

### For Developers

- **Robust Implementation**: Handles edge cases and errors gracefully
- **Maintainable Code**: Clear separation of concerns and modular design
- **Extensible**: Easy to add new formatting features
- **Performance**: Efficient processing with minimal overhead

## Future Enhancements

### Planned Features

- **Syntax Highlighting**: Color-coded assembly instructions
- **Auto-Completion**: Smart completion for assembly mnemonics
- **Error Highlighting**: Visual indicators for syntax errors
- **Undo/Redo**: Better support for complex edit operations

### Configuration Options

- **Line Number Style**: Different formatting options
- **Auto-Format**: Automatic formatting on paste
- **Keyboard Shortcuts**: Customizable hotkeys for common operations

## Troubleshooting

### Common Issues

1. **Line numbers not updating**

   - Check if line numbers are enabled via toggle button
   - Verify event bindings are working correctly

2. **Cursor position problems**

   - The system will fall back to safe positions if positioning fails
   - This is normal behavior for edge cases

3. **Formatting issues**
   - Use the Format button to fix indentation problems
   - The formatter handles most assembly syntax correctly

### Debug Mode

For development and troubleshooting, enable debug output:

```python
# Add debug prints to key functions
def add_line_numbers(input_text):
    print(f"Adding line numbers to: {repr(input_text[:50])}")
    # ... rest of function
```

## Conclusion

The enhanced line number system provides a significantly improved user experience for the Marie Assembler. With smart toggling, automatic formatting, and robust error handling, users can focus on writing assembly code while the system handles the presentation details seamlessly.
