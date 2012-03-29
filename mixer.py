import numpy as np
from threading import Timer
import inspect

import presets

class Mixer:
	def __init__(self, size=(24,24)):
		self.size = size
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)
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
		self.preset_time = 1.0
		self.transition_time = 0.25
		self.transition_state = 0.0
		self.preset_runtime = 0.0
		self.time = 0.0
		self.tick_callback = None
	
		for name,obj in inspect.getmembers(presets, inspect.isclass):
			try:
				self.presets.append(obj(self.size))
			except:
				print "Error loading preset "+name+"!"

	def run(self):
		self.draw_timer.start()
		if self.timebase is not None:
			self.timebase.start()

	def stop(self):
		if self.draw_timer is not None:
			self.draw_timer.cancel()
		self.timebase.stop()

	def set_tick_callback(self, cb):
		self.tick_callback = cb

	def on_tick(self):
		beat = self.timebase.is_beat()

		if self.preset_runtime >= self.preset_time:
			self.preset_runtime = 0.0
			self.next()

		if self.in_transition:
			if self.hard_cut is True and beat is True:
				self.active_preset = self.next_preset
				self.in_transition = False
				self.presets[self.active_preset].tick(self.draw_interval, True)
			else:
				if beat is True or self.transition_state > 0.0:	#delay start until beat
					self.transition_state += self.draw_interval
					if self.transition_state >= self.transition_time:
						self.in_transition = False
						t = self.active_preset
						self.active_preset = self.next_preset
						self.next_preset = t
				self.presets[self.active_preset].tick(self.draw_interval, beat)
				self.presets[self.next_preset].tick(self.draw_interval, beat)
		else:
			self.preset_runtime += self.draw_interval
			self.presets[self.active_preset].tick(self.draw_interval, beat)

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
			oldbuffer = (1.0 - (self.transition_state/self.transition_time)) * self.presets[self.active_preset].get_buffer()
			newbuffer = (self.transition_state/self.transition_time) * self.presets[self.next_preset].get_buffer()
			self.buffer = oldbuffer.astype('B') + newbuffer.astype('B')
		else:
			self.buffer = self.presets[self.active_preset].get_buffer()

	def next(self):
		if self.in_transition == True or self.paused == True:
			return False
		self.next_preset = (self.active_preset + 1) % len(self.presets)
		self.in_transition = True
		self.transition_state = 0.0

	def cut(self, delta):
		self.active_preset = (self.active_preset + delta) % len(self.presets)
		self.in_transition = False
		self.preset_runtime = 0.0

	def get_buffer(self):
		return self.buffer