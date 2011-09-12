import time
class World:
	def __init__(self):
		self.time = 0
		self.seed = ""
	def start(self):
		self.tick = 0
		while True:
			self.tick += 1
			print self.tick
			if self.tick == 20: self.tick = 0
			time.sleep(0.05)