
MSG_START = 0x10
MSG_STOP = 0x11
MSG_BLACKOUT = 0x12

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

	def autoload(self, payload):
		self.payload = payload
		return self