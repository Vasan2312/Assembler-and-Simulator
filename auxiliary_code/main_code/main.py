import sys
from globals import *
from print_machine import *


def has_length_or_name_error(line):
    if line[0] in opcode:
        instr = line[0]

        if len(line) != instr_length[opcode[instr]['type']]:
            print(f'ERROR: (Line {counter_raw})', errors['18'])
            err_lines.append(counter_raw)
            return True

        else:
            return False

    else:
        if '\t' in ' '.join(line):
            print(f'ERROR: (Line {counter_raw})', errors['general'])
            err_lines.append(counter_raw)
            return True

        # print(line[0])
        print(f'ERROR: (Line {counter_raw})', errors['0'])
        err_lines.append(counter_raw)
        return True


def is_register(param):
    global reg

    if param in reg:
        return True
    else:
        return False


def is_flags(param):
    if param == 'FLAGS'.lower():
        return True
    else:
        return False


def has_var_error(v):
    if v in variables:
        return False

    else:
        if v in labels:
            print(f'ERROR: (Line {counter_raw})', errors['11'])
            err_lines.append(counter_raw)
            return True
        else:
            print(f'ERROR: (Line {counter_raw})', errors['7'])
            err_lines.append(counter_raw)
            return True


def has_label_error(l):
    if l in labels:
        return False

    else:
        if l in variables:
            print(f'ERROR: (Line {counter_raw})', errors['11'])
            err_lines.append(counter_raw)
            return True
        else:
            print(f'ERROR: (Line {counter_raw})', errors['8'])
            err_lines.append(counter_raw)
            return True


def has_imm_error(arg: str):
    if '$' not in arg:                  # arg must have $
        print(f'ERROR: (Line {counter_raw})', errors['20'])
        err_lines.append(counter_raw)
        return True

    if '$' != arg[0]:                      # $ must be first symbol
        print(f'ERROR: (Line {counter_raw})', errors['3'])
        err_lines.append(counter_raw)
        return True

    if len(arg) <= 1:                   # imm empty
        print(f'ERROR: (Line {counter_raw})', errors['4'])
        err_lines.append(counter_raw)
        return True

    imm: str = arg[1:]

    if not imm.isdigit():                # imm must be int
        print(f'ERROR: (Line {counter_raw})', errors['13'])
        err_lines.append(counter_raw)
        return True

    try:
        imm = int(imm)
    except Exception:
        print(f'ERROR: (Line{counter_raw})', errors['general'])
        err_lines.append(counter_raw)
        return True

    if imm > 255 or imm < 0:            # imm out of range
        print(f'ERROR: (Line {counter_raw})', errors['14'])
        err_lines.append(counter_raw)
        return True

    return False


def has_param_error(instr, param_list):
    type = opcode[instr]['type']

    if instr == 'mov' and '$' in ' '.join(param_list):
        type = chr(ord(type)-1)

    if type == 'A':

        for arg in param_list:
            if is_register(arg):
                if is_flags(arg):               # illegal use of flags
                    print(f'ERROR: (Line {counter_raw})', errors['12'])
                    err_lines.append(counter_raw)
                    return True

                else:
                    pass

            else:                               # arg must be a reg
                print(f'ERROR: (Line {counter_raw})', errors['1'])
                err_lines.append(counter_raw)
                return True

        return False

# ----------------------------------------------------------------------------------------

    elif type == 'B':

        arg1 = param_list[0]
        arg2 = param_list[1]

        if not is_register(arg1):               # arg1 must be reg
            print(f'ERROR: (Line {counter_raw})', errors["1"])
            err_lines.append(counter_raw)
            return True

        if is_flags(arg1):                      # illegal use of flags
            print(f'ERROR: (Line {counter_raw})', errors['12'])
            err_lines.append(counter_raw)
            return True

        # check if imm is correct
        if has_imm_error(arg2):
            return True

        return False

# ----------------------------------------------------------------------------------------

    elif type == 'C':

        if instr == 'mov':
            for arg in param_list:
                if not is_register(arg):         # all args must be regs
                    print(f'ERROR: (Line {counter_raw})', errors["1"])
                    err_lines.append(counter_raw)
                    return True

            arg2 = param_list[1]

            if is_flags(arg2):                   # FLAGS must be arg1 in mov
                print(f'ERROR: (Line {counter_raw})', errors['12'])
                err_lines.append(counter_raw)
                return True

        else:
            for arg in param_list:               # all args must be regs
                if not is_register(arg):
                    print(f'ERROR: (Line {counter_raw})', errors["1"])
                    err_lines.append(counter_raw)
                    return True

                if is_flags(arg):                # illegal use of flags
                    print(f'ERROR: (Line {counter_raw})', errors['12'])
                    err_lines.append(counter_raw)
                    return True

        return False

# ----------------------------------------------------------------------------------------

    elif type == 'D':

        arg1 = param_list[0]
        arg2 = param_list[1]

        if not is_register(arg1):               # arg1 must be reg
            print(f'ERROR: (Line {counter_raw})', errors["1"])
            err_lines.append(counter_raw)
            return True

        if is_flags(arg1):                      # illegal use of flags
            print(f'ERROR: (Line {counter_raw})', errors['12'])
            err_lines.append(counter_raw)
            return True

        if has_var_error(arg2):                   # check if var is correct
            return True

        return False

