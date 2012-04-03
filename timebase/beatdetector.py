import threading
import pyaudio
import struct
import scipy
import scipy.fftpack
import scipy.signal
import math
import copy
import numpy as np
import Queue
import matplotlib.pyplot as plt


from timebase import Timebase
from audiodata import AudioData

class BeatDetector(Timebase):
	def __init__(self, callback):
		Timebase.__init__(self)
		self.callback = callback
		self.chunks = []
		self.stream = None
		self.input_thread_id = None
		self.process_thread_id = None
		self.sample_rate = 48000
		self.buffer_size = 2**12
		self.pyaudio = pyaudio.PyAudio()
		self.q = Queue.Queue(maxsize=1024)
		self.shutdown_event = threading.Event()
		self.data_event = threading.Event()
		self.demo_data = []
		self.ffty = []
		self.fftx = []

	def start(self):
		self.create_input_thread()
		self.create_process_thread()

	def stop(self):
		self.shutdown_event.set()
		#self.process_thread_id.join()
		#self.input_thread_id.join()

	def create_input_thread(self):
		self.stream = self.pyaudio.open(format=pyaudio.paInt16,channels=1,rate=self.sample_rate,input=True,frames_per_buffer=self.buffer_size)
		self.input_thread_id = threading.Thread(target=self.input_thread).start()

	def input_thread(self):
		while not self.shutdown_event.is_set():
			if not self.q.full():
				self.q.put(self.stream.read(self.buffer_size))

	def create_process_thread(self):
		self.process_thread_id = threading.Thread(target=self.process).start()

	def process(self):
		while not self.shutdown_event.is_set():
			packet = self.q.get(block=True)
			#print str(packet)
			self.demo_data=scipy.array(struct.unpack("%dh"%(self.buffer_size),packet))

			decimated = scipy.signal.decimate(self.demo_data, 16, ftype='fir')
			ffty = np.fft.fft(decimated)
			fftx = scipy.fftpack.fftfreq(self.buffer_size / 16, 16.0 / self.sample_rate)

			self.fftx = fftx[0:len(fftx)/2]
			self.ffty = abs(ffty[0:len(ffty)/2])/1000

			self.data_event.set()

	def post_data(self):
		pass

	def get_data(self):
		print int(self.demo_data)

def cbf(callback_context):
	pass

if __name__=="__main__":

	bd = BeatDetector(cbf)
	bd.start()

	bd.data_event.wait()
	bd.data_event.clear()

	#bd.stop()

	#print bd.demo_data

	#line, = pylab.plot(bd.demo_data)
	#pylab.autoscale()
	#pylab.draw()


	for i in range(20):
		bd.data_event.wait()
		bd.data_event.clear()
		print bd.demo_data[0]
		#line.set_ydata(bd.demo_data)
		#pylab.autoscale()
		raw_input(".")
		#pylab.draw()

	bd.stop()
	print len(bd.fftx)
	print len(bd.ffty)
	line, = plt.plot(bd.fftx,bd.ffty)
	#plt.plot(bd.demo_data)
	plt.show()