from consts import *
from gates import Node
from sidebar import Sidebar
from gate_area import GateArea

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class Screen:
    def __init__(self, win):
        self.win = win
        
        self.sidebar_width = 250
        self.sidebar = Sidebar(self.sidebar_width)
        
        self.gate_area = GateArea(self.sidebar_width)
    
    def update(self):
        self.sidebar.update()
        self.gate_area.update()
        if self.sidebar.create_new_node:
            new_node = self.sidebar.get_new_node()
            self.gate_area.nodes.append(new_node)
            
    def draw(self):
        self.win.fill(COLOURS["white"])
        
        self.gate_area.draw(self.win)
        self.sidebar.draw(self.win)
        
        pygame.display.update()
    
    def handle_key_down(self, event):
        self.gate_area.handle_key_down(event)
    
    def handle_key_up(self, event):
        pass
    
    def handle_mouse_down(self, event):
        if pygame.mouse.get_pos()[0] >= self.sidebar_width:
            self.gate_area.handle_mouse_down(event)
        else:
            self.sidebar.handle_mouse_down(event)
    
    def handle_mouse_up(self, event):
        self.gate_area.handle_mouse_up(event)
        self.sidebar.handle_mouse_up(event)
