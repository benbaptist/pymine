import time, sys, signal
from config import config
from pymine.server import Server
from pymine.world import World
from pymine.logger import Logger
from pymine.world import World

def quick_exit(s, f):
	sys.exit(0)
signal.signal(signal.SIGINT, quick_exit)
#try:
if __name__ == '__main__':
	server = Server(config)
	server.listen()
#except:
#	l = Logger()
#	l.error("Sorry, a fatal error occurred.")
#	#server.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	#server.socket.close()
#	sys.exit(0)