# ----------------------------------------------------------------------------------------

    elif type == 'E':

        arg = param_list[0]
        if has_label_error(arg):                  # check if label is correct
            return True

        return False


def err_check(line):
    global counter_raw, pc, var_flag, err_lines, l_arr

    if line == '':
        return False

    line = line.split()

    # Var check
    if line[0] == 'var':

        if var_flag == 0:
            print(f'ERROR: (Line {counter_raw})', errors['6'])
            err_lines.append(counter_raw)
            return True

        else:
            if len(line) == 2:        # Var check
                var_name = line[1]

                if var_name in opcode or var_name in reg:       # Var must not be keyword
                    print(f'ERROR: (Line {counter_raw})', errors['19'])
                    err_lines.append(counter_raw)
                    return True

                if var_name in variables:                   # Redefine var
                    print(f'ERROR: (Line {counter_raw})', errors['10'])
                    err_lines.append(counter_raw)
                    return True

                if var_name in labels:                      # Interchange of labels and vars
                    print(f'ERROR: (Line {counter_raw})', errors['11'])
                    err_lines.append(counter_raw)
                    return True

                variables[line[1]] = 0
                return False

            else:
                print(f'ERROR: (Line {counter_raw})', errors['general'])
                err_lines.append(counter_raw)
                return True

    if 'var' in line[0]:
        print(f'ERROR: (Line {counter_raw})', errors['general'])
        err_lines.append(counter_raw)
        return True

    var_flag = 0
    label_name = ''

    # Label check
    if ':' in ' '.join(line):
        
        ''' 
        if ':' != line[0][-1]:
            print(f'ERROR: (Line {counter_raw})', errors['17'])
            err_lines.append(counter_raw)
            return True                                    # : at wrong pos

        if ':' in ' '.join(line[1:]):
            print(f'ERROR: (Line {counter_raw})', errors['9'])
            err_lines.append(counter_raw)
            return True                                    # label redefined

        if len(line[0]) <= 1:
            print(f'ERROR: (Line {counter_raw})', errors['8'])
            err_lines.append(counter_raw)
            return True                                    # empty label
        '''
        
        label_name = line[0][:-1]

        if label_name in opcode or label_name in reg:       # label must not be keyword
            print(f'ERROR: (Line {counter_raw})', errors['19'])
            err_lines.append(counter_raw)
            l_arr.remove(label_name)
            return True

        if len(line) == 1:                                   # Empty label
            print(f'ERROR: (Line {counter_raw})', errors['5'])
            err_lines.append(counter_raw)
            l_arr.remove(label_name)
            return True

        if label_name in l_arr:                            # Redefine labels
            if label_name not in labels:
                labels[label_name] = 0
            
            else:
                print(f'ERROR: (Line{counter_raw})', errors['9'])
                err_lines.append(counter_raw)
                l_arr.remove(label_name)
                return True

        line = line[1:]

    if has_length_or_name_error(line):
        labels.pop(label_name)
        return True

    if has_param_error(line[0], line[1:]):
        labels.pop(label_name)
        return True

    if label_name:
        labels[label_name] = pc

    instructions.append(line)
    pc += 1
    return False


def main():
    prog = [i.strip().lower() for i in sys.stdin.read().split('\n')]
    print()     # Comment for final run

    global counter_raw, pc, error_flag, err_lines, l_arr
    error_flag = False

    for line in prog:
        counter_raw += 1
        line1 = line.split()

        # Adding Labels

        if line1 != []:
            if (line1[0] == 'var'):
                pass

            else:
                if line1[0].count(':') > 1:
                    print(f'ERROR: (Line{counter_raw})', errors['17'])
                    err_lines.append(counter_raw)
                    error_flag = True

                elif line1[0][-1] == ':':
                    if len(line1[0]) <= 1:
                        print(f'ERROR: (Line {counter_raw})', errors['8'])
                        err_lines.append(counter_raw)
                        error_flag = True

                    else:
                        l_arr.append(line1[0][:-1])

                #pc += 1

    counter_raw = 0
    pc = 0

    # Error check

    for line in prog:
        counter_raw += 1

        if err_check(line):
            error_flag = True
            continue

    # Set var values

    for v in variables:
        variables[v] = pc
        pc += 1

    # Check halt errors

    if instructions:
        halt_idx_list = [
            i+1 for i, line in enumerate(prog) if 'hlt' in line and i+1 not in err_lines]

        if instructions[-1] != ['hlt']:
            print(f'ERROR:', errors['16'])
            error_flag = True

            if halt_idx_list:
                for i in halt_idx_list:
                    print(f'ERROR: (Line {i})', errors['15'])
                    error_flag = True

        else:
            if halt_idx_list:
                for i in halt_idx_list[:-1]:
                    print(f'ERROR: (Line {i})', errors['15'])
                    error_flag = True

    else:
        print(f'ERROR:', errors['16'])
        error_flag = True

    print_binary(error_flag)
    print()


main()
