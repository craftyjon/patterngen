import numpy as np
from preset import Preset

class ColorStatic(Preset):
	def __init__(self, size=(24,24)):
		Preset.__init__(self, size)

		for a in np.nditer(self.buffer, op_flags=['readwrite']):
			if np.random.rand() > .4:
				a[...] = 100 * np.random.rand()

	def draw(self):
		for a in np.nditer(self.buffer, op_flags=['readwrite']):
			a[...] = a * 0.85
			if np.random.rand() > .9:
				if self.is_beat:
					a[...] = 200+155 * np.random.rand()
				else:
					a[...] = 100 * np.random.rand()
