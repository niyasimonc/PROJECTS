import os
import sys




def check_for_redir(lis):
    '''checking redirections'''
    if '|' in lis:
        return True
    elif '>' in lis:
        return True
    elif '<' in lis:
        return True
    else:
        return False




def setup_outred(cmd_list):
    '''setting redirection'''
    std_out=os.dup(1)
    cmd=[]
    for index in range(len(cmd_list)):
        if cmd_list[index] == '>':
            cmd=cmd_list[:index]
            fil=cmd_list[index+1]        
            break
    fd = os.open( fil,os.O_WRONLY|os.O_CREAT )  
    os.dup2(fd,1)
    
    r=os.fork()
    if r==0:
            try:
                err=os.execvp(cmd[0],cmd)
            except OSError:
                print '\n',cmd[0],':command not found\n'
                sys.exit()
    os.wait()
    os.close(fd)
    os.dup2(std_out,1)
    return







    
def setup_inred(cmd_list):
    '''setting redirection'''
    std_out=os.dup(1)
    std_in=os.dup(0)
    for index in range(len(cmd_list)):
        if cmd_list[index] == '<':
            cmd=(cmd_list[:index])
            fil=cmd_list[index+1]
            break
    fd = os.open( fil,os.O_RDONLY)
    os.dup2(fd,0)
    r=os.fork()
    if r==0:
            try:
                err=os.execvp(cmd[0],cmd)
            except OSError:
                print '\n',cmd[0],':command not found\n'
                sys.exit()
    os.wait()
    os.close(fd)
    os.dup2(std_out,1)
    os.dup2(std_in,0)
    return





def single_pipe(cmnds,std_in,std_out):
    '''single pipe execution'''
    
    (r,w)=os.pipe()
    pid=os.fork()
    if pid>0:
       os.wait()
       os.dup2(r,0)
       os.close(w)
       re=os.fork()
       if re==0:
          os.execvp(cmnds[1][0],cmnds[1])
       else:
          os.wait()
          os.dup2(std_out,1)
          os.dup2(std_in,0)
          return
    else:
       os.dup2(w,1)
       os.close(r)
       os.execvp(cmnds[0][0],cmnds[0])
       return





def setup_pipe(cmd_list):
    '''setting piping'''
    std_in=os.dup(0)
    std_out=os.dup(1)
    count=0
    for ind in range(len(cmd_list)):
        if cmd_list[ind]=='|':
            count+=1
    cmnds=[]
    j=0
    for i in range(len(cmd_list)):
        if cmd_list[i]=='|':
            cmnds.append(cmd_list[j:i])
            j=i+1
    cmnds.append(cmd_list[j:])
    if count==1:
        single_pipe(cmnds,std_in,std_out)
        return
    elif count==2:
        (r1,w1)=os.pipe()
        (r2,w2)=os.pipe()
        if os.fork()==0:
            os.dup2(w1,1)
            os.close(r1)
            os.close(w1)
            os.close(r2)
            os.close(w2)
            os.execvp(cmnds[0][0],cmnds[0])
        else:
            if  os.fork()==0:
                os.dup2(r1,0)
                os.dup2(w2,1)
                os.close(r1)
                os.close(w1)
                os.close(r2)
                os.close(w2)
                os.execvp(cmnds[1][0],cmnds[1])
            else:
                if os.fork()==0:
                    os.dup2(r2,0)
                    os.close(r1)
                    os.close(w1)
                    os.close(r2)
                    os.close(w2)
                    os.execvp(cmnds[2][0],cmnds[2])
        os.close(r1)
        os.close(w1)
        os.close(r2)
        os.close(w2)
        for i in range(3):
            os.wait()
        return

        

          
           
    
