from sys import stdin

def imm_to_bin(v:int)-> str:
    try:
        assert v>=0 and v<=(2**8-1)
        s0=''
        while v!=0:
            s0+=str(v%2)
            v=v//2
        s=s0[::-1]
        return ('0'*(8-len(s)))+s
    except:
        return 'I'


def frac_of(v:float)-> float:
    int_part = int(v)
    numofdig_intpart = len(str(int_part))
    frac_part = float(str(v)[numofdig_intpart:])
    return frac_part


def float_to_bin(v:float) -> str:
    int_part = int(v)
    fraction_part = frac_of(v)
    int_bin = imm_to_bin(int_part)
    frac_bin = ''   
    while frac_of(fraction_part):
        fraction_part *= 2
        bit = int(fraction_part)
        if (bit == 1) :   
            fraction_part -= bit  
            frac_bin += '1'
        else : 
            frac_bin += '0'
    return str(int(int_bin)) + '.'+ frac_bin



def binfloat_to_regformat(binum:str)->str:
    result = ''
    if len(binum)<= 7:
        lst = list(binum)
        orig_decimal_index = lst.index('.')
        left_shift = orig_decimal_index -1
        exponent = left_shift
        if exponent >7 or exponent<0:
            return 'invalid'
        bin_exponent = '0'*(3-len(str(int(imm_to_bin(exponent))))) + str(int(imm_to_bin(exponent)))
        lst.pop(0)
        bin_mantissa = ''.join(lst)
        bin_mantissa = bin_mantissa.replace('.','')   
        return bin_exponent + bin_mantissa + '0'*(5-len(bin_mantissa))
    else:
        return 'invalid'

def opcode_to_binary(opcode, typ):
    dict_opcode = {'add':'10000','addf':'00000', 'sub': '10001','subf':'00001',
                   'ld': '10100', 'st': '10101','mul':'10110', 'div':'10111',
                   'rs':'11000', 'ls':'11001', 'xor':'11010','or':'11011',
                   'and':'11100', 'not':'11101', 'cmp':'11110', 'jmp':'11111',
                   'jlt':'01100', 'jgt':'01101', 'je':'01111','hlt':'01010'}
    if opcode in dict_opcode:
        return dict_opcode[opcode]    
    elif opcode == 'mov' and typ == 'B':
        return '10010'
    elif opcode == 'movf' and typ == 'B':
        return '00010'
    elif opcode == 'mov' and typ == 'C':
        return '10011'
    else:
        return 'O' 

def errors(symbol,pc):
    dict_errors = {'O':'ERROR: Undefined Instruction Name',
                   'R': 'ERROR: Undefined Register Name',
                   'V': 'ERROR: Use of Undefined Variables',
                   'L': 'ERROR: Use of Undefined Labels',
                   'I': 'ERROR: Illegal Immediate Values(more than 8 bits)',
                   'i': 'ERROR: Incorrect Immediate Value',
                   'M': 'ERROR: Misuse of Labels as Variables or vice-versa',
                   'VB': 'ERROR: Variable not Declared in the Beginning',
                   'T': 'ERROR: Type Error - No such Type exists',
                   'H': 'ERROR: Halt Instruction Missing',
                   'HL': 'ERROR: Halt Not Used as Last Instruction',
                   'G': 'ERROR: General Syntax Error'}
    if symbol in dict_errors:
        return('@Line:'+str(pc+1)+' '+dict_errors[symbol])

def imm_to_bin(v:int)-> str:
    try:
        assert v>=0 and v<=(2**8-1) 
        s0=''
        while v!=0:
            s0+=str(v%2)
            v=v//2
        s=s0[::-1]
        return ('0'*(8-len(s)))+s
    except:
        return 'I'



