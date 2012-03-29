import numpy as np
from threading import Timer

class Mixer:
	def __init__(self, size=(24,24)):
		self.size = size
		self.buffer = np.zeros((size[0], size[1], 3), dtype=int)
		self.presets = [None, None, None]
		self.timebase = None
		self.draw_interval = 0.005
		self.draw_timer = Timer(self.draw_interval, self.on_tick)
		self.draw_timer.daemon = True
		self.active_preset = 0
		self.next_preset = 1
		self.loaded_preset = 1
		self.running = False
		self.hard_cut = False
		self.in_transition = False
		self.preset_time = 10.0
		self.transition_time = 0.25
		self.transition_state = 0.0
		self.time = 0.0
		self.tick_callback = None

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
			self.presets[self.active_preset].tick(self.draw_interval, beat)
		self.draw()
		if self.tick_callback is not None:
			self.tick_callback(self)
		self.draw_timer = Timer(self.draw_interval, self.on_tick).start()

	def set_timebase(self, timebase):
		self.timebase = timebase(self.on_tick)

	def load_preset(self, preset):
		if self.in_transition is True:
			return False	# TODO make this better by adding a third temporary preset
		if self.presets[0] is None and self.presets[1] is None:
			self.presets[0] = preset(self.size)
			self.active_preset = 0
		else:
			if self.active_preset == 0:
				self.presets[1] = preset(self.size)
			else:
				self.presets[0]= preset(self.size)

	def draw(self):
		if self.in_transition is True:
			oldbuffer = (1.0 - (self.transition_state/self.transition_time)) * self.presets[self.active_preset].get_buffer()
			newbuffer = (self.transition_state/self.transition_time) * self.presets[self.next_preset].get_buffer()

			#print oldbuffer
			#print newbuffer
			self.buffer = oldbuffer.astype('B') + newbuffer.astype('B')
			
			#self.buffer = ((1.0 - self.transition_state) * self.presets[self.active_preset].get_buffer())
			#self.buffer += (self.transition_state) * self.presets[self.next_preset].get_buffer()
			#it = np.nditer(self.buffer, flags=['multi_index'], op_flags=['writeonly'])
			#while not it.finished:	
			#	it[0] = int(((1.0 - (self.transition_state/self.transition_time)) * oldbuffer[it.multi_index[0]][it.multi_index[1]]) + (self.transition_state/self.transition_time)*newbuffer[it.multi_index[0]][it.multi_index[1]])
			#	it.iternext()
		else:
			self.buffer = self.presets[self.active_preset].get_buffer()

	def next(self):
		if self.in_transition == True:
			return False
		if self.active_preset == 0:
			self.next_preset = 1
		else:
			self.next_preset = 0
		self.in_transition = True
		self.transition_state = 0.0

	def get_buffer(self):
		return self.buffer