import numpy as np

class Frame:
	def __init__(self, size):
		self.size = size
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)

	def __add__(self, other):
		"""Adding performs mixing of two buffers"""
		if self.size != other.size:
			raise Exception("You can only add two frames of the same dimensions!")
		new = Frame(self.size)
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				new.buffer[x][y][0] = min(255, (self.buffer[x][y][0] + other.buffer[x][y][0]))
				new.buffer[x][y][1] = min(255, (self.buffer[x][y][1] + other.buffer[x][y][1]))
				new.buffer[x][y][2] = min(255, (self.buffer[x][y][2] + other.buffer[x][y][2]))
		return new

	def compose(self, other):
		"""Performs compositing away from black (since we have no alpha support right now).  A + B means A's pixels, replaced by any of B's pixels that aren't black."""
		if self.size != other.size:
			raise Exception("You can only compose two frames of the same dimensions!")
		new = Frame(self.size)
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				new.buffer[x][y] = self.buffer[x][y]
				if other.buffer[x][y][0] > 0:
					new.buffer[x][y][0] = other.buffer[x][y][0]
				if other.buffer[x][y][1] > 0:
					new.buffer[x][y][1] = other.buffer[x][y][1]
				if other.buffer[x][y][2] > 0:
					new.buffer[x][y][2] = other.buffer[x][y][2]
		return new

	def __mul__(self, other):
		new = Frame(self.size)
		new.buffer = other * self.buffer
		return new

	def clear(self):
		self.buffer = np.zeros((self.size[0], self.size[1], 3), dtype=int)


