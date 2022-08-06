from sys import stdin

reg_val={'R0':'0'*16, 'R1':'0'*16, 'R2':'0'*16, 'R3':'0'*16, 'R4':'0'*16, 'R5':'0'*16, 'R6':'0'*16, 'FLAGS':'0'*16}  #register values stored in binary form
memory = []
pc = 0

def binary_to_function(opcode):
    dict_opcode = {'add':'10000', 'sub': '10001','movimm':'10010', 'movreg':'10011', 'ld': '10100', 'st': '10101',
         'mul':'10110', 'div':'10111', 'rs':'11000', 'ls':'11001', 'xor':'11010',
         'or':'11011', 'and':'11100', 'not':'11101', 'cmp':'11110', 'jmp':'11111',
         'jlt':'01100', 'jgt':'01101', 'je':'01111','hlt':'01010'}
    for funct, code in dict_opcode.items():
        if code == opcode:
            return funct
def bin_to_reg(binary_no: str)-> int:
    d={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110","FLAGS":"111"}
    for reg in d:
        if d[reg]==binary_no:
            return reg

def bin_to_dec(n:str)->int:
    s0=''
    s=0
    c=0
    s1=n[::-1]
    for i in s1:
        s+=int(i)*(2**c)
        c+=1
    return s

def ld ( ins:str ):
    global reg_val
    global memory
    index = bin_to_dec(ins[-8:-1])
    val = memory [index]
    reg_name = bin_to_reg(ins[5:8])
    reg_val[reg_name] = val
    
def st (ins:str):
    global reg_val
    global memory
    value = reg_val [bin_to_reg(ins[5:8])]
    index = bin_to_dec(ins[-8:-1])
    memory [index] = value

def pcbin(v:int)-> str: # 8-bit binary number is returned
    s0=''
    while v!=0:
        s0+=str(v%2)
        v=v//2
    s=s0[::-1]
    return ('0'*(8-len(s)))+s

def dec_to_bin(v:int)->str: # 16-bit binary number is returned
    s0=''
    while v!=0:
        s0+=str(v%2)
        v=v//2
    s=s0[::-1]
    return ('0'*(16-len(s)))+s


def add(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [7:10])
    sc_reg2_name = bin_to_reg (ins[10:13])
    dest_reg_name = bin_to_reg (ins[13:16])
    
    sc_reg1_DecVal = bin_to_dec (reg_val[sc_reg1_name])
    sc_reg2_DecVal = bin_to_dec (reg_val[sc_reg2_name])
    
    sum_r1_r2 = sc_reg1_DecVal + sc_reg2_DecVal

    if sum_r1_r2 > ((2**16) - 1):
        list_val = list(reg_val['FLAGS'])
        list_val[-4]='1'
        new_flag= ''.join(list_val)
        reg_val['FLAGS'] = new_flag
        reg_val[dest_reg_name] =  dec_to_bin(sum_r1_r2 % (2**16))

    else:
        reg_val[dest_reg_name] = dec_to_bin(sum_r1_r2)


        
def sub(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [7:10])
    sc_reg2_name = bin_to_reg (ins[10:13])
    dest_reg_name = bin_to_reg (ins[13:16])

    sc_reg1_DecVal = bin_to_dec (reg_val[sc_reg1_name])
    sc_reg2_DecVal = bin_to_dec (reg_val[sc_reg2_name])
    
    sub_res = sc_reg1_DecVal - sc_reg2_DecVal

    if sub_res < 0:
        list_val = list(reg_val['FLAGS'])
        list_val[-4]='1'
        new_flag= ''.join(list_val)
        reg_val['FLAGS'] = new_flag
        reg_val[dest_reg_name] = '0'*16

    else:
        reg_val[dest_reg_name] = dec_to_bin(sub_res)

def movimm(ins:str): 
    global reg_val
    reg_name = bin_to_reg(ins[5:8])
    imm_val = ins[-8:]
    reg_val[reg_name] = '0'*8 + imm_val
        
def movreg(ins:str): 
    global reg_val
    dest_reg_name = bin_to_reg(ins[13:16])
    source_reg_name = bin_to_reg(ins[10:13])
    reg_val[dest_reg_name] = reg_val [source_reg_name]
    if source_reg_name != 'FLAGS':
        reg_val['FLAGS'] = '0'*16


def mul(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [7:10])
    sc_reg2_name = bin_to_reg (ins[10:13])
    dest_reg_name = bin_to_reg (ins[13:16])

    sc_reg1_DecVal = bin_to_dec (reg_val[sc_reg1_name])
    sc_reg2_DecVal = bin_to_dec (reg_val[sc_reg2_name])
    
    mul_res = sc_reg1_DecVal * sc_reg2_DecVal

    if mul_res > ((2**6) - 1):
        list_val = list(reg_val['FLAGS'])
        list_val[-4]='1'
        new_flag= ''.join(list_val)
        reg_val['FLAGS'] = new_flag
        reg_val[dest_reg_name] = dec_to_bin(mul_res % (2**16))
        
def div(ins:str):
    global reg_val
    numer_reg_name = bin_to_reg(ins[10:13])
    denom_reg_name = bin_to_reg(ins[13:16])

    numer_val = bin_to_dec ( reg_val[numer_reg_name] )
    denom_val = bin_to_dec ( reg_val[denom_reg_name] )

    reg_val['R0'] = dec_to_bin(numer_val//denom_val) # Quotient
    reg_val['R1'] = dec_to_bin(numer_val % denom_val) # Remainder
    
def ls (ins:str):
    global reg_val
    shift = bin_to_dec(ins[8:16])
    reg_name = bin_to_reg (ins[5:8])
    
    reg_val[reg_name] = reg_val[reg_name][shift : ] + ('0'*shift)

def rs (ins:str):
    global reg_val
    shift = bin_to_dec(ins[8:16]) # decimal value of immediate
    reg_name = bin_to_reg (ins[5:8])
    ind = len(val) - shift
    val = reg_val[reg_name]
    reg_val[reg_name] = '0'*shift + val[:ind]
    
def or_func(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [7:10])
    sc_reg2_name = bin_to_reg (ins[10:13])
    dest_reg_name = bin_to_reg (ins[13:16])

    sc_reg1_Val = bin_to_dec(reg_val[sc_reg1_name])
    sc_reg2_Val = bin_to_dec(reg_val[sc_reg2_name])

    reg_val[dest_reg_name] = dec_to_bin (sc_reg1_Val | sc_reg2_Val)

def xor(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [7:10])
    sc_reg2_name = bin_to_reg (ins[10:13])
    dest_reg_name = bin_to_reg (ins[13:16])

    sc_reg1_Val = bin_to_dec(reg_val[sc_reg1_name])
    sc_reg2_Val = bin_to_dec(reg_val[sc_reg2_name])

    reg_val[dest_reg_name] = dec_to_bin (sc_reg1_Val ^ sc_reg2_Val)

def and_func(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [7:10])
    sc_reg2_name = bin_to_reg (ins[10:13])
    dest_reg_name = bin_to_reg (ins[13:16])

    sc_reg1_Val = bin_to_dec(reg_val[sc_reg1_name])
    sc_reg2_Val = bin_to_dec(reg_val[sc_reg2_name])

    reg_val[dest_reg_name] = dec_to_bin (sc_reg1_Val & sc_reg2_Val)

def not_func(ins:str):
    global reg_val
    sc_reg1_name = bin_to_reg (ins [10:13])
    dest_reg_name = bin_to_reg (ins[-3:])
    l = list(sc_reg1_name)
    result = ['0' if i == '1' else '1' for i in l]
    reg_val[dest_reg_name] = ''.join(result)
    
def cmp (ins:str):
    global reg_val
    reg1_name = bin_to_reg (ins[-6:-3])
    reg2_name= bin_to_reg (ins[-3:])

    list_val = list(reg_val['FLAGS'])

    if bin_to_dec(reg_val[reg1_name]) > bin_to_dec(reg_val[reg2_name]):
        list_val[-2]='1'

    elif bin_to_dec(reg_val[reg1_name]) < bin_to_dec(reg_val[reg2_name]):
        list_val[-3]='1'

    else:
        list_val[-1]='1'
        
    new_flag= ''.join(list_val)
    reg_val['FLAGS'] = new_flag
    
def jmp(ins: str):
    global pc
    index = bin_to_dec(ins[-8:])
    pc = index
    
def jlt(ins: str):
    global pc
    index = bin_to_dec(ins[-8:])
    if reg_val['FLAGS'][-3] == '1':
        pc = index
        
def jgt(ins: str):
    global pc
    index = bin_to_dec(ins[-8:])
    if reg_val['FLAGS'][-2] == '1':
        pc = index

def je(ins: str):
    global pc
    index = bin_to_dec(ins[-8:])
    if reg_val['FLAGS'][-1] == '1':
        pc = index
        
def format(program_counter):
    global reg_val
    result = pcbin(program_counter) + ' '
    for reg in reg_val:
        result += reg_val[reg] + ' '
    result = result.strip()
    return result


def main():
    global reg_val
    global pc
    global memory
    

    #instn = ['10010','1000000000001010','1000000000001010','1001000000000001','0101000000000000']
    instn = []

    for line in stdin:
        items = line.rstrip('\r\n')
        if items!=[]:
            instn.append(items)
    
    '''f = open('sample.txt','r')
    for line in f.readlines():
        items = line.rstrip('\r\n')
        if items!=[]:
            instn.append(items)
    f.close()'''

    length = len(instn)
    memory = [] + instn 
    empty = '0'*16
    for i in range(length, 256):
        memory.append(empty)
    
    #print (len(memory))
    # print(memory)
    while True:

        function = binary_to_function(instn[pc][:5])

        check = ['jmp', 'jlt','je','jgt', 'movreg']
        if function not in check:      #  if not a jump instruction reset flags register
            reg_val['FLAGS'] = '0'*16

        if function == 'add':
            add(instn[pc])
            print(format(pc))
            pc += 1
        
        elif function == 'sub':
            sub(instn[pc])
            print(format(pc))
            pc += 1

        
        elif function == 'movimm':
            movimm(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'movreg':
            movreg(instn[pc])
            print(format(pc))
            pc += 1
            
        elif function == 'ld':
            ld(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'st':
            st(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'mul':
            mul(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'div':
            div(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'rs':
            rs(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'ls':
            ls(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'xor':
            xor(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'or':
            or_func(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'and':
            and_func(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'not':
            not_func(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'cmp':
            cmp(instn[pc])
            print(format(pc))
            pc += 1

        elif function == 'jmp':
            jmp(instn[pc])
            print(format(pc))

        elif function == 'jlt':
            jlt(instn[pc])
            print(format(pc))

        elif function == 'jgt':
            jgt(instn[pc])
            print(format(pc))

        elif function == 'je':
            je(instn[pc])
            print(format(pc))

        else:
            print(format(pc))
            for i in memory:
                print(''.join(i))
            return   
  

main()
