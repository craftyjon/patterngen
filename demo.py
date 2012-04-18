import pygame
import sys
from pygame.locals import *
import struct
from array import array
import zmq
import time

from message import *
from timebase.metronome import Metronome
#from timebase.beatdetector import BeatDetector
from mixer import Mixer
from outputmap import OutputMap

idx = 0
def serial_update(mixer_context):
	global ser, outmap
	#ser.write(outmap.map(mixer_context.frame))
	print outmap.map(mixer_context.frame)
	#ser.flushOutput()

def demo_update(mixer_context):
	global ser
	e = pygame.event.Event(pygame.USEREVENT, {'code':0})
	if ser is not None:
		serial_update(mixer_context)
	if not pygame.event.peek(pygame.USEREVENT):
		pygame.event.post(e)

if __name__=="__main__":
	pygame.init()

	size = width, height = 336, 320
	screen = pygame.display.set_mode(size)
	pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

	s = pygame.Surface((16,16))
	sc = pygame.Surface((320,320))

	outmap = OutputMap()
	outmap.outputs = [ [0,[1,1]], [1,[10,10]] ]

	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.connect("tcp://127.0.0.101:5443")

	try:
		import serial
		ser = serial.Serial()
		#ser.setPort("/dev/ttyUSB1")
		ser.setPort("COM13")
		ser.setBaudrate(650000)		# from testing, we are going to need a super high BR for 16x16
		# TODO: If we are using fewer than 16x16 LEDs, speed this up by mapping them
		# and only transmitting the ones we use
		try:
			ser.open()
		except serial.SerialException:
			print "Warning, could not open serial port"
			ser = None
	except:
		ser = None
	
	mixer = Mixer((16,16))
	mixer.set_timebase(Metronome)
	#mixer.set_timebase(BeatDetector)

	mixer.set_tick_callback(demo_update)

	mixer.run()
	while True:
		try:
			msg = None
			msg = socket.recv_pyobj(flags=zmq.NOBLOCK)
		except:
			pass

		if msg is not None:
			print "RPC: ", msg
			if msg == MSG_START:
				mixer.run()
			if msg == MSG_STOP:
				mixer.stop()
			if msg == MSG_BLACKOUT:
				mixer.blackout()

		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			mixer.stop()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_PERIOD:
				mixer.timebase.inject_beat()
			if event.key == pygame.K_BACKSLASH:
				mixer.timebase.toggle()
			if event.key == pygame.K_SPACE:
				mixer.next()
			if event.key == pygame.K_RIGHT:
				mixer.cut(1)
			if event.key == pygame.K_LEFT:
				mixer.cut(-1)
			if event.key == pygame.K_COMMA:
				mixer.toggle_paused()
			if event.key == pygame.K_ESCAPE or event.key== pygame.K_q:
				mixer.stop()
				sys.exit()

		if event.type == pygame.USEREVENT:
			try:
				pygame.surfarray.blit_array(s, mixer.get_frame().buffer)
			except:
				mixer.stop()
				sys.exit()

		

		sc = pygame.transform.smoothscale(s, (320,320))

		screen.blit(sc, sc.get_rect())
		screen.blit(s, (320,0))
		pygame.display.flip()