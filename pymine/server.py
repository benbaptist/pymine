import os, sys, socket, thread, traceback
from logger import Logger
from connection import Connection

class Server:
# 	protocol_version = 22
	def __init__(self, config):
		self.config = config
		self.abort = False
		self.connections = []
		
		self.playersConnected = 0
		
		self.motd = config['motd']
		
		self.log = Logger(os.path.expanduser("~/.pymine.log"))
		self.log.info("Started logging")
		
		self.info = {}
		
		self.protocolVersion = 23
		# TODO: Fill info with init values
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self.socket.bind(('', config['port']))
			self.isReady = 1
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
			
			current = Connection(sock, addr, id, self.info, self.log, self.socket, self)
			self.connections.append(current)
			thread.start_new_thread(current.listen, ())
		
		# Loop ended, so abort = True
		sys.exit(0)
	
	def broadcastGlobalMessage(self, message):
		self.log.info(message)
		for x in self.connections:
			if x.defunct == False:
				x.broadcast(message)
	def userJoined(self):
		self.playersConnected += 1
	def userLeft(self):
		self.playersConnected -= 1