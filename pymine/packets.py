from logger import Logger
from hex import HexToDecimal
import binascii, struct
class PacketIDs:
	KEEP_ALIVE = 0x00
	LOGIN_REQUEST = 0x01
	HANDSHAKE = 0x02
	CHAT_MESSAGE = 0x03
	TIME_UPDATE = 0x04
	ENTITY_EQUIPMENT = 0x05
	SPAWN_POSITION = 0x06
	USE_ENTITY = 0x07
	UPDATE_HEALTH = 0x08
	RESPAWN = 0x09
	PLAYER = 0x0A
	PLAYER_POSITION = 0x0B
	PLAYER_LOOK = 0x0C
	PLAYER_POSITION_LOOK = 0x0D
	PLAYER_DIGGING = 0x0E
	PLAYER_BLOCK_PLACEMENT = 0x0F
	HOLDING_CHANGE = 0x10
	USE_BED = 0x11
	ANIMATION = 0x12
	ENTITY_ACTION = 0x13
	NAMED_ENTITY_SPAWN = 0x14
	PICKUP_SPAWN = 0x15
	COLLECT_ITEM = 0x16
	ADD_OBJECT = 0x17
	MOB_SPAWN = 0x18
	ENTITY_PAINTING = 0x19
	STANCE_UPDATE = 0x1B
	ENTITY_VELOCITY = 0x1C
	DESTROY_ENTITY = 0x1D
	ENTITY = 0x1E
	ENTITY_RELATIVE_MOVE = 0x1F
	ENTITY_LOOK = 0x20
	ENTITY_LOOK_RELATIVE_MOVE = 0x21
	ENTITY_TELEPORT = 0x22
	ENTITY_STATUS = 0x26
	ATTACH_ENTITY = 0x27
	ENTITY_METADATA = 0x28
	PRE_CHUNK = 0x32
	MAP_CHUNK = 0x33
	MULTI_BLOCK_CHANGE = 0x34
	BLOCK_CHANGE = 0x35
	BLOCK_ACTION = 0x36
	EXPLOSION = 0x3C
	SOUND_EFFECT = 0x3D
	NEW_INVALID_STATE = 0x46
	THUNDERBOLT = 0x47
	OPEN_WINDOW = 0x64
	CLOSE_WINDOW = 0x65
	WINDOW_CLICK = 0x66
	SET_SLOT = 0x67
	WINDOW_ITEMS = 0x68
	UPDATE_PROGRESS_BAR = 0x69
	TRANSACTION = 0x6A
	UPDATE_SIGN = 0x82
	MAP_DATA = 0x83
	INCREMENT_STATISTIC = 0xC8
	DISCONNECT_KICK = 0xFF
	packets = {
		'KEEP_ALIVE': '\x00',
		'LOGIN_REQUEST': '\x01',
		'HANDSHAKE': '\x02',
		'CHAT_MESSAGE': '\x03',
		'PLAYER_POS': '\x0d'
	}
class PacketParser:
	def __init__(self, data, log):
		self.log = log
		
		packetID = data[0:1] # get packet ID
		for x in PacketIDs.packets:
			if str(PacketIDs.packets[x]) == packetID:
				log.debug("Packet %s from client" % x)
				if x == "HANDSHAKE":
					self.packet = self.HANDSHAKE(data)
				if x == "LOGIN_REQUEST":
					self.packet = self.LOGIN_REQUEST(data)
	# FIELD TYPES
	def hexint(self, data):
		return HexToDecimal(binascii.hexlify(data)).result	
	def string16(self, data):
		r = ""
		for x in data: 
			if binascii.hexlify(x) != "00":
				r += binascii.unhexlify(binascii.hexlify(x))
		return r
	def getRidOfZero(self, data):
		r = ""
		for x in data:
			if binascii.hexlify(x) != "00":
				r += x
		return x
	
	# PACKET PARSERS
	def KEEP_ALIVE(self, data):
		return [0x00]
	def LOGIN_REQUEST(self, data):
		protocol_version = self.hexint(data[1:5]) # pv, which is currently 14 (int)
		username_len = self.hexint(data[6:8]) * 4
		username = self.string16(data[8:username_len]) # username itself (string16)
		
		print data[8:username_len]
		
		if self.getRidOfZero(data[8:username_len]) == "benbaptist":
			print "poo"
		
		return [0x01, protocol_version, username]
	def HANDSHAKE(self, data):
		length = HexToDecimal(binascii.hexlify(data[1:3])).result * 4
		r = data[4:length]; b = [r[x:x+2] for x in xrange(0,len(r),2)]; c = ""
		for x in b:
			c += binascii.a2b_hex(binascii.hexlify(x))
		c = c.strip('\x00')
		return [0x02,c]

class PacketMaker: # MAKIN PACKET WITH MY SOCKET!
	def __init__(self,array,log):
		self.log = log
		self.hexlify = binascii.hexlify
		self.unhexlify = binascii.unhexlify
		
		packetID = array[0] # get packet ID
		for x in PacketIDs.packets:
			if str(PacketIDs.packets[x]) == packetID:
				self.log.debug("Packet %s from server" % x)
				if x == "LOGIN_REQUEST":
					self.packet = self.LOGIN_REQUEST(array)
				if x == "HANDSHAKE":
					self.packet = self.HANDSHAKE(array) 
				if x == "PLAYER_POS":
					self.packet = self.PLAYER_POS(array)
				print len(self.packet)
	
	# FIELD TYPE CONVERTERS
	def double(self, data):
		z = struct.pack(">d", data)
		return z
	def floathex(self, data):
		print len(self.unhexlify(self.hexlify(struct.pack(">f", data))))
		return self.unhexlify(self.hexlify(struct.pack(">f", data)))
	def boolhex(self, data):
		if data == 1:
			return "\x01"
		else:
			return "\x00"

	# PACKET MAKERS
	def KEEP_ALIVE(self, array): #00
		return [0x00]

	def LOGIN_REQUEST(self, array): #01
		return "\x01%s" % array[1]

	def HANDSHAKE(self,array): #02
		connection_hash = array[1]
		connection_hash_ = ""; n = 0
		for x in connection_hash:
			if n % 2 == 1:
				connection_hash_ += "\x00%s" % x
			else:
				connection_hash_ += x
			n += 1
		num = struct.pack(">h", len(connection_hash))
		numf = binascii.hexlify(num)
		numf = binascii.unhexlify(numf)
		return "\x02%s%s" % (numf,connection_hash)
	
	def PLAYER_POS(self,array): # 0D 
		hexlify = self.hexlify
		
		x = self.double(array[1]) # z coord
		y = self.double(array[2]) # y coord
		s = self.double(array[3]) # stance
		z = self.double(array[4]) # z coord
		yaw = self.floathex(array[5]) # yaw hoo
		pitch = self.floathex(array[6]) # pitcher
		on_ground = self.boolhex(array[7]) # oh yessery
		
		print x
		
		return "\x0d%s%s%s%s%s%s%s" % (x, s, y, z, yaw, pitch, on_ground)