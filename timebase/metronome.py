from timebase import Timebase
from threading import Timer

class Metronome(Timebase):
	def __init__(self, callback):
		Timebase.__init__(self)
		self.interval = 0.5
		self.callback = callback
		self.timer = Timer(self.interval, self.on_tick)
		self.timer.daemon = True
		self.beat = False

	def start(self):
		self.timer.start()

	def stop(self):
		if self.timer is not None:
			self.timer.cancel()
			self.timer.join()

	def is_beat(self):
		if self.beat:
			self.beat = False
			return True
		else:
			return False

	def on_tick(self):
		#self.callback(self.interval)
		self.beat = True
		self.timer = Timer(self.interval, self.on_tick).start()