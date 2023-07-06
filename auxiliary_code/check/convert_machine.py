from globals import *


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
