import numpy as np
from threading import Timer

class Mixer:
	def __init__(self, size=(24,24)):
		self.size = size
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)
		self.preset_0 = None
		self.preset_1 = None
		self.timebase = None
		self.draw_timer = Timer(0.033, self.on_tick)
		self.draw_timer.daemon = True
		self.active_preset = self.preset_0
		self.running = False
		self.hard_cut = True
		self.in_transition = False
		self.preset_time = 10.0
		self.transition_time = 1.0
		self.time = 0.0

	def run(self):
		self.draw_timer.start()
		if self.timebase is not None:
			self.timebase.start()

	def stop(self):
		if self.draw_timer is not None:
			self.draw_timer.cancel()
		self.timebase.stop()

	def on_tick(self):
		self.active_preset.tick(0.033, self.timebase.is_beat())
		self.draw()
		self.draw_timer = Timer(0.033, self.on_tick).start()

	def set_timebase(self, timebase):
		self.timebase = timebase(self.on_tick)

	def load_preset(self, preset):
		if self.preset_0 is None and self.preset_1 is None:
			self.preset_0 = preset(self.size)
			self.active_preset = self.preset_0
		else:
			if self.active_preset == self.preset_0:
				self.preset_1 = preset(self.size)
			else:
				self.preset_0 = preset(self.size)

	def draw(self):
		self.buffer = self.active_preset.get_buffer()

	def next(self):
		pass

	def get_buffer(self):
		return self.buffer