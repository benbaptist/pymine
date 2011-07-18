from pymine.packets import *
from pymine.player import *
import binascii
class Connection:
	def __init__(self, sock, addr, id, info, log):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
		self.log = log
	
	def send(self,data):
		self.sock.send(data, 1024)
		self.log.debug("Server sent packet to %s: %s" % (self.addr, data))
	def listen(self):
		while True:
			buffer = self.sock.recv(1024)
			
			if len(buffer) == 0:
				self.log.info("Client %s:%d disconnected" % \
					(self.addr, self.id))
				break
			
			self.log.debug("Received a message")
			packetID = buffer[0:1]
			
			self.log.debug("Packet ID: %s" % packetID.encode('hex'))
			self.log.debug("Running the PacketParser")
			
			parsed = PacketParser(buffer,self.log).packet 
			
			if parsed[0] == 2:
				self.log.info("%s is logging in as %s" % (self.addr, parsed[1]))
				self.player = Player(self.addr,self.log)
				self.player.username = parsed[1]
				a = PacketMaker(["\x02","-"],self.log)
				print binascii.hexlify(a.packet)
				self.send(a.packet)
			
			# returns an array of each field
			# note that strings have 0x00 sandwiched between each character, and it seems to be hard to strip out. this may cause issues with if statements.