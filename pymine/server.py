import sys, socket

class Server:
	def __init__(self, config):
		self.config = config
		self.abort = False
		
		# TODO: Initialize logger
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('', config['port']))
		self.socket.listen(5)
	
	def listen(self):
		while not self.abort:
			conn, info = self.socket.accept()
			addr, id = info
			
			# TODO: Create and start a Connection object
		
		# Loop ended, so abort = True
		sys.exit(0)
