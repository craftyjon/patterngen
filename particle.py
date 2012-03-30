import colorsys

class Point2D:
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

	def __iadd__(self, a, b):
		return Point2D(a.x+b.x,a.y+b.y)

	def __mul__(self, a, b):
		return Point2D(a.x*b.x, a.y*b.y)

	def __sub__(self, a, b):
		return Point2D(a.x-b.x, a.y-b.y)

	def __add__(self, a, b):
		return Point2D(a.x+b.x, a.y+b.y)

	def __abs__(self):
		return Point2D(abs(self.x),abs(self.y))

class Vector2D:
	def __init__(self, dx=0.0, dy=0.0):
		self.dx = dx
		self.dy = dy

	def __iadd__(self, a, b):
		return Vector2D(a.dx+b.dx,a.dy+b.dy)

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

	def decay(self):
		self.h = self.h * (self.dh)
		self.s = self.s * (self.ds)
		self.v = self.v * (self.dv)

	def get_rgb(self):
		(rf,gf,bf) = colorsys.hsv_to_rgb(self.h, self.s, self.v)
		return (int(255*rf),int(255*gf),int(255*bf))

class Particle:
	def __init__(self, pos=Point2D(), vel=Point2D(), accel=Point2D(), color=ColorHSV()):
		self.pos = pos
		self.vel = vel
		self.accel = accel
		self.color = color

	def rasterize(self):
		return (int(self.pos.x),int(self.pos.y))

	def tick(self, interval):
		self.vel += (interval*self.accel)
		self.pos += (interval*self.vel)
		self.color.decay()


class ParticleSystem:
	def __init__(self):
		self.particles = []

	def add_particle(self, pos=Point2D(), vel=Point2D(), accel=Point2D(), color=ColorHSV()):
		self.particles.append(Particle(pos, vel, accel, color))