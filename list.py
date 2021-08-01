import pygame
import pygame.midi
from pygame.locals import *

pygame.midi.init()

count = pygame.midi.get_count()

print("Number of devices: " + str(count))


for i in range(count):
    print(pygame.midi.get_device_info(i))