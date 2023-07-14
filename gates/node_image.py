from consts import *
from gates import Node, Movable

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class NodeImage(Movable):
    def __init__(self, node_name, default_pos):
        self.default_pos = default_pos
        self.x, self.y = self.default_pos
        self.name = node_name
        self.node = Node(node_name, self.x, self.y, 50, NODE_HEIGHT)
        super().__init__(0, 0, 50, NODE_HEIGHT)
        self.reset()
    
    def draw(self, win, x=None, y=None):
        if x is None: x = self.x
        if y is None: y = self.y
        self.node.draw(win, x, y)
    
    def reset(self):
        self.end_move()
        self.x, self.y = self.default_pos
        self.node = Node(self.name, 0, 0, 50, NODE_HEIGHT)
        