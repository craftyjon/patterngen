import numpy as np
from frame import Frame

class Preset:
	def __init__(self, size=(24,24)):
		self.size = size
		self.frame = Frame(size)
		self.is_beat = False
		self.interval = 0

	def setup(self):
		pass

	def draw(self):
		pass

	def tick(self, interval, is_beat):
		self.interval = interval
		self.is_beat = is_beat
		self.draw()

	def get_frame(self):
		return self.frame
