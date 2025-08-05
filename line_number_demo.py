"""
Demo script showing the enhanced line number system features.
"""

# Import the GUI functions for testing
from gui import add_line_numbers, remove_line_numbers, format_assembly_code

# Sample assembly code
sample_code = """
loop, load x
add y
store z
skipcond 400
jump loop
halt
x dec 5
y dec 10
z hex 0
"""

print("=== Enhanced Line Number System Demo ===\n")

print("1. Original code:")
print(sample_code.strip())
print()

print("2. After formatting:")
formatted = format_assembly_code(sample_code.strip())
print(formatted)
print()

print("3. After adding line numbers:")
numbered = add_line_numbers(formatted)
print(numbered)
print()

print("4. After removing line numbers:")
clean = remove_line_numbers(numbered)
print(clean)
print()

print("=== Features of the Enhanced System ===")
print("✓ Smart line number formatting with proper padding")
print("✓ Robust line number removal that preserves colons in code")
print("✓ Assembly code formatting with proper indentation")
print("✓ Toggle button to show/hide line numbers")
print("✓ Format button for automatic code styling")
print("✓ Smart cursor positioning when updating line numbers")
print("✓ Real-time line number updates during editing")
print("✓ Copy functionality that automatically removes line numbers")
