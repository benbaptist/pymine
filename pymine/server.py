import os, sys, socket
from logger import Logger
from connection import Connection

class Server:
	protocol_version = 14
	def __init__(self, config):
		self.config = config
		self.abort = False
		self.connections = []
		
		self.log = Logger(os.path.expanduser("~/.pymine.log"))
		self.log.info("Started logging")
		
		self.info = {}
		# TODO: Fill info with init values
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self.socket.bind(('', config['port']))
		except:
			self.log.error("Unable to bind to port! Binding to next available port...")
			self.socket.bind(('', config['port'] + 1))
			config['port'] += 1
		
		self.socket.listen(5)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.log.info("Listening to port %d" % config['port'])
	def close(self):
		self.socket.close()
	
	def listen(self):
		while not self.abort:
			sock, info = self.socket.accept()
			addr, id = info
			self.log.info("Client connecting: %s:%d" % (addr, id))
			
			conn = Connection(sock, addr, id, self.info, self.log, self.socket)
			conn.listen()
			
			self.connections.append(conn)
		
		# Loop ended, so abort = True
		sys.exit(0)
