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
		self.running = False

	def start(self):
		self.running = True
		self.timer = Timer(self.interval, self.on_tick)
		self.timer.start()

	def stop(self):
		self.running = False
		if self.timer is not None:
			#self.timer.cancel()
			self.timer.join()

	def toggle(self):
		if self.running == True:
			self.stop()
		else:
			self.start()

	def is_beat(self):
		if self.beat:
			self.beat = False
			return True
		else:
			return False

	def inject_beat(self):
		self.beat = True

	def on_tick(self):
		#self.callback(self.interval)
		self.beat = True
		if self.running == True:
			self.timer = Timer(self.interval, self.on_tick)
			self.timer.daemon = True
			self.timer.start()
