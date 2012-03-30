import colorsys
import numpy as np

class Point2D:
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

#	def __iadd__(self, a, b):
#		return Point2D(a.x+b.x,a.y+b.y)

	def __mul__(self, a):
		if isinstance(a,Point2D):
			return Point2D(a.x*self.x, a.y*self.y)
		else:
			return Point2D(self.x*a, self.y*a)

	def __rmul__(self, a):
		if isinstance(a,Point2D):
			return Point2D(a.x*self.x, a.y*self.y)
		else:
			return Point2D(self.x*a, self.y*a)

	def __add__(self, a):
		if isinstance(a, Point2D):
			return Point2D(a.x+self.x, a.y+self.y)
		else:
			return Point2D(self.x+a, self.y+a)

class ColorHSV:
	def __init__(self, h=0.0, s=0.0, v=0.0, dh=1.0, ds=1.0, dv=1.0):
		self.h = h
		self.s = s
		self.v = v
		self.dh = dh
		self.ds = ds
		self.dv = dv

	def set_decay_coeffs(self, dh, ds, dv):
		self.dh = dh
		self.ds = ds
		self.dv = dv

	def set_rgb(self, r, g, b):
		rf = r / 255.0
		gf = g / 255.0
		bf = b / 255.0
		(self.h, self.s, self.v) = colorsys.rgb_to_hsv(rf,gf,bf)

	def decay(self, interval):
		self.h -= 0.01 * interval * (self.dh)
		self.s -= 0.01 * interval * (self.ds)
		self.v -= 0.01 * interval * (self.dv)

	def get_rgb(self):
		(rf,gf,bf) = colorsys.hsv_to_rgb(self.h, self.s, self.v)
		return (int(255*rf),int(255*gf),int(255*bf))

	def is_dead(self):
		return (self.get_rgb() == (0,0,0))

class Particle:
	def __init__(self, pos=Point2D(), vel=Point2D(), accel=Point2D(), color=ColorHSV()):
		self.pos = pos
		self.vel = vel
		self.accel = accel
		self.color = color

	def rasterize(self):
		return (int(self.pos.x),int(self.pos.y))

	def oob(self, size):
		(x, y) = self.rasterize()
		return not((x>=0) and (x<size[0]) and (y>=0) and (y<size[1]))

	def tick(self, interval):
		self.vel = self.vel + (interval*self.accel)
		self.pos = self.pos + (interval*self.vel)
		self.color.decay(interval)


class ParticleSystem:
	def __init__(self, size=(16,16)):
		self.particles = []
		self.size = size
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)

	def add_particle(self, pos=Point2D(), vel=Point2D(), accel=Point2D(), color=ColorHSV()):
		self.particles.append(Particle(pos, vel, accel, color))

	def tick(self, interval):
		
		for particle in self.particles:
			particle.tick(interval)

	def rasterize(self, backdrop=None):
		if backdrop is not None:
			self.buffer = np.copy(backdrop)
		else:
			self.buffer = np.zeros((self.size[0], self.size[1], 3), dtype=int)
		# cull dead particles
		self.particles[:] = [particle for particle in self.particles if (not particle.color.is_dead() and not particle.oob(self.size))]

		for particle in self.particles:
			loc = particle.rasterize()
			color = particle.color.get_rgb()
			#if np.in1d(self.buffer[loc[0]][loc[1]],[0,0,0]).all():
			self.buffer[loc[0]][loc[1]][0] = color[0]
			self.buffer[loc[0]][loc[1]][1] = color[1]
			self.buffer[loc[0]][loc[1]][2] = color[2]
			#else:
			#	self.buffer[loc[0]][loc[1]][0] = int((self.buffer[loc[0]][loc[1]][0]+color[0])/2.0)
			#	self.buffer[loc[0]][loc[1]][1] = int((self.buffer[loc[0]][loc[1]][1]+color[1])/2.0)
			#	self.buffer[loc[0]][loc[1]][2] = int((self.buffer[loc[0]][loc[1]][2]+color[2])/2.0)
		return self.buffer