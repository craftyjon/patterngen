import numpy as np
from frame import Frame
from timebase.audiodata import AudioData

class Preset:
	def __init__(self, size=(24,24)):
		self.size = size
		self.frame = Frame(size)
		self.audio_data = AudioData()
		self.interval = 0

	def setup(self):
		pass

	def draw(self):
		pass

	def tick(self, interval, ad):
		self.interval = interval
		self.audio_data = ad
		self.draw()

	def get_frame(self):
		return self.frame
