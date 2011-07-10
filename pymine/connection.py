class Connection:
	def __init__(self, sock, addr, id, info, log):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
		self.log = log
	
	def listen(self):
		pass
