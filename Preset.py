import numpy as np

class Preset:
	def __init__(self, size=(24,24)):
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)

		for a in np.nditer(self.buffer, op_flags=['readwrite']):
			if np.random.rand() > .4:
				a[...] = 200 * np.random.rand()

	def setup(self):
		pass

	def draw(self):
		for a in np.nditer(self.buffer, op_flags=['readwrite']):
			if np.random.rand() > .4:
				a[...] = 200 * np.random.rand()

	def get_buffer(self):
		return self.buffer
