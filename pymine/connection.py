from pymine.packets import *
from pymine.player import *
from pymine.server import *
import binascii, random, thread, time, sys
class Connection:
	def __init__(self, sock, addr, id, info, log, server, globalServer):
		self.sock = sock
		self.addr = addr
		self.id = id
		self.info = info
		self.server = server
		self.globalServer = globalServer
		self.state = 0
		self.player = Player(addr, log)
		self.defunct = False
		
		self.log = log
		self.hexlify = binascii.hexlify
		
		self.username = ""
		self.sendBuff = ""
		self.connectionState = 0
	def close(self):
		self.sock.close()
		self.defunct = True
	def send(self, data):
		self.sock.send(data)
		# self.log.debug("Server sent packet to %s: %s" % (self.addr, data))
	def packetSend(self, type, args):
		packet = ""
		if type == 2:
			ConnectionHash = args[0]
			packet = "\x02\x00\x01%s" % ConnectionHash
		# self.send(packet)
	
	# RECEIVING FUNCTIONS
	def recv(self, num):
		if num < 0:
			result = self.buffer
		else:
			result = self.buffer[0:num]
			self.buffer = self.buffer[num:]
		return result
	def recvInt(self):
		Int = struct.unpack(">I",self.recv(4))
		return Int[0]
	def recvShort(self):
		Short = struct.unpack(">H", self.recv(2))
		return Short[0]
	def recvLong(self):
		Long = struct.unpack(">l", self.recv(4))
		return Long[0]
	def recvByte(self):
		return self.recv(1)
	def recvDouble(self):
		Double = struct.unpack(">d", self.recv(8))
		return Double[0]
	def recvFloat(self):
		Float = struct.unpack(">f", self.recv(4))
		return Float[0]
	def recvString(self):
		StringLen = self.recvShort()
		String = self.recv(StringLen * 2).decode('utf-16be')
		return String
	
	# SENDING FUNCTIONS
	def sendBuffer(self, add):
		self.sendBuff += add
	def sendFlush(self):
# 		print "SEND: " + self.sendBuff.encode('hex')
		self.send(self.sendBuff)
		self.sendBuff = ""
	def sendByte(self, byte):
		self.sendBuffer(byte.decode('hex'))
	def sendByteInt(self, byte):
		self.sendBuffer(struct.pack(">b", byte))
	def sendSignedByte(self, byte):
		self.sendBuffer(struct.pack(">b", byte))
	def sendUnsignedByte(self, byte):
		self.sendBuffer(str(byte))
	def sendInt(self, int):
		self.sendBuffer(struct.pack(">i", int))
	def sendLong(self, long):
		self.sendBuffer(struct.pack(">l", long))
	def sendShort(self, short):
		self.sendBuffer(struct.pack(">H", short))
	def sendDouble(self, double):
		self.sendBuffer(struct.pack(">d", double))
	def sendFloat(self, float):
		self.sendBuffer(struct.pack(">f", float))
	def sendString(self, string):
		self.sendShort(len(string))
		self.sendBuffer(string.encode('utf-16be'))
	def sendBool(self, bool):
		if bool:
			self.sendByte('01')
		else:
			self.sendByte('00')
	def loop(self):
		while True:
			if self.connectionState == 1:
				self.sendByte("00")
				self.sendInt(random.randrange(0,9999))
			time.sleep(0.50)
	def listen(self):
		self.connectionInit = False
		thread.start_new_thread(self.loop, ())
		while True:
			self.buffer = self.sock.recv(1024)
			
			if len(self.buffer) == 0:
				if self.username != "":
					self.log.info("User %s disconnected (%s)" % (self.username, self.addr))
				else:
					self.log.info("Client %s:%d disconnected" % \
						(self.addr, self.id))
				break
			type = self.recvByte()
# 			self.log.debug("PACKET ID: " + type.encode('hex'))
			# if self.connectionInit:
