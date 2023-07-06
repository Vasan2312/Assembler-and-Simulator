import sys
from math import pow
# from sim_func1 import *

opcode = {
    '00001': {'key': 'sub',
              'type': 'a'},
    '00000': {'key': 'add',
              'type': 'a'},
    '00011': {'key': 'movr',
              'type': 'c'},
    '00010': {'key': 'movi',
              'type': 'b'},
    '00100':  {'key': 'ld',
               'type': 'd'},
    '00101':  {'key': 'st',
               'type': 'd'},
    '00110': {'key': 'mul',
              'type': 'a'},
    '00111': {'key': 'div',
              'type': 'c'},
    '01000':  {'key': 'rs',
               'type': 'b'},
    '01001':  {'key': 'ls',
               'type': 'b'},
    '01010': {'key': 'xor',
              'type': 'a'},
    '01011':  {'key': 'or',
               'type': 'a'},
    '01100': {'key': 'and',
              'type': 'a'},
    '01101': {'key': 'not',
              'type': 'c'},
    '01110': {'key': 'cmp',
              'type': 'c'},
    '01111': {'key': 'jmp',
              'type': 'e'},
    '10000': {'key': 'jlt',
              'type': 'e'},
    '10001': {'key': 'jgt',
              'type': 'e'},
    '10010':  {'key': 'je',
               'type': 'e'},
    '10011': {'key': 'hlt',
              'type': 'f'}
}

reg_convert = {
    '000': 'r0',
    '001': 'r1',
    '010': 'r2',
    '011': 'r3',
    '100': 'r4',
    '101': 'r5',
    '110': 'r6',
    '111': 'flags'
}

reg_data = {
    'r0': 0,
    'r1': 0,
    'r2': 0,
    'r3': 0,
    'r4': 0,
    'r5': 0,
    'r6': 0,
    'flags': [0 for i in range(16)]
}

unused_bits = {
    'a': 2,
    'b': 0,
    'c': 5,
    'd': 0,
    'e': 3,
    'f': 11
}

memory = [0 for i in range(256)]

halted = False
pc = 0

overflow_flag_pos = -4
less_flag_pos = -3
greater_flag_pos = -2
equal_flag_pos = -1


def reset_flags():
    reg_data['flags'][-1] = 0
    reg_data['flags'][-2] = 0
    reg_data['flags'][-3] = 0
    reg_data['flags'][-4] = 0


def set_overflow_flag():
    reset_flags()
    reg_data['flags'][overflow_flag_pos] = 1


def set_less_flag():
    reset_flags()
    reg_data['flags'][less_flag_pos] = 1


def set_greater_flag():
    reset_flags()
    reg_data['flags'][greater_flag_pos] = 1


def set_equal_flag():
    reset_flags()
    reg_data['flags'][equal_flag_pos] = 1


def Addition(reg1, reg2, reg3):
    global reg_data

    src1 = reg_data[reg2]
    src2 = reg_data[reg3]

    if src1 + src2 > int(pow(2, 16))-1:
        set_overflow_flag()
        reg_data[reg1] = int(format(src1 + src2, '0b')[-16:], 2)

    else:
        reg_data[reg1] = src1 + src2
        reset_flags()


def Subtraction(reg1, reg2, reg3):
    src1 = reg_data[reg2]
    src2 = reg_data[reg3]

    if src2 > src1:
        set_overflow_flag()
        reg_data[reg1] = 0

    else:
        reg_data[reg1] = src1 - src2
        reset_flags()


def Multiply(reg1, reg2, reg3):
    src1 = reg_data[reg2]
    src2 = reg_data[reg3]

    if src1 * src2 > int(pow(2, 16))-1:
        set_overflow_flag()
        reg_data[reg1] = int(format(src1 * src2, '0b')[-16:], 2)

    else:
        reg_data[reg1] = src1 * src2
        reset_flags()


def Xor(reg1, reg2, reg3):
    reg_data[reg1] = reg_data[reg2] ^ reg_data[reg3]
    reset_flags()


def Or(reg1, reg2, reg3):
    reg_data[reg1] = reg_data[reg2] | reg_data[reg3]
    reset_flags()


def And(reg1, reg2, reg3):
    reg_data[reg1] = reg_data[reg2] & reg_data[reg3]
    reset_flags()


def Movi(reg, imm):
    reg_data[reg] = imm
    reset_flags()


def LeftShift(reg, imm):
    reg_data[reg] <<= imm
    reset_flags()


def RightShift(reg, imm):
    reg_data[reg] >>= imm
    reset_flags()


