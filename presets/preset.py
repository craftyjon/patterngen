import numpy as np

class Preset:
	def __init__(self, size=(24,24)):
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)
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

	def get_buffer(self):
		return self.buffer
