import numpy as np
from particle import *
from frame import Frame
from preset import Preset

class ParticleTest(Preset):
	def __init__(self, size=(24,24)):
		Preset.__init__(self, size)
		self.size = size
		self.ps = ParticleSystem(size)
		self.backdrop = Frame(size)
		self.backdrop_hs = 0.0
		self.backdrop_hd = 1
		self.pe1 = ParticleEmitter(pos=Point2D(0,0))
		self.pe2 = ParticleEmitter(pos=Point2D(23,23))
		self.pe1.set_vel(Point2D(18,1.1))
		self.pe2.set_vel(Point2D(-18,-1.1))
		self.pe1.set_color(ColorHSV(1.0,1.0,1.0,(lambda c: (c.pos.x/24.0)),0,10))
		self.pe2.set_color(ColorHSV(1.0,1.0,1.0,(lambda c: (c.pos.x/24.0)),0,10))
		self.pe1.bind(self.ps)
		self.pe2.bind(self.ps)

	def draw(self):
		self.backdrop_hs += 0.01
		if self.audio_data.is_beat:# or np.random.rand() > 0.8:
			#self.backdrop_hd *= -1
			for n in range(5):
				self.pe1.set_accel(Point2D(-9-2*np.random.rand(),2+10*np.random.rand()))
				self.pe2.set_accel(Point2D(10-2*np.random.rand(),-2-10*np.random.rand()))
				self.pe1.emit()
				self.pe2.emit()
				#self.ps.add_particle(pos=Point2D(0,0),vel=Point2D(15+2*np.random.rand(),1+2*np.random.rand()),accel=Point2D(-9-2*np.random.rand(),2+10*np.random.rand()),color=ColorHSV(1.0,1.0,1.0,(lambda c: (c.pos.x/24.0)),0,10))
				#self.ps.add_particle(pos=Point2D(23,23),vel=Point2D(-15+2*np.random.rand(),-2-3*np.random.rand()),accel=Point2D(10+2*np.random.rand(),-2-10*np.random.rand()),color=ColorHSV(1.0,1.0,1.0,(lambda c: (c.pos.x/24.0)),0,10))
				#self.ps.add_particle(pos=Point2D(23,23),vel=Point2D(-5-2*np.random.rand(),-7-2*np.random.rand()),accel=Point2D(-4-10*np.random.rand(),-3-2*np.random.rand()),color=ColorHSV(0.6,1.0,1.0,100,2.5,40))

		for x in range(self.size[0]):
			for y in range(self.size[1]):
				el = self.backdrop.buffer[x][y]
				hue = (float(x) * self.backdrop_hd / self.size[0]) + self.backdrop_hs
				(rf,gf,bf) = colorsys.hsv_to_rgb(hue, 1.0, 0.3)
				(el[0],el[1],el[2]) = (int(rf*255),int(gf*255),int(bf*255))

		self.ps.tick(self.interval)
		
		self.frame = self.backdrop.compose(self.ps.rasterize())