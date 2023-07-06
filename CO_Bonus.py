'''
------------ 4 Types of Memory---------------

1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size (depends on CPU)
'''

import math

print("\nQuestion1, Type-1 starts here...\n")

size_of_memory={'kb':(2**10),'kB':(2**13),'Mb':(2**20),'MB':(2**23),'Gb':(2**30),'GB':(2**33),'Tb':(2**40),'TB':(2**43)}
addressing_memory={'bit':1,'nibble':4,'byte':8}

space=input("Please enter the space in memory: ")
support=int(input("Please enter the number of bits the CPU supports: "))
addressing=input("Please enter how the memory is addressed: ").lower()

length_of_instr=int(input("Please enter the length of Instruction in bits: "))
length_of_reg=int(input("Please enter the length of Register in bits: "))


#ISA AND INSRUCTIONS
def Q1_part1(space,addressing):
    global support
    temp=space.split()
    a=temp[0]
    b=temp[1]
    if(addressing in addressing_memory):
        c=size_of_memory[b]
        mul=(int(a)*int(c))/addressing_memory[addressing]
    elif(addressing not in addressing_memory):
        if(b[0]=='k'):
            mul=(int(a)*(2**10)*support)/support
        elif(b[0]=='M'):
            mul=(int(a)*(2**20)*support)/support
        elif(b[0]=='G'):
            mul=(int(a)*(2**30)*support)/support
        elif(b[0]=='T'):
            mul=(int(a)*(2**40)*support)/support
    answer=math.log(mul,2)
    return int(answer)
    
def Q1_part2(x,y,space,addressing):
    return int(x-(y+Q1_part1(space,addressing)))

def Q1_part3(x,y,space,addressing):
    return int(x-(Q1_part2(x,y,space,addressing)+(2*y)))

def Q1_part4(x,y,space,addressing):
    return int(2**(Q1_part2(x,y,space,addressing)))

def Q1_part5(y):
    return int(2**y)

print("\n\nThe Output for the given queries is as given below!\n")
print(f'\nMinimum bits are needed to represent an address in this architecture: {Q1_part1(space,addressing)}')
print(f'\nNumber of bits needed by opcode: {Q1_part2(length_of_instr, length_of_reg,space,addressing)}')
print(f'\nNumber of filler bits in Instruction type 2: {Q1_part3(length_of_instr, length_of_reg,space,addressing)}')
print(f'\nMaximum numbers of instructions this ISA can support: {Q1_part4(length_of_instr, length_of_reg,space,addressing)}')
print(f'\nMaximum number of registers this ISA can support: {Q1_part5(length_of_reg)}')


#SYSTEM ENHANCEMENT
print("\n\nQuestion2, Type-1 starts here...\n")
enhanced=input("Please enter how'd you like to enhance your system (bit/nibble/byte/word): ").lower()
print("\n")
def Q2_type1(x,y,space,addressing):
    temp0=Q1_part1(space,addressing)
    temp=space.split()
    a=temp[0]
    b=temp[-1]
    if(addressing in addressing_memory):
        if(y in addressing_memory):
            c=size_of_memory[b]
            mul=(int(a)*int(c))/addressing_memory[y]
        else:
            c=size_of_memory[b]
            if(b[0]=='k'):
                mul=(int(a)*int(c))/support
            elif(b[0]=='M'):
                mul=(int(a)*int(c))/support
            elif(b[0]=='G'):
                mul=(int(a)*int(c))/support
            elif(b[0]=='T'):
                mul=(int(a)*int(c))/support
    elif(addressing not in addressing_memory):
        if(y in addressing_memory):
            if(b[0]=='k'):
                mul=(int(a)*(2**10)*support)/addressing_memory[y]
            elif(b[0]=='M'):
                mul=(int(a)*(2**20)*support)/addressing_memory[y]
            elif(b[0]=='G'):
                mul=(int(a)*(2**30)*support)/addressing_memory[y]
            elif(b[0]=='T'):
                mul=(int(a)*(2**40)*support)/addressing_memory[y]
    result=math.log(mul,2)
    answer=temp0-result
    f_res= -int(answer)
    if(f_res<0):
        return f'{f_res} ({-f_res} pins saved)!'
    elif(f_res>0):
        return f'{f_res} ({f_res} pins required)!'
    else:
        return f'{f_res} ({f_res} pins saved/required)!'

print(Q2_type1(support,enhanced,space,addressing))


#TYPE-2
print("\n\nQuestion-2, Type-2 starts here...\n")
cpu_bits=int(input("Please enter the number of bits supported by the CPU: "))
addr_pins=int(input("Please enter the total number of address pins: "))
addressing_type=input("Please enter how the memory is addressed: ").lower()

print("\n\nBreakup of Size of Memory:->\n")
def Q2_type2(x,y,z):
    if(z in addressing_memory):
        res=(2**y)*addressing_memory[z]
        answer1=res/(2**3)
        answer2=res/(2**33)
        answer3=res/(2**13)
        answer4=res/(2**23)
        answer5=res/(2**43)
        print(f'Size of memory in Bytes: {float(answer1)} Bytes')
        print(f'Size of memory in kB: {float(answer3)} kB')
        print(f'Size of memory in MB: {float(answer4)} MB')
        print(f'Size of memory in GB: {float(answer2)} GB')
        return f'Size of memory in TB: {float(answer5)} TB\n'
    else:
        res=(2**y)*x
        answer1=res/(2**3)
        answer2=res/(2**33)
        answer3=res/(2**13)
        answer4=res/(2**23)
        answer5=res/(2**43)
        print(f'Size of memory in Bytes: {float(answer1)} Bytes')
        print(f'Size of memory in kB: {float(answer3)} kB')
        print(f'Size of memory in MB: {float(answer4)} MB')
        print(f'Size of memory in GB: {float(answer2)} GB')
        return f'Size of memory in TB: {float(answer5)} TB\n'
    
print(Q2_type2(cpu_bits,addr_pins,addressing_type))