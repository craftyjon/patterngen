import pygame
import sys
from pygame.locals import *
import struct

from timebase.metronome import Metronome
from mixer import Mixer

idx = 0
def serial_update(mixer_context):
	global ser
	arr = mixer_context.buffer
	data = struct.pack("BBBBBBBB", 0, arr[idx][idx][0], arr[idx][idx][1], arr[idx][idx][2], 1, arr[idx+1][idx+1][0], arr[idx+1][idx+1][1], arr[idx+1][idx+1][2])
	ser.write(data)
	#ser.flushOutput()

def demo_update(mixer_context):
	global ser
	e = pygame.event.Event(pygame.USEREVENT, {'code':0})
	if ser is not None:
		serial_update(mixer_context)
	pygame.event.post(e)

if __name__=="__main__":
	pygame.init()

	size = width, height = 344, 320
	screen = pygame.display.set_mode(size)

	s = pygame.Surface((24,24))
	sc = pygame.Surface((320,320))

	try:
		import serial
		ser = serial.Serial()
		ser.setPort("/dev/ttyUSB1")
		ser.setBaudrate(115200)
		try:
			ser.open()
		except serial.SerialException:
			print "Warning, could not open serial port"
			ser = None
	except:
		ser = None
	
	mixer = Mixer((24,24))
	mixer.set_timebase(Metronome)

	#if ser is not None:
	#	mixer.set_tick_callback(serial_update)

	mixer.set_tick_callback(demo_update)

	mixer.run()

	while 1:
		#for event6 in pygame.event.get():
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