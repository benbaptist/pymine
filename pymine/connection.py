from pymine.packets import *
from pymine.player import *
from pymine.server import *
import binascii, random
class Connection:
	def __init__(self, sock, addr, id, info, log, server):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
		self.server = server
		
		self.log = log
		self.hexlify = binascii.hexlify
		
		self.username = ""
	def close(self):
		self.sock.close()
	def send(self, data):
		self.sock.send(data, 1024)
		# self.log.debug("Server sent packet to %s: %s" % (self.addr, data))
	def recv(self, num):
		if num < 0:
			result = self.buffer
		else:
			result = self.buffer[0:num]
			self.buffer = self.buffer[num:]
		return result
	def packetSend(self, type, args):
		packet = ""
		if type == 2:
			ConnectionHash = args[0]
			packet = "\x02\x00\x01%s" % ConnectionHash
		self.send(packet)
	def listen(self):
		while True:
			self.buffer = self.sock.recv(1024)
			self.log.debug("Received a message")
			
			if len(self.buffer) == 0:
				self.log.info("Client %s:%d disconnected" % \
					(self.addr, self.id))
				break
			type = self.recv(1)
			
			if type == '\x02': # PACKET: HANDSHAKE
				UsernameLength = self.recv(2)
				Username = self.buffer
				self.log.info("%s:%d logged in as %s" % \
					(self.addr, self.id, Username))
				self.packetSend(2, ['-'])
			
			# if type == '\x01':
				