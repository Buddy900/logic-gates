import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from consts import *


class Movable:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.offset = (0, 0)
        self.moving = False
        self.start_pos = None
        self.width = max(
            NODE_FONT.render(self.name, 1, COLOURS["white"]).get_width() + 40,
            self.width,
        )
    
    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        return False
    
    def start_move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.offset = (mouse_x - self.x, mouse_y - self.y)
        self.moving = True
        self.start_pos = (self.x, self.y)
    
    def end_move(self):
        self.moving = False
        self.start_pos = None
    
    def update(self):
        if self.moving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.x = mouse_x - self.offset[0]
            self.y = mouse_y - self.offset[1]
    
    def click(self):
        pass
    