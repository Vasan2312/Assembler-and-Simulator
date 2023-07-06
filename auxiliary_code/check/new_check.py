import sys

opcode = {
    'var': {'type': 'var'},
    'sub': {'opcode': '00001',
            'type': 'A'},
    'add': {'opcode': '00000',
            'type': 'A'},
    'mov': {'opcode': '00011',
            'type': 'C'},
    'ld':  {'opcode': '00100',
            'type': 'D'},
    'st':  {'opcode': '00101',
            'type': 'D'},
    'mul': {'opcode': '00110',
            'type': 'A'},
    'div': {'opcode': '00111',
            'type': 'C'},
    'rs':  {'opcode': '01000',
            'type': 'B'},
    'ls':  {'opcode': '01001',
            'type': 'B'},
    'xor': {'opcode': '01010',
            'type': 'A'},
    'or':  {'opcode': '01011',
            'type': 'A'},
    'and': {'opcode': '01100',
            'type': 'A'},
    'not': {'opcode': '01101',
            'type': 'C'},
    'cmp': {'opcode': '01110',
            'type': 'C'},
    'jmp': {'opcode': '01111',
            'type': 'E'},
    'jlt': {'opcode': '10000',
            'type': 'E'},
    'jgt': {'opcode': '10001',
            'type': 'E'},
    'je':  {'opcode': '10010',
            'type': 'E'},
    'hlt': {'opcode': '10011',
            'type': 'F'}
}

reg = {
    'R0':    {'addr': '000',
              'data': 0},
    'R1':    {'addr': '001',
              'data': 0},
    'R2':    {'addr': '010',
              'data': 0},
    'R3':    {'addr': '011',
              'data': 0},
    'R4':    {'addr': '100',
              'data': 0},
    'R5':    {'addr': '101',
              'data': 0},
    'R6':    {'addr': '110',
              'data': 0},
    'FLAGS': {'addr': '111',
              'data': [0 for i in range(16)]}
}

instr_length = {
    'var': 2,
    'A': 4,
    'B': 3,
    'C': 3,
    'D': 3,
    'E': 2,
    'F': 1,

}

errors = {'0': 'Instruction Name is Invalid!',
          '1': 'Register Name is Invalid!',
          '2': 'Punctuation Error (except ":" and "$")!',
          '3': '"$" symbol in Instruction (other than type B)!',
          '4': '"$" symbol is not followed by an immediate numerical value!',
          '5': 'Label is empty!',
          '6': 'Variables not declared at Beginning!',
          '7': 'Variables not defined!',
          '8': 'Labels not defined!',
          '9': 'Redefining Labels (changing already defined labels)!',
          '10': 'Redefining Variables (changing pre-existing variables)!',
          '11': 'Illegal Interchange of Labels and Variables!',
          '12': 'Illegal use of Flags!',
          '13': 'Immediate Value is not an Integer(Whole Number)!',
          '14': 'Immediate Value is not in range [0,255]',
          '15': 'Halt Instruction is called In-between the program!',
          '16': 'Halt instruction not at last line!',
          '17': '":" in wrong position in definition of Labels!',
          '18': 'No. of parameters not valid!',
          '20': '"$" missing in definition of immediate!',
          'general': 'general syntax error'}

variables = dict()
labels = dict()
instructions = []

counter_raw = 0     # first incre to begin from line 1
pc = 0

# pc changes after exec of instr => pc shows current line index, not that of next line

var_flag = 1
error_flag = False


def converter(num1, A=10, B=2):
    tot = 0
    digit = [i for i in num1]
    digit.reverse()
    for val in range(len(digit)):
        if digit[val].isalpha():
            pos = ord(digit[val]) - 55
            tot += (A**val)*pos
        else:
            tot += int(digit[val])*(A**val)
    l = []
    a2 = tot
    while a2 > 0:
        a1 = tot % B
        a2 = tot//B
        tot = a2
        l.append(a1)
    l2 = []
    for converter in l:
        if converter > 9:
            l2.append(chr(converter-10 + 65))
        else:
            l2.append(converter)
    l2 = [str(num1) for num1 in l2]
    l2.reverse()
    finalnum = "".join(l2)
    return finalnum


