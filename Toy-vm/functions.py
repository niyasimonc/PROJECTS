def read_pyc(filename):
    ''' Reading a .pyc file as ascii values'''
    lst=[]
    f=open(filename,'rb')
    if f==None:
       print "Error in file"
    magic_and_timestamp = f.read(8)  # first 8 bytes are metadata
    while True:
        chunk = f.read(1)
        if chunk:
            for byte in chunk:
                yield ord(byte)
        else:
            break

 

def r_long(cur,lst):
    x=lst[cur+1]
    x|=lst[cur+2]<<8
    x|=lst[cur+3]<<16
    x|=lst[cur+4]<<24
    return x


    
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

