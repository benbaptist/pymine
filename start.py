import time, sys
from config import config
from pymine.server import Server

if __name__ == '__main__':
	server = Server(config)
	server.listen()
