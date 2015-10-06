import functions


INT_LIMIT = 2 ** 31
stringref=[]
name_value={}

class code(object):
    '''class code'''

    def __init__(self,pyc_lst,cur=0):
        '''initialsing'''
        self.pyclst=pyc_lst
        self.cur=cur
        self.code=self.acq_code()       
#        print self.code
        self.consts = self.acq_consts()
#        print self.consts
        self.names = self.acq_names()
 #       print self.names
        self.varnames = self.acq_varnames()
 #       print self.varnames
        self.freevars = self.acq_freevars()
 #       print self.freevars
        self.cellvars=self.acq_cellvars()
 #       print self.cellvars
        self.filename=self.acq_filename()
 #       print self.filename
        self.name=self.acq_name()
 #       print self.name
        self.firstlineno=self.acq_firstlineno()
 #       print self.firstlineno
        self.lnotab=self.acq_lnotab()
 #       print self.lnotab
  

    def acq_code(self):
        '''co_code field'''
        pyc_lst=self.pyclst
        cur=self.cur
        code=[]
        if chr(pyc_lst[cur])=='c' and chr(pyc_lst[cur+17])=='s':
           self.argcount=functions.r_long(cur,pyc_lst)
           if self.argcount >= INT_LIMIT:
                self.argcount -= (2 * INT_LIMIT)

           cur+=17
           size=functions.r_long(cur,pyc_lst)
           cur+=5
           for i in range(size):
               code.append(pyc_lst[cur+i])
           cur=cur+size
        self.cur=cur
        return code   
           
              
    def acq_consts(self):
        pyc_lst=self.pyclst
        cur=self.cur
        consts=[]
        size=functions.r_long(cur,pyc_lst)
        cur+=5
        for i in range(size):
#            print i,cur,hex(pyc_lst[cur]),chr(pyc_lst[cur])
            if chr(pyc_lst[cur])=='i':  #	TYPE_INT
                x=functions.r_long(cur,pyc_lst)
                if x >= INT_LIMIT:                    
                    x = x - (2 * INT_LIMIT)
                consts.append(x)
                cur+=5
            elif pyc_lst[cur]==78:   #TYPE_NONE
                consts.append(None)
                cur+=1
            elif chr(pyc_lst[cur])=='t' or pyc_lst[cur]==115:  #TYPE_INTERNED or TYPE_STRING
                char=chr(pyc_lst[cur])
                length=functions.r_long(cur,pyc_lst)
                cur+=5
                strng=''
                for j in range(length):
                    strng+=chr(pyc_lst[cur+j])
                cur=cur+length
                if char=='t':
                     stringref.append(strng)
                consts.append(strng)
            elif chr(pyc_lst[cur])=='c' :    #TYPE_CODE
                code_obj=code(pyc_lst,cur)
                cur=code_obj.cur
                consts.append(code_obj)
            else:
                print 'NOT DEFIEND IN CO_CONSTS'
                return

                
                
        self.cur=cur
        return consts



    def acq_names(self):
        pyc_lst=self.pyclst
        cur=self.cur
        names=[]
#        print 'inside names',cur,hex(self.pyclst[cur]),chr(pyc_lst[cur])
        size=functions.r_long(cur,pyc_lst)
        cur+=5
#        print 'inside names',cur,hex(self.pyclst[cur]),chr(pyc_lst[cur])       
        for i in range(size):
            if chr(pyc_lst[cur])=='t':  #TYPE_INTERNED
                char=chr(pyc_lst[cur])
                length=functions.r_long(cur,pyc_lst)
                cur+=5
                strng=''
                for j in range(length):
                    strng+=chr(pyc_lst[cur+j])
                if char=='t':
                     stringref.append(strng)
                     name_value[strng]=strng
                cur=cur+length
                names.append(strng)
            elif chr(pyc_lst[cur])=='i':  #       TYPE_INT
                x=functions.r_long(cur,pyc_lst)
                if x >= INT_LIMIT:
                    x = x - (2 * INT_LIMIT)
                names.append(x)
                cur+=5
            elif chr(pyc_lst[cur])=='R':   # TYPE_STRINGREF
                index=functions.r_long(cur,pyc_lst)
                names.append(stringref[index])
                cur+=5


        self.cur=cur
        return names  



    def acq_varnames(self):
        '''co_varnames  field'''
        pyc_lst=self.pyclst
        cur=self.cur
        var_names=[]
        size=functions.r_long(cur,pyc_lst)
        cur+=5
        for i in range(size):
            if chr(pyc_lst[cur])=='t':  #TYPE_INTERNED
                char=chr(pyc_lst[cur])
                length=functions.r_long(cur,pyc_lst)
                cur+=5
                strng=''
                for j in range(length):
                    strng+=chr(pyc_lst[cur+j])
                if char=='t':
                     stringref.append(strng)
                cur=cur+length
                var_names.append(strng)
        self.cur=cur
        return var_names

    def acq_freevars(self):
        pyc_lst=self.pyclst
        cur=self.cur
        free_vars=[]
        size=functions.r_long(cur,pyc_lst)
        cur+=5
        self.cur=cur
        return free_vars
                

    def acq_cellvars(self):
        pyc_lst=self.pyclst
        cur=self.cur
        cell_vars=[]
        size=functions.r_long(cur,pyc_lst)
        cur+=5
        self.cur=cur
        return cell_vars

 
    def acq_filename(self):
        pyc_lst=self.pyclst
        cur=self.cur
        if chr(pyc_lst[cur])=='s':
            length=functions.r_long(cur,pyc_lst)
            cur+=5
            strng=''
            for j in range(length):
                strng+=chr(pyc_lst[cur+j])
            cur+=length
        self.cur=cur
        return strng

    def acq_name(self):
        pyc_lst=self.pyclst
        cur=self.cur
        cell_vars=[]
        if chr(pyc_lst[cur])=='t' or pyc_lst[cur]==115:  #TYPE_INTERNED
                length=functions.r_long(cur,pyc_lst)
                char=chr(pyc_lst[cur])
                cur+=5
                strng=''
                for j in range(length):
                    strng+=chr(pyc_lst[cur+j])
                if char=='t':
                     stringref.append(strng)
                cur=cur+length
        elif chr(pyc_lst[cur])=='R':   # TYPE_STRINGREF
                index=functions.r_long(cur,pyc_lst)
                strng=''
                for j in range(index):
                    strng+=chr(pyc_lst[cur+j])
                cur+=5

        self.cur=cur
        return strng

    def acq_firstlineno(self):
        lst=self.pyclst
        cur=self.cur
        x=lst[cur]
        x|=lst[cur+1]<<8
        x|=lst[cur+2]<<16
        x|=lst[cur+3]<<24
    
        cur+=4
        self.cur=cur
        return x


    def acq_lnotab(self):
        pyc_lst=self.pyclst
        cur=self.cur
        if chr(pyc_lst[cur])=='t' or pyc_lst[cur]==115:  #TYPE_INTERNED
                length=functions.r_long(cur,pyc_lst)
                cur+=5
                strng=''
                for j in range(length):
                    strng+=str(pyc_lst[cur+j])
                cur=cur+length
        self.cur=cur
#        print hex(pyc_lst[cur]),cur
        return strng



