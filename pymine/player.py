import random
class Player:
	username = ""
	health = 10
	def __init__(self, addr, log):
		self.addr = addr
		self.log = log
		self.eid = random.randrange(0, 3000)