# 				self.sendFlush()
# 				self.sendByte('08')
# 				self.sendShort(random.randrange(2, 5))
# 				self.sendShort(random.randrange(2, 5))
# 				self.sendFloat(5.0)
# 				self.sendFlush()
#			self.sendByte('3d')
#			self.sendInt(1005)
#			self.sendInt(0)
#			self.sendByte('00')
#			self.sendInt(0)
#			self.sendInt(2262)
			if type == '\x00': # PACKET: KEEP ALIVE
				ID = self.recvInt()
				self.sendByte('00')
				self.sendInt(ID)
			if type == '\x02': # PACKET: HANDSHAKE
				Username = self.recvString()
				self.username = Username
				self.log.info("%s:%d logged in as %s" % \
					(self.addr, self.id, Username))
				self.sendByte('02')
				self.sendString('-')
				self.globalServer.broadcastGlobalMessage(u"\xa70\xa7e%s has joined the game." % Username)
				if self.globalServer.playersConnected == self.globalServer.config['max_users']:
					self.sendByte("ff")
					self.sendString("Server full! Yikes!")
					break
				self.globalServer.userJoined()
			if type == "\x03":
				Message = self.recvString()
				if Message[0:1] == "/":
					# command code here!
					self.broadcast("Commands are not implemented yet.")
					self.log.info("%s ran command: %s" % (self.username, Message))
				else:
					name = self.username
					for x in self.globalServer.config['ops']:
						if x == self.username:
							name = u"\xa70\xa7c" + self.username + u"\xa70\xa7f"
					self.globalServer.broadcastGlobalMessage("<%s> %s" % \
						(name, Message))
				if Message == "spawnmob":
					self.sendByte("17")
					self.sendInt(5)
					self.sendByte('01')
					self.sendInt(0)
					self.sendInt(67)
					self.sendInt(0)
					self.sendInt(0)
					
					self.sendByte('27')
					self.sendInt(self.player.eid)
					self.sendInt(5)
					
					self.sendByte('03')
					self.sendString('Should spawn a boat...')
					self.sendFlush()
				if Message == "hurt":
					self.sendByte('08')
					self.sendShort(random.randrange(2, 20))
					self.sendShort(random.randrange(2, 20))
					self.sendFloat(5.0)
					self.sendFlush()
				if Message == "creative":
					self.sendByte('46')
					self.sendByte('03')
					self.sendByte('01')
					self.sendFlush()
				if Message == "survival":
					self.sendByte('46')
					self.sendByte('03')
					self.sendByte('00')
					self.sendFlush()
				if Message == "smite":
					self.sendByte('47')
					self.sendInt(4)
					self.sendByte('01') # boolean, always true
					self.sendInt(0)
					self.sendInt(0)
					self.sendInt(0)
					self.sendFlush()
				if Message == "gimmie":
					self.sendByte('67')
					self.sendByte('00')
					self.sendShort(36)
				if Message == "exp":
					self.sendByte('3c')
					self.sendDouble(self.player.x)
					self.sendDouble(self.player.y)
					self.sendDouble(self.player.z)
					self.sendFloat(3.0)
					self.sendInt(1)
					self.sendByte('00')
					self.sendFlush()
				if Message == "confusion":
					self.sendByte('29')
					self.sendInt(self.player.eid)
					self.sendByte('09')
					self.sendByte('00')
					self.sendShort(64)
				if Message == "block":
					self.sendByte('35')
					self.sendInt(0)
					self.sendSignedByte(5)
					self.sendInt(0)
					self.sendSignedByte(5)
					self.sendSignedByte(00)
					# self.sendByte('33')
# 					self.sendInt(0)
# 					self.sendShort(0)
# 					self.sendInt(0)
# 					self.sendByte('15')
# 					self.sendByte('01')
# 					self.sendByte('15')
				if Message == "getpos":
					self.sendByte('03')
					self.sendString("X: %d Y: %d Z: %d" % (self.player.x, self.player.y, self.player.z))
				if Message == "scoot":
					self.sendByte('1c')
					self.sendInt(5)
					self.sendShort(2000)
					self.sendShort(0)
					self.sendShort(0)
					self.sendByte('26')
					self.sendInt(5)
					self.sendByte('02')
				if Message == "bing":
					self.sendByte('36')
					self.sendInt(0)
					self.sendShort(0)
					self.sendInt(0)
					self.sendByte("00")
					self.sendByte("00")
				if Message == "record":
					self.sendByte('3d')
					self.sendInt(1005)
					self.sendInt(0)
					self.sendByte('00')
					self.sendInt(0)
					self.sendInt(2262)
				if Message == "regular":
					self.sendFlush()
					self.sendByte("09")
					self.sendByte("80") # dimension
					self.sendByte("01") # difficulty
					self.sendByte("0a") # survival/creative
					self.sendShort(128)
					self.sendLong(-3815848935435401459)
					print len(self.sendBuff)
					self.sendString("DEFAULT")
					self.sendFlush()
				if Message[0:5] == "tppos":
					Args = Message.split(" ")
					X = int(Args[1])
					Y = int(Args[2])
					Z = int(Args[3])
					self.sendByte("0d")
					self.sendDouble(X)
					self.sendDouble(0)
					self.sendDouble(Y)
					self.sendDouble(Z)
					self.sendFloat(0.0)
					self.sendFloat(0.0)
					self.sendByte("01")
				if Message == "creeper":
					self.sendByte("18")
					self.sendInt(random.randrange(0, 9999))
					self.sendByteInt(50)
					self.sendInt(0)
					self.sendInt(60)
					self.sendInt(0)
					self.sendByteInt(-2)
					self.sendByteInt(0)
					self.sendByteInt(127)
				if Message == "pickup":
					self.sendByte("16")
					self.sendInt(38)
					self.sendInt(self.player.eid)
				# if Message == "hey":
