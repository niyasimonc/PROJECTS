import sys
import opcodes


def read_pyc(filename):
    ''' Reading a .pyc file as ascii values'''
    lst=[]
    f=open(filename,'rb')
    if f==None:
       print "Error in file"
    magic_and_timestamp = f.read(8)  # first 8 bytes are metadata

    for line in f:
        word=line.strip()
        for c in word:
             yield ord(c)
    
def pyc_list(filename):
    ''' return the list which contains the ascii values of .pyc file content'''
    return list(read_pyc(filename))



def find_start(lst):
    """find start of the code object"""
    i=0
    for i in range(len(lst)):
        if opcodes.m_type.get(lst[i])=='TYPE_CODE':
               return i 


def have_arg(value):
    '''check whether it have argument or not'''
    if value>=opcodes.HAVE_ARGUMENT:
        return True
    else:
        return False




def get_oparg(lst,cur):
    '''finding opargs'''
    l = lst[cur+1]
    m = lst[cur+2]
    return l | m << 8  # l + m * 256 


def r_long(cur,lst):
    x=lst[cur+1]
    x|=lst[cur+2]<<8
    x|=lst[cur+3]<<16
    x|=lst[cur+4]<<24
    return x




def print_assembler(lst,cur):
    ''' printing disassembler'''
    typ=opcodes.m_type.get(lst[cur])
   
    
    if typ=='TYPE_CODE':
        if chr(lst[cur+17])=='s':
            cur=cur+17   #4 bytes:argcount,4bytes:nlocals,4bytes:stacksize,4 bytes:flags 
        cur=print_assembler(lst,cur)      
        return cur+1
    
    if lst[cur]==115:    #TYPE_STRING
       size=r_long(cur,lst)         #size
       cur+=5            #next byte
       i=0
       while i<size:
        if not have_arg(lst[cur]):  
            print opcodes.my_map.get(lst[cur])
            cur+=1
            i+=1
        else:
            print opcodes.my_map.get(lst[cur]),get_oparg(lst,cur)
            cur+=3
            i+=3
       return cur    
    
    

def disassembler(filename):
    '''dissassembling a .pyc file'''  
    
    lst=pyc_list(filename)
    index_of_start_code=find_start(lst)
    cur=print_assembler(lst,index_of_start_code)    
    return     
   



def main():
    ''' Main function'''
    if len(sys.argv)<2:
       print 'usage: main_code.py filename.pyc'
    else:
       filename=sys.argv[1]
       disassembler(filename)


if __name__=='__main__':
     main()
