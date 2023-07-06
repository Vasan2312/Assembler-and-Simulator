from globals import *
from convert_machine import *


def print_binary(error_flag):
    if not error_flag:

        for line in instructions:

            if line[0] == 'add':
                print(Addition(line[1:]))

            elif line[0] == 'sub':
                print(Subtraction(line[1:]))

            elif line[0] == 'mov' and '$' in line[2]:
                print(MoveImmediate(line[1:]))

            elif line[0] == 'mov':
                print(MoveRegister(line[1:]))

            elif line[0] == 'mul':
                print(Multiply(line[1:]))

            elif line[0] == 'div':
                print(Divide(line[1:]))

            elif line[0] == 'rs':
                print(Rightshift(line[1:]))

            elif line[0] == 'ls':
                print(Leftshift(line[1:]))

            elif line[0] == 'xor':
                print(Exclusiveor(line[1:]))

            elif line[0] == 'or':
                print(Or(line[1:]))

            elif line[0] == 'and':
                print(And(line[1:]))

            elif line[0] == 'not':
                print(Invert(line[1:]))

            elif line[0] == 'cmp':
                print(Compare(line[1:]))

            elif line[0] == 'ld':
                print(Load(line[1:], converter(str(variables[line[2]]))))

            elif line[0] == 'st':
                print(Store(line[1:], converter(str(variables[line[2]]))))

            elif line[0] == 'jmp':
                print(UnconditionalJump(
                    line[1:], converter(str(labels[line[1]]))))

            elif line[0] == 'jlt':
                print(JumpIfLessThan(line[1:], converter(
                    str(labels[line[1]]))))

            elif line[0] == 'jgt':
                print(JumpIfgreaterThan(
                    line[1:], converter(str(labels[line[1]]))))

            elif line[0] == 'je':
                print(JumpIfEqual(line[1:], converter(
                    str(labels[line[1]]))))

            elif line[0] == 'hlt':
                print('1001100000000000')
