import pygame
import sys
from pygame.locals import *
import colorsys
from threading import Timer

from Preset import Preset
#from CirclePreset import CirclePreset

def on_tick():
	global tick_timer, p
	p.draw()
	tick_timer = Timer(0.5, on_tick).start()


if __name__=="__main__":
	pygame.init()

	size = width, height = 344, 320

	screen = pygame.display.set_mode(size)

	#fps counter
	last = 0
	count = 0
	now = pygame.time.get_ticks()

	tick_timer = Timer(0.5, on_tick)

	s = pygame.Surface((24,24))
	sc = pygame.Surface((320,320))
	p = Preset((24,24))

	tick_timer.daemon = True
	tick_timer.start()

	while 1:
		start_time = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		pygame.surfarray.blit_array(s, p.get_buffer())

		sc = pygame.transform.smoothscale(s, (320,320))

		screen.blit(sc, sc.get_rect())
		screen.blit(s, (320,0))
		pygame.display.flip()

		count += 1
		if pygame.time.get_ticks() - now > 1000.0:
			now = pygame.time.get_ticks()
			last = count
			count = 0
			print("fps:",last)