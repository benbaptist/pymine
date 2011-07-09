import sys, socket

class Server:
    def __init__(self, config):
        self.config = config
        self.abort = False
        
        # TODO: Initialize logger
       	
       	self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.socket.bind(('0.0.0.0',config{'port'}))
		self.socket.listen(5)
    
    def listen(self):
        while not self.abort:
			c,d = self.socket.accept() # c is the client object. you can do things like c.send('blah') with it. d should return IP address, etc. (I think)
			
			
        
        # Loop ended, so abort = True
        sys.exit(0)
