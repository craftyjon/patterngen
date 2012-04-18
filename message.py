
MSG_START = 0x10
MSG_STOP = 0x11
MSG_BLACKOUT = 0x12
MSG_GET_STATUS = 0x13
MSG_PLAYPAUSE = 0x14

class Message:
	def __init__(self, pl=None):
		self.payload = pl

	def __repr__(self):
		return "[Message] "+hex(self.payload)

	#def __str__(self):
	#	return self.__repr__()

	def __eq__(self, other):
		if isinstance(other, Message):
			return (self.payload == other.payload)
		else:
			return (self.payload == other)

	def get_cmd(self, cmd):
		self.payload = cmd
		return {'cmd': cmd}