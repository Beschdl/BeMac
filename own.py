import sys
import os
import pygame
import pygame.midi
import vgamepad as vg
import time
import tools
from tools import B

# init
pygame.midi.init()
i = pygame.midi.Input(2)
print(pygame.midi.get_device_info(2))
time.sleep(1)


def main():
    print("Starting")
    while True:
        if i.poll():
            tools.check(i.read(1))

main()