import time
class World:
	def __init__(self):
		self.time = 0
		self.seed = ""
	def start_tick(self):
		self.tick = 0
		while 1:
			self.tick += 1
			time.sleep(0.05)
			print self.tick
			if self.tick == 20: self.tick = 0