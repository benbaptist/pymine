class Connection:
	def __init__(self, sock, addr, id, info, log):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
		self.log = log
	
	def listen(self):
		while True:
			buffer = self.sock.recv(1024)
			
			if len(buffer) == 0:
				self.log.info("Client %s:%d disconnected" % \
					(self.addr, self.id))
				break
			
			self.log.debug("Received a message")
			packetID = self.buffer[0:1]
			
			self.log.debug("Packet ID: %s" % packetID.encode('hex'))
