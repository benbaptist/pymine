from logger import Logger
from hex import HexToDecimal
import binascii
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
		'CHAT_MESSAGE': '\x03'
	}
class PacketParser:
	def __init__(self,data,log):
		self.log = log
		
		packetID = data[0:1] # get packet ID
		for x in PacketIDs.packets:
			if str(PacketIDs.packets[x]) == packetID:
				log.debug("Packet %s from client" % x)
				if x == "HANDSHAKE":
					self.HANDSHAKE(data)
	def KEEP_ALIVE(data):
		return [0x00]
	def LOGIN_REQUEST(data):
		pass
	def HANDSHAKE(self,data):
		length=HexToDecimal(binascii.hexlify(data[1:3])).result*2
		username_hex = binascii.hexlify(data[4:length])
		username = data[4:length]
		
		#log.debug("Username: %s" % username)
		return [0x02,username]