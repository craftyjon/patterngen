import pygame
import sys
from pygame.locals import *
import colorsys

from timebase.metronome import Metronome
from presets.colorstatic import ColorStatic
from mixer import Mixer

if __name__=="__main__":
	pygame.init()

	size = width, height = 344, 320
	screen = pygame.display.set_mode(size)

	f = pygame.font.SysFont("sans", 14)

	#fps counter
	last = 0
	count = 0
	now = pygame.time.get_ticks()
	fps_surface = f.render("fps: %d" % last, True, (255,255,255), (0,0,0))


	s = pygame.Surface((24,24))
	sc = pygame.Surface((320,320))
	
	mixer = Mixer((24,24))
	mixer.load_preset(ColorStatic)
	mixer.set_timebase(Metronome)

	mixer.run()


	while 1:
		start_time = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mixer.stop()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_PERIOD:
					mixer.timebase.inject_beat()
				if event.key == pygame.K_BACKSLASH:
					mixer.timebase.toggle()

		pygame.surfarray.blit_array(s, mixer.get_buffer())

		sc = pygame.transform.smoothscale(s, (320,320))

		screen.blit(sc, sc.get_rect())
		screen.blit(s, (320,0))

		count += 1
		if pygame.time.get_ticks() - now > 100.0:
			now = pygame.time.get_ticks()
			last = count
			count = 0
			#print("fps:",last)
			fps_surface = f.render("fps: %d" % (last*10), True, (255,255,255), (0,0,0))
		screen.blit(fps_surface, (0,0))

		pygame.display.flip()

		