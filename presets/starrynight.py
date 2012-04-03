import numpy as np
import colorsys
from preset import Preset

class StarryNight(Preset):
	def __init__(self, size=(24,24)):
		Preset.__init__(self, size)
		self.size = size
		self.stars = np.zeros((size[0],size[1],2), dtype=float)

	def draw(self):
		if self.audio_data.is_beat or np.random.rand() > 0.8:
			for i in range(2+3*self.audio_data.is_beat):
				self.stars[int(np.random.rand()*self.size[0])][int(np.random.rand()*self.size[1])] = [(0.3 + (0.7*self.audio_data.is_beat)),0.7 + ((np.random.rand()*0.1)-0.05)]

		for x in range(self.size[0]):
			for y in range(self.size[1]):
				el = self.frame.buffer[x][y]

				#hue = 0.7 + ((np.random.rand()*0.1)-0.05)
				hue = self.stars[x][y][1]
				sat = self.stars[x][y][0]

				(rf,gf,bf) = colorsys.hsv_to_rgb(hue, 0.5+(0.5*sat), sat)
				(el[0],el[1],el[2]) = (int(rf*255),int(gf*255),int(bf*255))

				self.stars[x][y][0] *= 0.99