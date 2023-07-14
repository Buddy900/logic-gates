from consts import *
from scroll_list import ScrollList
from gates import NodeImage, Node

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class Sidebar:
    def __init__(self, width):
        self.width = width
        
        self.scroll_list = ScrollList(["and", "or", "not", "nand", "xor", "nor", "xnor", "switch", "bulb", "buffer", "4_bit_number", "full_adder", "clock",
                                       "_example", "_example", "_example"],
                                      (15, 15), (self.width - 30, HEIGHT - 30))
        
        self.chosen = None
        
        self.create_new_node = False
        self.new_node = None
    
    def draw(self, win: pygame.surface.Surface):
        pygame.draw.rect(win, COLOURS["snow2"], pygame.rect.Rect(0, 0, self.width, HEIGHT))
        self.scroll_list.draw(win)
        if self.chosen:
            self.chosen.draw(win)

    def update(self):
        if self.chosen:
            self.chosen.update()
    
    def handle_mouse_down(self, event):
        self.chosen = self.scroll_list.click(event, pygame.mouse.get_pos())
        if self.chosen:
            self.chosen.start_move()
    
    def handle_mouse_up(self, event):
        if event.button == 1 and self.chosen:
            self.create_new_node = True
            self.new_node = Node(self.chosen.name, self.chosen.x - self.width, self.chosen.y, 50, NODE_HEIGHT, 0)
            self.chosen.reset()
            self.chosen = None
    
    def get_new_node(self):
        self.create_new_node = False
        new_node, self.new_node = self.new_node, None
        self.create_new_node = False
        return new_node
        