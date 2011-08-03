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
		self.log.debug("Server sent packet to %s: %s" % (self.addr, data))
	def listen(self):
		while True:
			buffer = self.sock.recv(1024)
			print self.hexlify(buffer)
			
			if len(buffer) == 0:
				self.log.info("Client %s:%d disconnected" % \
					(self.addr, self.id))
				break
			
			self.log.debug("Received a message")
			self.log.debug("Running the PacketParser")
			
			parsed = PacketParser(buffer, self.log).packet 
			self.log.debug("Packet ID: %s" % parsed[0])
			
			# 0x01: LOGIN_REQUEST
			if parsed[0] == 1:
				#if parsed[1] != Server.protocol_version:
				#	self.log.info("%s has a protocol mismatch!" % self.addr)
				prococol_version = parsed[1]
				
				self.send(PacketMaker(["\x01", int(8000)], self.log).packet)	
				
				self.send(PacketMaker(["\x0d", 2,2,2,2,2,2,2], self.log).packet)	
			
			# 0x02: HANDSHAKE
			if parsed[0] == 2:
				self.log.info("%s is logging in as %s" % (self.addr, parsed[1]))
				self.player = Player(self.addr, self.log)
				self.player.username = parsed[1]
				self.player.entityID = random.randrange(0, 9999)
				
				self.send(PacketMaker(["\x02", "-"], self.log).packet+"\n")
			# returns an array of each field
			# note that strings have 0x00 sandwiched between each character, and it seems to be hard to strip out. this may cause issues with if statements.
			# 3f:f0:00:00:00:00:00:00:3f:f0:00:00:00:00:00:00:3f:f0:00:00:00:00:00:00:3f:f0:00:00:00:00:00:00:3f:80:00:00:3f:80:00:00:01