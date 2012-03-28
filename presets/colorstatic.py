import numpy as np
from preset import Preset

class ColorStatic(Preset):
	def __init__(self, size=(24,24)):
		Preset.__init__(self, size)

		#for a in np.nditer(self.buffer, op_flags=['readwrite']):
		#	if np.random.rand() > .4:
		#		a[...] = 100 * np.random.rand()

	def draw(self):
		for a in np.nditer(self.buffer, op_flags=['readwrite']):
			a[...] = int(a * 0.9)
			r = np.random.rand()
			if self.is_beat:
				if r> .9:
					a[...] = min(255,a + 200+50 * np.random.rand())
			else:
				if r>.8:
					a[...] = min(255,a + 10+30 * np.random.rand())
