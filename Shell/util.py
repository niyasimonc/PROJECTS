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





def setup_pipe(cmd_list):
    '''setting piping'''
    std_in=os.dup(0)
    std_out=os.dup(1)
    (r,w)=os.pipe()
    for index in range(len(cmd_list)):
        if cmd_list[index] == '|':
            cmd1=(cmd_list[:index])
            cmd2=cmd_list[index+1:]
            break
    pid=os.fork()
    if pid>0:
       os.wait()
       os.dup2(r,0)
       os.close(w)
       r=os.fork()
       if r==0:
           os.execvp(cmd2[0],cmd2)
       else:
           os.wait()
           os.dup2(std_out,1)
           os.dup2(std_in,0)
           return
    else:
       os.dup2(w,1)
       os.close(r)
       os.execvp(cmd1[0],cmd1)
       return
