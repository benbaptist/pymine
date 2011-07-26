import os, sys, socket
from logger import Logger
from connection import Connection

class Server:
	protocol_version = 14
	def __init__(self, config):
		self.config = config
		self.abort = False
		
		self.log = Logger(os.path.expanduser("~/.pymine.log"))
		self.log.info("Started logging")
		
		self.info = {}
		# TODO: Fill info with init values
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('', config['port']))
		self.socket.listen(5)
		self.log.info("Listening to port %d" % config['port'])
	
	def listen(self):
		while not self.abort:
			sock, info = self.socket.accept()
			addr, id = info
			self.log.info("Client connecting: %s:%d" % (addr, id))
			
			conn = Connection(sock, addr, id, self.info, self.log)
			conn.listen()
		
		# Loop ended, so abort = True
		sys.exit(0)