def Addition(given_list: list):
    opcode1 = opcode['add']['opcode']
    unused = '00'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    reg3 = reg[given_list[2]]['addr']
    final = opcode1 + unused + reg1 + reg2 + reg3
    return final


def Subtraction(given_list: list):
    opcode1 = opcode['sub']['opcode']
    unused = '00'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    reg3 = reg[given_list[2]]['addr']
    final = opcode1 + unused + reg1 + reg2 + reg3
    return final


def MoveImmediate(given_list: list):
    opcode1 = '00010'
    reg1 = reg[given_list[0]]['addr']
    imm = (given_list[1][1:])
    new = converter(imm)
    left = 8-len(new)
    unused = ''
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + reg1 + unused + new
    return final


def MoveRegister(given_list: list):
    opcode1 = opcode['mov']['opcode']
    unused = '00000'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    final = opcode1 + unused + reg1 + reg2
    return final


def Multiply(given_list: list):
    opcode1 = opcode['mul']['opcode']
    unused = '00'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    reg3 = reg[given_list[2]]['addr']
    final = opcode1 + unused + reg1 + reg2 + reg3
    return final


def Divide(given_list: list):
    opcode1 = opcode['div']['opcode']
    unused = '00000'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    final = opcode1 + unused + reg1 + reg2
    return final


def Rightshift(given_list: list):
    opcode1 = opcode['rs']['opcode']
    reg1 = reg[given_list[0]]['addr']
    imm = (given_list[1][1:])
    new = converter(imm)
    left = 8-len(new)
    unused = ''
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + reg1 + unused + new
    return final


def Leftshift(given_list: list):
    opcode1 = opcode['ls']['opcode']
    reg1 = reg[given_list[0]]['addr']
    imm = (given_list[1][1:])
    new = converter(imm)
    left = 8-len(new)
    unused = ''
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + reg1 + unused + new
    return final


def Exclusiveor(given_list: list):
    opcode1 = opcode['xor']['opcode']
    unused = '00'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    reg3 = reg[given_list[2]]['addr']
    final = opcode1 + unused + reg1 + reg2 + reg3
    return final


def Or(given_list: list):
    opcode1 = opcode['or']['opcode']
    unused = '00'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    reg3 = reg[given_list[2]]['addr']
    final = opcode1 + unused + reg1 + reg2 + reg3
    return final


def And(given_list: list):
    opcode1 = opcode['and']['opcode']
    unused = '00'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    reg3 = reg[given_list[2]]['addr']
    final = opcode1 + unused + reg1 + reg2 + reg3
    return final


def Invert(given_list: list):
    opcode1 = opcode['not']['opcode']
    unused = '00000'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    final = opcode1 + unused + reg1 + reg2
    return final


def Compare(given_list: list):
    opcode1 = opcode['cmp']['opcode']
    unused = '00000'
    reg1 = reg[given_list[0]]['addr']
    reg2 = reg[given_list[1]]['addr']
    final = opcode1 + unused + reg1 + reg2
    return final


def Load(given_list: list, memory):
    opcode1 = opcode['ld']['opcode']
    reg1 = reg[given_list[0]]['addr']
    left = 8-len(memory)
    unused = ''
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + reg1 + unused + memory
    return final


def Store(given_list: list, memory):
    opcode1 = opcode['st']['opcode']
    reg1 = reg[given_list[0]]['addr']
    left = 8-len(memory)
    unused = ''
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + reg1 + unused + memory
    return final


def UnconditionalJump(given_list: list, memory):
    opcode1 = opcode['jmp']['opcode']
    unused = '000'
    left = 8-len(memory)
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + unused + memory
    return final


def JumpIfLessThan(given_list: list, memory):
    opcode1 = opcode['jlt']['opcode']
    unused = '000'
    left = 8-len(memory)
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + unused + memory
    return final


def JumpIfgreaterThan(given_list: list, memory):
    opcode1 = opcode['jgt']['opcode']
    unused = '000'
    left = 8-len(memory)
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + unused + memory
    return final


def JumpIfEqual(given_list: list, memory):
    opcode1 = opcode['je']['opcode']
    unused = '000'
    left = 8-len(memory)
    for i in range(left):
        unused = unused + '0'
    final = opcode1 + unused + memory
    return final


def halt():
    return '1001100000000000'


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
