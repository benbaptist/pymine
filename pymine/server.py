import sys, socket

class Server:
    def __init__(self, config):
        self.config = config
        self.abort = False
        
        # TODO: Initialize logger
        
        # TODO: Open socket
    
    def listen(self):
        while not self.abort:
            # TODO: Listen for connections
            pass
        
        # Loop ended, so abort = True
        sys.exit(0)
