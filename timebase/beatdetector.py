import threading
import pyaudio
import copy
import numpy as np
import queue

from timebase import Timebase
from audiodata import AudioData

class BeatDetector(Timebase):
	def __init__(self, callback):
		Timebase.__init__(self)
		self.callback = callback
		self.chunks = []
		self.stream = None

	def start(self):
		pass

	def stop(self):
		pass

	def create_thread(self):
		pass

	def stream(self):
		pass

	def process(self):
		pass

	def post_data(self):
		pass