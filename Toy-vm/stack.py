class stack(object):
    '''class stack'''
    def __init__(self):
        ''' initialising stack'''
        self.stack=[]
    def push(self,data):
        '''push data to stack'''
        self.stack.append(data)
    def pop(self):
        '''pop element from stack'''
        try:
            return self.stack.pop()
        except IndexError:
            print 'Stack is empty'
    def get_top_n(self, num):
        """ returns the top -num'th element of the stack """
        try:
            return self.stack[-1-num]
        except IndexError:
            print "there is only {} elements!"
    def print_stack(self):
        """ prints the stack """
        print self.stack   
