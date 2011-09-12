#!/usr/bin/python
import time, sys, signal, threading
from config import config
from pymine.server import Server
from pymine.world import World
from pymine.logger import Logger
from pymine.world import World

if __name__ == '__main__':
	def quick_exit(s, f):
		sys.exit(0)
	signal.signal(signal.SIGINT, quick_exit)
	
	server = Server(config)
	server.listen()
	#ServerListeningThread = threading.Thread(target=server.listen)
	
	while not server.isReady:
		time.sleep(1)
	
	World1 = World()
	WorldThread = threading.Thread(target=World1.start)
	
	def ConsoleStart():
		while True:
			input = raw_input()
			args = input.split(' ')
	# ConsoleStart()
