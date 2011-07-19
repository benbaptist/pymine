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
	def __init__(self,data,log):
		self.log = log
		
		packetID = data[0:1] # get packet ID
		for x in PacketIDs.packets:
			if str(PacketIDs.packets[x]) == packetID:
				log.debug("Packet %s from client" % x)
				if x == "HANDSHAKE":
					self.packet = self.HANDSHAKE(data)
	def KEEP_ALIVE(data):
		return [0x00]
	def LOGIN_REQUEST(data):
		pass
	def HANDSHAKE(self,data):
		length = HexToDecimal(binascii.hexlify(data[1:3])).result*4
		r = data[4:length]; b = [r[x:x+2] for x in xrange(0,len(r),2)]; c = ""
		for x in b:
			c += binascii.a2b_hex(binascii.hexlify(x))
		c = c.strip('\x00')
		return [0x02,c]
		
class PacketMaker:
	def __init__(self,array,log):
		self.log = log
		
		packetID = array[0] # get packet ID
		for x in PacketIDs.packets:
			if str(PacketIDs.packets[x]) == packetID:
				self.log.debug("Packet %s from server" % x)
				if x == "HANDSHAKE":
					self.packet = self.HANDSHAKE(array) 
				if x == "PLAYER_POS":
					self.packet = self.PLAYER_POS(array)
	def KEEP_ALIVE(self,array):
		return ""
	def LOGIN_REQUEST(self,array):
		pass
	def HANDSHAKE(self,array):
		connection_hash = array[1]
		connection_hash_ = ""; n = 0
		for x in connection_hash:
			if n % 2 == 1:
				connection_hash_ += "\x00%s" % x
			else:
				connection_hash_ += x
			n += 1
		num = struct.pack(">h", len(connection_hash))
		return "\x02%s%s" % (num,connection_hash)
	def PLAYER_POS(self,array):
		x = struct.pack(">d", len(array[1]))
		y = struct.pack(">d", len(array[2]))
		stance = struct.pack(">d", len(array[3]))
		z = struct.pack(">d", len(array[4]))
		yaw = struct.pack(">f", len(array[5]))
		pitch = struct.pack(">f", len(array[6]))
		on_ground = array[7]
		if on_ground == 0: on_ground = "\x00"
		else: on_ground = "\x01"
		return "\x0d%s.%s.%s.%s.%s.%s.%s" % (x, stance, y, z, yaw, pitch, on_ground)