def Movr(reg1, reg2):
    if reg2 == 'flags':
        reg_data[reg1] = int(''.join([str(i) for i in reg_data[reg2]]), 2)

    else:
        reg_data[reg1] = reg_data[reg2]

    reset_flags()


def Div(reg1, reg2):
    reset_flags()

    if reg_data[reg2] != 0:
        reg_data['r0'] = reg_data[reg1]//reg_data[reg2]
        reg_data['r1'] = reg_data[reg1] % reg_data[reg2]
    else:
        pass


def Not(reg1, reg2):
    a = format(reg_data[reg2], '016b')
    st = ''
    for i in a:
        if i == '0':
            st += '1'
        elif i == '1':
            st += '0'

    reg_data[reg1] = int(st, 2)
    reset_flags()


def Cmp(reg1, reg2):
    if(reg_data[reg1] == reg_data[reg2]):
        set_equal_flag()

    elif(reg_data[reg1] > reg_data[reg2]):
        set_greater_flag()

    elif(reg_data[reg1] < reg_data[reg2]):
        set_less_flag()


def Load(reg, addr):
    reg_data[reg] = memory[addr]
    reset_flags()


def Store(reg, addr):
    memory[addr] = reg_data[reg]
    reset_flags()


def execute_a(instr, reg1, reg2, reg3):
    if instr == 'add':
        Addition(reg1, reg2, reg3)

    elif instr == 'sub':
        Subtraction(reg1, reg2, reg3)

    elif instr == 'mul':
        Multiply(reg1, reg2, reg3)

    elif instr == 'xor':
        Xor(reg1, reg2, reg3)

    elif instr == 'or':
        Or(reg1, reg2, reg3)

    elif instr == 'and':
        And(reg1, reg2, reg3)

    return


def execute_b(instr, reg, imm):
    if instr == 'movi':
        Movi(reg, imm)

    elif instr == 'ls':
        LeftShift(reg, imm)

    elif instr == 'rs':
        RightShift(reg, imm)


def execute_c(instr, reg1, reg2):
    if instr == 'movr':
        Movr(reg1, reg2)

    elif instr == 'div':
        Div(reg1, reg2)

    elif instr == 'not':
        Not(reg1, reg2)

    elif instr == 'cmp':
        Cmp(reg1, reg2)

    return True


def execute_d(instr, memory_addr, reg1):
    global memory

    if instr == 'ld':
        Load(reg1, memory_addr)

    elif instr == 'st':
        Store(reg1, memory_addr)

    return True


def execute_e(instr, label):
    pc_temp = -1

    if instr == 'jmp':
        pc_temp = label-1

    elif instr == 'jlt':
        if (reg_data['flags'][less_flag_pos] == 1):
            pc_temp = label-1

    elif instr == 'jgt':
        if (reg_data['flags'][greater_flag_pos] == 1):
            pc_temp = label-1

    elif instr == 'je':
        if (reg_data['flags'][equal_flag_pos] == 1):
            pc_temp = label-1

    reset_flags()
    return pc_temp


data = sys.stdin.read().split()

while True:
    pc_temp = -1

    if halted:
        break

    line = data[pc]
    instr = opcode[line[:5]]['key']
    encode_type = opcode[line[:5]]['type']
    # print(encode_type)

    if encode_type == 'a':
        reg1 = reg_convert[line[7:10]]
        reg2 = reg_convert[line[10:13]]
        reg3 = reg_convert[line[13:]]
        execute_a(instr, reg1, reg2, reg3)

    elif encode_type == 'b':
        reg = reg_convert[line[5:8]]
        imm = int(line[8:], 2)
        execute_b(instr, reg, imm)

    elif encode_type == 'c':
        reg1 = reg_convert[line[10:13]]
        reg2 = reg_convert[line[13:]]
        execute_c(instr, reg1, reg2)

    elif encode_type == 'd':
        reg = reg_convert[line[5:8]]
        addr = int(line[8:], 2)
        execute_d(instr, addr, reg)

    elif encode_type == 'e':
        label = int(line[8:], 2)
        pc_temp = execute_e(instr, label)

    elif encode_type == 'f':
        halted = True
        reset_flags()

    print(format(pc, '08b'), end=' ')

    for i in range(7):
        print(format(reg_data[f'r{i}'], "016b"), end=' ')

    print(''.join([str(i) for i in reg_data['flags']]))

    if pc_temp != -1:
        pc = pc_temp
    pc += 1

for line in data:
    print(line)

for i in range(pc, 256):
    print(format(memory[i], "016b"))
