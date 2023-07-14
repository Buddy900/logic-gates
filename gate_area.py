from consts import *
from gates import Node

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class GateArea:
    def __init__(self, x):
        self.x = x
        self.nodes = []
        self.selected_node = None
    
    def draw(self, win: pygame.surface.Surface):
        for node in self.nodes:
            node.draw(win, x_offset=self.x)
            
    def update(self):
        for i in self.nodes:
            delete = i.update()
            if delete:
                i.remove()
                self.nodes.remove(i)
    
    def handle_key_down(self, event):
        pass
    
    def handle_mouse_down(self, event):
        if event.button == 1:
            for i in reversed(self.nodes):       # reversed so that highest layer is checked first
                if i.clicked():
                    i.start_move()
                    break
                if (selected := i.output_node_selected()) >= 0:
                    if self.selected_node == [i, selected]:
                        self.selected_node = None
                        i.select(None)
                        break
                    i.select(selected)
                    self.selected_node = [i, selected]
                    break
                if self.selected_node is not None and (selected := i.input_node_selected()) >= 0 and self.selected_node[0] != i:
                    if tuple(self.selected_node) in i.inputs[selected]:
                        self.selected_node[0].un_attach(i, self.selected_node[1], selected)
                        self.selected_node[0].select(None)
                        self.selected_node = None
                    else:
                        self.selected_node[0].attach(i, self.selected_node[1], selected)
                        self.selected_node[0].select(None)
                        i.select(None)
                        self.selected_node = None
                    break
        elif event.button == 3:
            for i in reversed(self.nodes):
                if i.clicked():
                    i.remove()
                    self.nodes.remove(i)
                    break
    
    def handle_mouse_up(self, event):
        if event.button == 1:
            for i in self.nodes:
                if (i.x, i.y) == i.start_pos:
                    i.click()
                i.end_move()
