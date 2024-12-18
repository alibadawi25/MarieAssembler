import pytest
from test import programReader, programTranslator
from AssemblyToMachineCodeTranslator import translate, instructionSet

program2 = "load x\nadd y\nstore x\nhalt\nx, dec 10\ny, dec 20"


def test_translate_valid_instructions():
    for instruction, code in instructionSet.items():
        expected_code = format(code, '04b')
        assert translate(instruction) == expected_code


def test_translate_invalid_instruction():
    assert translate("invalid_instruction") is None


def test_program_translate_instructions():
    instructions = [line.split()[0] for line in program2.split("\n") if line and line.split()[0] in instructionSet]

    for instruction in instructions:
        assert translate(instruction) == format(instructionSet[instruction], '04b')
