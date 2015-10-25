import os
import sys
import util


def execute(cmd_list):
    '''executing'''
    for index in range(len(cmd_list)):
        if cmd_list[index]=='<':
           util.setup_inred(cmd_list)
           break
        if cmd_list[index]=='>':
           util.setup_outred(cmd_list)
           break
        if cmd_list[index]=='|':
           util.setup_pipe(cmd_list)
           break
    return





def shell(prompt):
    '''Implements shell'''
    while(1):
        print '\nEnter your command here',prompt,
        cmd=raw_input()    
        cmd_list=cmd.split()
        check=util.check_for_redir(cmd_list)        
        if check:
            v=execute(cmd_list)        
            continue
        if cmd_list[0]=='exit':
            print 
            print 'Exiting...'
            print
            return
        elif os.fork()==0:
            try:
                err=os.execvp(cmd_list[0],cmd_list)
            except OSError:
                print '\n',cmd_list[0],':command not found\n'
                sys.exit()
        os.wait()
    return    


          
  
def main():
    '''Main function'''
    
    prompt=':$'
    print 
    print
    print "**************niya's shell**************"
    print
    shell(prompt)
    return  




if __name__=='__main__':
    main()
