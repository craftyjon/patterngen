import numpy as np
from threading import Timer
import inspect
import time

from frame import Frame
import presets

class Mixer:
	def __init__(self, size=(24,24)):
		self.size = size
		self.frame = Frame(size)
		self.presets = []
		self.timebase = None
		self.draw_interval = 0.005
		self.draw_timer = Timer(self.draw_interval, self.on_tick)
		self.draw_timer.daemon = True
		self.active_preset = 0
		self.next_preset = 1
		self.loaded_preset = 1
		self.running = False
		self.paused = False
		self.hard_cut = False
		self.in_transition = False
		self.preset_time = 8.0
		self.transition_time = 1.25
		self.transition_state = 0.0
		self.preset_runtime = 0.0
		self.time = 0.0
		self.last_time = 0.0
		self.time_delta = 0.0
		self.tick_callback = None
	
		for name,obj in inspect.getmembers(presets, inspect.isclass):
			#try:
			self.presets.append(obj(self.size))
			#except:
			#	print str(e)
			#	print "Error loading preset "+name+"!"

	def run(self):
		self.last_time = time.time()
		self.draw_timer.start()
		self.running = True
		if self.timebase is not None:
			self.timebase.start()

	def stop(self):
		self.running = False
		if self.draw_timer is not None:
			self.draw_timer.cancel()
			self.draw_timer.join()
		self.timebase.stop()

	def set_tick_callback(self, cb):
		self.tick_callback = cb

	def on_tick(self):
		if not self.running:
			return False
		beat = self.timebase.is_beat()
		self.time_delta = time.time() - self.last_time
		self.last_time = time.time()
		if self.preset_runtime >= self.preset_time:
			self.preset_runtime = 0.0
			self.next()

		if self.in_transition:
			if self.hard_cut is True and beat is True:
				self.cut(1)
				self.presets[self.active_preset].tick(self.time_delta, True)
			else:
				if beat is True or self.transition_state > 0.0:	#delay start until beat
					self.transition_state += self.time_delta
					if self.transition_state >= self.transition_time:
						self.in_transition = False
						t = self.active_preset
						self.active_preset = self.next_preset
						self.next_preset = t
				self.presets[self.active_preset].tick(self.time_delta, beat)
				self.presets[self.next_preset].tick(self.time_delta, beat)
		else:
			self.preset_runtime += self.time_delta
			self.presets[self.active_preset].tick(self.time_delta, beat)

		self.draw()

		if self.tick_callback is not None:
			self.tick_callback(self)

		self.draw_timer = Timer(self.draw_interval, self.on_tick).start()

	def set_timebase(self, timebase):
		self.timebase = timebase(self.on_tick)

	def toggle_paused(self):
		self.paused = not self.paused

	def draw(self):
		if self.in_transition is True:
			oldframe = self.presets[self.active_preset].get_frame() * (1.0 - (self.transition_state/self.transition_time))
			newframe = self.presets[self.next_preset].get_frame() * (self.transition_state/self.transition_time)
			self.frame = oldframe + newframe
		else:
			self.frame = self.presets[self.active_preset].get_frame()

	def next(self):
		if self.in_transition == True or self.paused == True or len(self.presets) < 2:
			return False
		self.next_preset = (self.active_preset + 1) % len(self.presets)
		self.in_transition = True
		self.transition_state = 0.0

	def cut(self, delta):
		self.active_preset = (self.active_preset + delta) % len(self.presets)
		self.in_transition = False
		self.preset_runtime = 0.0

	def get_frame(self):
		return self.frame