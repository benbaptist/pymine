import binascii
class Connection:
	def __init__(self, sock, addr, id, info, log):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
		self.log = log
	
	def listen(self):
		self.abort = 0
		while not self.abort:
			self.buffer,self.addr= self.sock.recvfrom(1024)
			
			if len(self.buffer) == 0:
				self.abort = 1
				self.log.info("Disconnected")
				break
			
			if not self.abort:
				self.log.info("Received a message")
				self.packetID = self.buffer[0:1]
				
				self.log.info("Packet ID: %s" % binascii.hexlify(self.packetID))