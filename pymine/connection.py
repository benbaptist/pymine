class Connection:
	def __init__(self, sock, addr, id, info):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
	
	def listen(self):
		pass