# 					self.sendByte('03')
# 					self.sendString("Hey there, chum.")
# 				else:
# 					self.sendByte('03')
# 					self.sendString("Er... whaaaa?")
			if type == "\x07":
				self.recvInt()
				TargetEID = self.recvInt()
				self.sendByte('03')
				self.sendString('Ouchie! You hit %d' % TargetEID)
				self.log.info("Attax! %d" % TargetEID)
				if TargetEID == 5:
					self.sendByte('03')
					self.sendString('Hitting your own boat!? u mad bro?')
					self.sendByte('12')
					self.sendInt(5)
					self.sendByte('02')
					self.sendFlush()
				self.recvByte()
			if type == "\x01": # PACKET: LOGIN REQUEST
				self.connectionInit = True
				ProtocolVersion = self.recvInt()
				Username = self.recvString()
				self.recvLong()
				self.recvInt()
				self.recvByte()
				self.recvByte()
				self.recvByte() # unsigned?
				self.recvByte() # unsigned?
				
				if ProtocolVersion != self.globalServer.protocolVersion:
					self.sendByte('ff')
					self.sendString("Outdated Client/Server")
					self.log.info("Arr! Out of date!")
				
				self.sendByte('01')
				self.sendInt(self.player.eid)
				self.sendString('') # Not Used
				self.sendLong(971768181197178410) # Map Seed
				#self.sendString('DEFAULT') # Level Type (DEFAULT or SUPERFLAT)
				self.sendInt(1) # Server Mode
				self.sendByte('00') # Dimension
				self.sendByte('01') # Difficulty
				self.sendUnsignedByte('128')
				self.sendUnsignedByte('8')
				self.sendFlush()
				
				self.connectionState = 1
				
				self.sendByte("09")
				self.sendByte("80") # dimension
				self.sendByte("01") # difficulty
				self.sendByte("0a") # survival/creative
				self.sendShort(128)
				self.sendLong(-3815848935435401459)
				self.sendString("DEFAULT")
				
				self.sendFlush()
			if type == '\xfe': # PACKET: MOTD/PLAYERS/MAXPLAYERS	
				self.sendByte('ff')
				self.sendString(u"%s\xa7%d\xa7%d" % (self.globalServer.motd, self.globalServer.playersConnected, self.globalServer.config['max_users']))
			if type == '\x0d': # PACKET: PLAYER POS AND LOOK
				X = self.recvDouble()
				Y = self.recvDouble()
				Stance = self.recvDouble()
				Z = self.recvDouble()
				Yaw = self.recvFloat()
				Pitch = self.recvFloat()
				self.recvByte()
				self.player.x = X
				self.player.y = Y
				self.player.z = Z
				# if self.player.y < 0:					
# 					self.sendByte('0d')
# 					self.sendDouble(X)
# 					self.sendDouble(67)
# 					self.sendDouble(10)
# 					self.sendDouble(Z)
# 					self.sendFloat(Yaw)
# 					self.sendFloat(Pitch)
# 					self.sendBool(0)
			self.sendFlush()
		# connection ended
		if self.connectionState > 0:
			self.globalServer.broadcastGlobalMessage(u"\xa70\xa7e%s has left the game." % self.username)
			self.globalServer.userLeft()
		self.close()
	def broadcast(self, msg):
		self.sendByte('03')
		self.sendString(msg)