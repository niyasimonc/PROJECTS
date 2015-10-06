import sys
import opcodes
import functions
import Code
import stack


def less_than(op1, op2):
    """ a < b """
    return op1 < op2

def less_equal(op1, op2):
    """ a <= b """
    return op1 <= op2

def equal(op1, op2):
    """ a == b """
    return op1 == op2

def not_equal(op1, op2):
    """ a != b """
    return op1 != op2

def greater_than(op1, op2):
    """ a > b """
    return op1 > op2

def grt_equal(op1, op2):
    """ a >= b """
    return op1 >= op2


""" dictionary compare_op_index: comparison """
comparisons = {0: less_than,1: less_equal,2: equal,3: not_equal,4: greater_than,5: grt_equal}



def execute(code_obj):
    '''executing'''
    cur=0
    stak=stack.stack()
    while cur<len(code_obj.code):
        opcode=code_obj.code[cur]
#        print cur,len(code_obj.code),hex(opcode)
        if opcode==0x64:        # LOAD_CONS
            operand=functions.get_oparg(code_obj.code,cur)
            stak.push(code_obj.consts[operand])
            cur+=3
        elif opcode==0x5a:      # STORE_NAME
            operand=functions.get_oparg(code_obj.code,cur)
            n=stak.pop()
            if Code.name_value.get(code_obj.names[operand]):
                Code.name_value[code_obj.names[operand]]=n
            code_obj.names[operand]=n
            cur+=3
        elif opcode==0x47:      # PRINT_ITEM
            print stak.pop(),
            cur+=1
        elif opcode==0x48 :     # PRINT_NEWLINE
            print 
            cur+=1
        elif opcode==0x78:      # SETUP_LOOP
            cur+=3
        elif opcode==0x65:       # LOAD_NAME
            oparg=functions.get_oparg(code_obj.code,cur)
            stak.push(code_obj.names[oparg])
            cur+=3
        elif opcode==0x71 :     # JUMB_ABSOLUTE
            cur=functions.get_oparg(code_obj.code,cur)
        elif opcode==0x57  :   # POP_BLOCK
            cur+=1
        
        elif opcode==0x53:    # RETURN_VALUE
            return stak.pop()
        elif opcode==0x67:   #BUILD_LIST
            oparg=functions.get_oparg(code_obj.code,cur)
            lst=[0]*oparg
            end=oparg-1
            for i in range(oparg):
                lst[end]=stak.pop()
                end-=1
            stak.push(lst)
            cur+=3
        elif opcode==0x6b:    #	COMPARE_OP
            opname=functions.get_oparg(code_obj.code,cur)
            tos=stak.pop()
            tos2=stak.pop()
            stak.push(comparisons[opname](tos2, tos))
            cur+=3
        elif opcode==0x72   :  # POP_JUMP_IF_FALSE
            target=functions.get_oparg(code_obj.code,cur)
            value=stak.pop()
            if not value: 
                cur=target
            else: 
                cur+=3

        elif opcode==0x73   :  # POP_JUMP_IF_TRUE
            target=functions.get_oparg(code_obj.code,cur)
            value=stak.pop()
            if  value:
                cur=target
            else:
                cur+=3

        elif opcode==0x17:    #BINARY_ADD
            stak.push(stak.pop()+stak.pop())
            cur+=1
        elif opcode==20:    #BINARY_MULTIPLY
            stak.push(stak.pop()*stak.pop())
            cur+=1
        elif opcode==21:    #BINARY_DIVIDE
            stak.push(stak.pop()/stak.pop())
            cur+=1
        elif opcode==22:    #BINARY_MODULO
            stak.push(stak.pop()%stak.pop())
            cur+=1
        elif opcode==24:    #BINARY_SUBTRACT
            f=stak.pop()
            s=stak.pop()
#            print 'sub',f,s
            stak.push(s-f)
      
            cur+=1
        elif opcode==12:    #UNARY NOT
            stak.push(not stak.pop())
            cur+=1
        elif opcode==0x6e: #JUMP_FORWARD         
            delta=functions.get_oparg(code_obj.code,cur)
            cur+=delta+3
        elif opcode==0x84:    # MAKE_FUNCTION
            operand=functions.get_oparg(code_obj.code,cur)
            cur+=3
        elif opcode==0x83 :   #CALL_FUNCTION
            argc=functions.get_oparg(code_obj.code,cur)
            func=stak.get_top_n(argc)
            backup=func.varnames[:]
            while argc:
                argc -= 1
                func.varnames[argc] = stak.pop()
            stak.pop()
            ret=execute(func)
            stak.push(ret)
            func.varnames = backup[:]
            cur+=3
        elif opcode==0x7c :    #LOAD_FAST
            oparg=functions.get_oparg(code_obj.code,cur)
            stak.push(code_obj.varnames[oparg])
            cur+=3
        elif opcode==0x7d :   #STORE_FAST
            oparg=functions.get_oparg(code_obj.code,cur)
            code_obj.varnames[oparg]=stak.pop()
            cur+=3
        elif opcode==0x74: #LOAD_GLOBAL
            oparg=functions.get_oparg(code_obj.code,cur)
            if Code.name_value[code_obj.names[oparg]]:
                stak.push(Code.name_value[code_obj.names[oparg]])
            else:
                stak.push(code_obj.names[oparg])
            cur+=3
        elif opcode==25 :  #BINARY_SUBSCR
            top=stak.pop()
            nex=stak.pop()
            stak.push(nex[top])
            cur+=1
        else :
            if opcode>=90:
                cur+=3
            else:
                cur+=1                   
            
                    
 


 
    
        


def vm(filename):
    '''implementing virtual machine'''
    pyc_lst=functions.pyc_list(filename)
#    print pyc_lst
    code_obj=Code.code(pyc_lst)
    execute(code_obj)       
    return     



def main():
    '''main function'''
    if len(sys.argv)<2 or '.pyc' not in sys.argv[1]:
       print 'usage: main_code.py filename.pyc'
    else:
       filename=sys.argv[1]
       vm(filename)




if __name__=='__main__':
    main()
