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
    'r0':    {'addr': '000',
              'data': 0},
    'r1':    {'addr': '001',
              'data': 0},
    'r2':    {'addr': '010',
              'data': 0},
    'r3':    {'addr': '011',
              'data': 0},
    'r4':    {'addr': '100',
              'data': 0},
    'r5':    {'addr': '101',
              'data': 0},
    'r6':    {'addr': '110',
              'data': 0},
    'flags': {'addr': '111',
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
          '3': 'Illegal use of "$" symbol',
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
          '19': 'Illegal use of keyword',
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

err_lines = []
