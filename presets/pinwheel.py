import numpy as np
import colorsys
import math
from preset import Preset

class Pinwheel(Preset):
	def __init__(self, size=(24,24)):
		Preset.__init__(self, size)
		self.size = size
		self.rot  = 0.0
		self.center = (size[0]/2,size[1]/2)
		self.max_radius = math.sqrt((((size[0]/2)^2) +  ((size[1]/2)^2)))

	def draw(self):
		self.rot += self.interval * (1 + 50*self.is_beat)
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				el = self.frame.buffer[x][y]

				angle = math.atan2(self.center[1] - y, self.center[0] - x) + (self.rot)
				dx = abs(self.center[0] - x)
				dy = abs(self.center[1] - y)

				r = math.sqrt((dx^2) + (dy^2))

				hue = 0.5 + (angle / (2*math.pi))

				value = 1.0# - (r / self.max_radius)

				(rf,gf,bf) = colorsys.hsv_to_rgb(hue, 1.0, value)
				(el[0],el[1],el[2]) = (int(rf*255),int(gf*255),int(bf*255))