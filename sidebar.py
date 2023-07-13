from consts import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class Sidebar:
    def __init__(self, width):
        self.width = width
    
    def draw(self, win: pygame.surface.Surface):
        pygame.draw.rect(win, COLOURS["black"], pygame.rect.Rect(0, 0, self.width, HEIGHT))

    def update(self):
        pass
    