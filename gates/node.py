from consts import *
from .movable import Movable

import pygame


class Node(Movable):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[], []]
        self.inputs = [[], []]
        self.selected = None
        self.name = "#"
    
    def value(self, r):
        return False
    
    def attach(self, other_node, output_index, input_index):
        other_node.inputs[input_index].append((self, output_index))
        self.outputs[output_index].append((other_node, input_index))
    
    def un_attach(self, other_node, output_index, input_index):
        other_node.inputs[input_index].remove((self, output_index))
        self.outputs[output_index].remove((other_node, input_index))
    
    def remove(self):
        for i, other in enumerate(self.outputs):
            for node, index in reversed(other):         # reversed to prevent errors where it stops iterating through the list
                self.un_attach(node, i, index)
        
        for i, other in enumerate(self.inputs):
            for node, index in reversed(other):
                node.un_attach(self, index, i)
    
    def select(self, index):
        self.selected = index
    
    def output_rects(self):
        rects = []
        for i, other in enumerate(self.outputs):
            x = self.x + self.width
            y = self.y + self.height / len(self.outputs) * i + (self.height / len(self.outputs) - self.height / (len(self.outputs) + 1)) / 2
            width = 10
            height = self.height / (len(self.outputs) + 1)
            rects.append(pygame.Rect(x, y, width, height))
        return rects
    
    def input_rects(self):
        rects = []
        for i, other in enumerate(self.inputs):
            x = self.x - 10
            y = self.y + self.height / len(self.inputs) * i + (self.height / len(self.inputs) - self.height / (len(self.inputs) + 1)) / 2
            width = 10
            height = self.height / (len(self.inputs) + 1)
            rects.append(pygame.Rect(x, y, width, height))
        return rects
    
    def draw_output_rects(self, win):
        for i, rect in enumerate(self.output_rects()):
            if i == self.selected:
                pygame.draw.rect(win, COLOURS["green"], rect)
            else:
                pygame.draw.rect(win, COLOURS["red"], rect)
        
        # draw lines from input rects to output rects
        for i, output in enumerate(self.outputs):
            for this_index, (other) in enumerate(output):
                if other is None:
                    continue
                other_node, other_index = other
                pygame.draw.line(win, COLOURS["black"], self.output_rects()[i].center, other_node.input_rects()[other_index].center)
    
    def draw_input_rects(self, win):
        for rect in self.input_rects():
            pygame.draw.rect(win, COLOURS["red"], rect)
    
    def draw(self, win):
        if self.value(0):
            colour = COLOURS["cyan"]
        else:
            colour = COLOURS["black"]
        pygame.draw.rect(win, colour, self.rect)
        text = NODE_FONT.render(self.name, 1, COLOURS["white"])
        win.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))
        self.draw_output_rects(win)
        self.draw_input_rects(win)
    
    def output_node_selected(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, rect in enumerate(self.output_rects()):
            if rect.collidepoint(mouse_x, mouse_y):
                return i
        return -1
    
    def input_node_selected(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, rect in enumerate(self.input_rects()):
            if rect.collidepoint(mouse_x, mouse_y):
                return i
        return -1
            