from consts import *
from scroll_list import ScrollList

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class Sidebar:
    def __init__(self, width):
        self.width = width
        
        self.scroll_list = ScrollList([str(i) for i in range(60)], (15, 15), (self.width - 30, HEIGHT - 30))
    
    def draw(self, win: pygame.surface.Surface):
        pygame.draw.rect(win, COLOURS["snow2"], pygame.rect.Rect(0, 0, self.width, HEIGHT))
        self.scroll_list.draw(win)

    def update(self):
        # self.scroll_list.update(pygame.mouse.get_pos())
        ...
    
    def handle_mouse_down(self, event):
        self.scroll_list.click(event, pygame.mouse.get_pos())
    
    def handle_mouse_up(self, event):
        pass
    