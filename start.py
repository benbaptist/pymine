import time, sys
from config import config
from pymine.server import Server
from pymine.world import World

if __name__ == '__main__':
	server = Server(config)
	server.listen()
