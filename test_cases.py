from assembly_to_machine_code_translator import translate, instruction_set

# A sample program to test translation
PROGRAM = "load x\nadd y\nstore x\nhalt\nx, dec 10\ny, dec 20"


def test_translate_valid_instructions():
    """
    Test the `translate` function with valid instructions.

    Verifies that each instruction in the `instruction_set` is correctly
    translated to its corresponding 4-bit binary representation.
    """
    for instruction, code in instruction_set.items():
        expected_code = format(code, '04b')
        assert translate(instruction) == expected_code


def test_translate_invalid_instruction():
    """
    Test the `translate` function with an invalid instruction.

    Ensures that the function returns `None` for an instruction not found
    in the `instruction_set`.
    """
    assert translate("invalid_instruction") is None


def test_program_translate_instructions():
    """
    Test the translation of instructions in a program.

    Extracts the first word (instruction) from each line of `program2`
    and verifies that it translates correctly if it exists in `instruction_set`.
    """
    instructions = [
        line.split()[0]
        for line in PROGRAM.split("\n")
        if line and line.split()[0] in instruction_set
    ]

    for instruction in instructions:
        assert translate(instruction) == format(instruction_set[instruction], '04b')
