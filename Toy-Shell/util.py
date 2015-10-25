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
    pipes=[]
    for i in range(count):
        pipes.append(tuple(os.pipe()))
#    print pipes
    if os.fork()==0:
       os.dup2(pipes[0][1],1)
       for k in range(count):
           for j in range(2):
               os.close(pipes[k][j])
       os.execvp(cmnds[0][0],cmnds[0])        
    else:
        for i in range(1,count):
            if os.fork()==0:
                os.dup2(pipes[i-1][0],0)
                os.dup2(pipes[i][1],1)
                for k in range(count):
                    for j in range(2):
                        os.close(pipes[k][j])
                os.execvp(cmnds[i][0],cmnds[i])
        if os.fork()==0:
            os.dup2(pipes[-1][0],0)
            for k in range(count):
                for j in range(2): 
                    os.close(pipes[k][j])
            os.execvp(cmnds[-1][0],cmnds[-1])
        else:
            for k in range(count):
               for j in range(2):
                   os.close(pipes[k][j])
            for i in range(count):
                os.wait()
            os.wait()
            os.dup2(std_out,1)
            os.dup2(std_in,0)
            return
