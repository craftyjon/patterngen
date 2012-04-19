import colorsys
import numpy as np
import copy

from frame import Frame

class Point2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

#    def __iadd__(self, a, b):
#        return Point2D(a.x+b.x,a.y+b.y)

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
        self.parent = None

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
        if callable(self.dh):
            self.h = self.dh(self.parent)
        else:
            self.h -= 0.01 * interval * (self.dh)
        if callable(self.ds):
            self.s = self.ds(self.parent)
        else:
            self.s -= 0.01 * interval * (self.ds)
        if callable(self.dv):
            self.v = self.dv(self.parent)
        else:
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
        self.color.parent = self

    def rasterize(self):
        #TODO: Add rasterization modes: quantize (default, below), blend (not implemented), etc
        return (int(self.pos.x),int(self.pos.y))

    def tick(self, interval):
        if callable(self.accel):
            self.vel = self.vel + self.accel(self)
        else:
            self.vel = self.vel + (interval*self.accel)

        self.pos = self.pos + (interval*self.vel)
        self.color.decay(interval)


# TODO: Make a particle emitter to simplify code on the preset side
class ParticleEmitter:
    def __init__(self, pos=Point2D()):
        self.pos = pos
        self.particle = Particle(pos=pos)
        self.ps = None

    def set_vel(self, vel=Point2D()):
        self.particle.vel = vel

    def set_accel(self, accel=Point2D()):
        self.particle.accel = accel

    def set_color(self, color=ColorHSV()):
        self.particle.color = color
        self.particle.color.parent = self.particle

    def bind(self, ps):
        self.ps = ps

    def emit(self, n=1):
        for i in range(n):
            self.ps.add_particle(copy.deepcopy(self.particle))


class ParticleSystem:
    def __init__(self, size=(16,16)):
        self.particles = []
        self.size = size
        self.frame = Frame(size)

    def add_particle(self, particle=None, pos=Point2D(), vel=Point2D(), accel=Point2D(), color=ColorHSV()):
        if particle is not None:
            self.particles.append(particle)
        else:
            self.particles.append(Particle(pos, vel, accel, color))

    def tick(self, interval):
        for particle in self.particles:
            particle.tick(interval)

    def cull(self, particle):
        (x, y) = particle.rasterize()
        return not((x>=0) and (x<self.size[0]) and (y>=0) and (y<self.size[1]))

    def is_particle_dead(self, particle):
        if particle.color.is_dead():
            return True
        (x, y) = particle.rasterize()
        if (x < (-10)) or (x > (self.size[0]+10)) or (y < (-10)) or (y > (self.size[1]+10)):
            return True
        return False

    def rasterize(self):
        self.frame.clear()
        # delete dead particles
        self.particles[:] = [particle for particle in self.particles if not self.is_particle_dead(particle)]
        # cull offscreen particles
        renderlist = [particle for particle in self.particles if not self.cull(particle)]

        for particle in renderlist:
            loc = particle.rasterize()
            color = particle.color.get_rgb()

            self.frame.buffer[loc[0]][loc[1]][0] = color[0]
            self.frame.buffer[loc[0]][loc[1]][1] = color[1]
            self.frame.buffer[loc[0]][loc[1]][2] = color[2]

        return self.frame