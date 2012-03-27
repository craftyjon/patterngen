import pygame
import sys
from pygame.locals import *
import colorsys

from Preset import Preset
#from CirclePreset import CirclePreset

pygame.init()

size = width, height = 344, 320

screen = pygame.display.set_mode(size)

s = pygame.Surface((24,24))
sc = pygame.Surface((320,320))
p = Preset((24,24))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	pygame.surfarray.blit_array(s, p.get_buffer())

	sc = pygame.transform.smoothscale(s, (320,320))

	screen.blit(sc, sc.get_rect())
	screen.blit(s, (320,0))
	pygame.display.flip()