def reg_to_bin(reg)-> str:
    d={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110","FLAGS":"111"}
    if reg in d:
        return(d[reg])
    return('R')

def var_to_addr(var_list, l):
    d = {}
    for var in var_list:
        imm = imm_to_bin(l)
        d[var] = imm
        l += 1
    return d

def typ (ins: list) :
    typA = ['add', 'sub', 'mul', 'xor', 'and', 'or', 'addf', 'subf']
    typB = ['ls','rs', 'movf']
    typD = ['ld','st']
    typC=['not', 'cmp','div']
    typE=['jmp','jlt', 'jgt','je']

    if len(ins)>4:
        return 'T'
    
    if ins[0]=='hlt':
        return 'F'

    if ins[0] in typA:
        if len(ins)==4:
            return 'A'
        else:
            return 'T'
    
    elif ins[0]=='mov' and len(ins)==3:
        if ins[2][0]=='$':
            return 'B'
        else:
            try:
                a=int(ins[2])
                return 'B'
            except:
                return 'C'

    elif ins[0] in typB:
        if len(ins)==3:
            return 'B'
        else:
            return 'T'
    
    elif ins[0] in typC:
        if len(ins)==3:
            return 'C'
        else:
            return 'T'
    
    elif ins[0] in typD:
        if len(ins)==3:
            return 'D'
        else:
            return 'T'
    
    elif ins[0] in typE:
        if len(ins)==2:
            return 'E'
        else:
            return 'T'

    return 'T'

# MAIN CODE:
output=''
def main():
    global output
    try:

        #l = [['add','R1','R2','R3'], ['addf','R1','R2','R3'],['subf','R1','R2','R3'],['label:']] 
        l=[]
        for line in stdin:
            items = line.rstrip('\r\n').split('\t') 
            items = [item.strip() for item in items]  
            items = items[0].split()
            if items!=[]:
                l.append(items)
        '''l=[]
        f = open('sample.txt','r')
        for line in f.readlines():
            items = line.rstrip('\r\n').split('\t') 
            items = [item.strip() for item in items]  
            items = items[0].split()
            if items!=[]:
                l.append(items)
        f.close()'''
        
        #[label: label2: add R0 R1 R3]
        label_d={}
        for i in l:
            if len(i) != 1:
                str_txt = ''.join(i)
                count_c = str_txt.count(':')
                if count_c > 0:
                    for j in range(count_c):
                        if len(i[j].split())!=1 or i[j][-1]!=':':
                            print('@Line: '+str(l.index(i))+' ERROR: Incorrect Label Name')
                            output+='@Line: '+str(l.index(i))+' ERROR: Incorrect Label Name'
                            return
                        label_d[i[j]] = l.index(i)
                    for k in range(count_c):
                        i.pop(0)
        

        for i in l:
            if len(i)==1 and i!=['hlt']:
                if len(i[0].split())!=1 or i[0][-1]!=':':
                    print('@Line: '+str(l.index(i))+' ERROR: Incorrect Label Name')
                    output+='@Line: '+str(l.index(i))+' ERROR: Incorrect Label Name'
                    return
                else:
                    label_d[i[0]]=l.index(i)


        for label in label_d:
            s = label[:-1]
            if not(s.isalnum()):
                print('@Line: '+str(label_d[label])+' ERROR: Incorrect Label Name')
                output+='@Line: '+str(label_d[label])+' ERROR: Incorrect Label Name'
                return

        for ele in l:
            if 'FLAGS' in ele:
                if typ(ele)!='C':
                    print('@Line'+str(l.index(ele))+' ERROR: Illegal use of FLAGS register')
                    output+='@Line'+str(l.index(ele))+' ERROR: Illegal use of FLAGS register'
                    return
        try:
            var_list=[]
            for f in range(0, len(l)):
                if l[f][0]=='var':
                    var_list.append(l[f][1])
        except:
            print(errors('G',f))
            output+=errors('G',f)
            return
        
    # print('variable= ', var_list)

        j = 0
        while l[j][0] == 'var':
            j += 1

        for v in range(j,len(l)):
            if l[v][0] == 'var':
                print(errors('VB', v))
                output+=errors('VB',v)
                return

        while j>0:
            l.remove(l[0])
            j -= 1

        #check label-variable misuse
        
        for i in l:
            if typ(i)=='E':
                    k=i[1]
                    if k in var_list:
                        print(errors('M',l.index(i)))
                        output+=errors('M',l.index(i))
                        return

        for i in range (0,len(var_list)):
            if var_list[i]+':' in label_d:
                print(errors('M',label_d[var_list[i]+':']))
                output+=errors('M',label_d[var_list[i]+':'])
                return

        
        dict_var = var_to_addr(var_list, len(l))

        pc = 0
        

        if ['hlt'] in l and l.index(['hlt'])<len(l)-1:
            print(errors('HL', l.index(['hlt'])))
            output+=errors('HL', l.index(['hlt']))
            return;
        elif ['hlt'] not in l:
            print(errors('H', len(l)-1))
            output+=errors('H', len(l)-1)
            return;

        
        

        while pc<len(l):
            s=''
            t=typ(l[pc])
            if l[pc][0] not in label_d:
                if t=='T':
                    print(errors(t,pc))
                    output+=errors(t,pc)
                    return
                opc = opcode_to_binary(l[pc][0],t)
                if opc == 'O':
                    print(errors(opc,pc))
                    output+=errors(opc,pc)
                    return
                s+=opc
            else:
                pass

            if t=='A':
                s+='00'
                r1 = reg_to_bin(l[pc][1])
                r2 = reg_to_bin(l[pc][2])
                r3 = reg_to_bin(l[pc][3])
                if r1 == 'R' or r2 == 'R' or r3 == 'R':
                    print(errors('R',pc))
                    output+=errors('R',pc)
                    return
                s+=r1+r2+r3
                output+=s+'\n'


            elif t == 'B':
                r1=reg_to_bin(l[pc][1])
                if r1=='R':
                    print(errors('R',pc))
                    output+=errors('R',pc)
                    return
                s+=r1
                try:
                    assert l[pc][2][0]=='$'

                    if s[:5] == '10010':
                        try:
                            im=imm_to_bin(int(l[pc][2][1:]))
                            if im=='I':
                                print(errors(im,pc))
                                output+=errors(im,pc)
                                return
                            s+=im
                        except:
                            print("@Line"+str(pc+1)+" ERROR: Imm value should be a whole number <=255 and >=0")
                            output+="@Line"+str(pc+1)+" ERROR: Imm value should be a whole number <=255 and >=0"
                            return

                    elif s[:5] =='00010':
                        try:
                            float_num = binfloat_to_regformat(float_to_bin(float(l[pc][2][1:])))
                            if float_num == 'invalid':
                                print("@Line"+str(pc+1)+" ERROR: Immediate value should be a floating point number <=252.0 and >0.0")
                                output+="@Line"+str(pc+1)+" ERROR: Immediate value should be a floating point number <=252.0 and >0.0"
                                return
                            s+=str(float_num)

                        except:
                            print("@Line"+str(pc+1)+" ERROR: Immediate value should be a floating point number <=252.0 and >0.0")
                            output+="@Line"+str(pc+1)+" ERROR: Immediate value should be a floating point number <=252.0 and >0.0"
                            return
                                
                except:
                    print('@Line'+str(pc+1)+' ERROR: Invalid Syntax ($ sign missing)')
                    output+='@Line'+str(pc+1)+' ERROR: Invalid Syntax ($ sign missing)'
                    return

                output+=s+'\n'

            
            elif t == 'C':
                s+="0"*5
                r1 = reg_to_bin(l[pc][1])
                r2 = reg_to_bin(l[pc][2])
                if r1 == 'R' or r2 == 'R':
                    print(errors('R',pc))
                    output+=errors('R',pc)
                    return
                s += r1 + r2
                output+=s+'\n'


            elif t=='D':
                r1=reg_to_bin(l[pc][1])
                if r1=='R':
                    print(errors('R',pc))
                    output+=errors('R',pc)
                    return
                s+=r1
                if l[pc][2] in dict_var:
                    s+=dict_var[l[pc][2]]
                else:
                    print(errors('V',pc))
                    output+=errors('V',pc)
                    return
                output+=s+'\n'


            elif t=='E':
                s+='0'*3
                if (l[pc][1]+':') not in label_d:
                    print(errors('L',pc))
                    output+=errors('L',pc)
                    return
            
                s+=imm_to_bin(label_d[l[pc][1]+':'])
                output+=s+'\n'


            
            elif t=='F':
                output+=s+'0'*11+'\n'
                print(output)
                return 
                
            pc+=1

    except:
        print(errors('G',pc))
        output+=errors('G',pc)
        return 
        

main()
file = open('output.txt','a')
file.write(output)
file.close()
