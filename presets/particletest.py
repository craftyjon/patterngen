import numpy as np
from particle import *
from preset import Preset

class ParticleTest(Preset):
	def __init__(self, size=(24,24)):
		Preset.__init__(self, size)
		self.size = size
		self.ps = ParticleSystem(size)
		self.backdrop = np.copy(self.buffer)
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				el = self.backdrop[x][y]
				hue = (float(x) / self.size[0])*0.05 + 0.6
				(rf,gf,bf) = colorsys.hsv_to_rgb(hue, 1.0, 0.2)
				(el[0],el[1],el[2]) = (int(rf*255),int(gf*255),int(bf*255))

	def draw(self):
		if self.is_beat:# or np.random.rand() > 0.8:
			for n in range(5):
				self.ps.add_particle(pos=Point2D(0,0),vel=Point2D(5+2*np.random.rand(),7+2*np.random.rand()),accel=Point2D(5,2),color=ColorHSV(1.0,1.0,1.0,2.5,4.5,10))
				self.ps.add_particle(pos=Point2D(23,23),vel=Point2D(-5-2*np.random.rand(),-7-2*np.random.rand()),accel=Point2D(-4,-3),color=ColorHSV(0.255,1.0,1.0,2.5,4.5,10))

		self.ps.tick(self.interval)
		
		self.buffer = self.ps.rasterize(self.backdrop)