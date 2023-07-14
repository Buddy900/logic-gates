from consts import *
from gates import NodeImage

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class ScrollList:
    def __init__(self, things, pos, dimensions):
        self.things = []
        self.x, self.y = pos
        self.width, self.height = dimensions
        self.border = 3
        self.item_height = NODE_HEIGHT
        self.current_pos = 0
        self.max_on_screen = self.height // (self.item_height + self.border)
        for index, item in enumerate(things):
            x_1, y_1 = self.x + self.border * 5, self.y + index * (self.item_height + self.border) + self.border
            self.things.append(NodeImage(item, [x_1, y_1]))
    
    def click(self, event, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if not (self.x <= mouse_x < self.x + self.width and self.y <= mouse_y < self.y + self.height):
            return
        
        if event.button == 1:   # left click
            on_screen = self.things[self.current_pos: self.current_pos + self.max_on_screen]
            chosen = (mouse_y - self.y) // (self.item_height + self.border)
            if chosen >= min(len(self.things), self.max_on_screen):
                return
            return self.press(on_screen[chosen])
            
        elif event.button == 4: # scroll up
            old = self.current_pos
            self.current_pos = max(0, self.current_pos - 1)
            if old != self.current_pos:
                for node in self.things:
                    node.default_pos[1] += self.item_height + self.border
                    node.reset()
        elif event.button == 5: # scroll down
            old = self.current_pos
            self.current_pos = min(max(0, len(self.things) - self.max_on_screen), self.current_pos + 1)
            if old != self.current_pos:
                for node in self.things:
                    node.default_pos[1] -= self.item_height + self.border
                    node.reset()
        
    def release(self, event, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if not (self.x <= mouse_x < self.x + self.width and self.y <= mouse_y < self.y + self.height):
            return
        
        if event.button == 1:   # left click
            on_screen = self.things[self.current_pos : self.current_pos + self.max_on_screen]
            chosen = (mouse_y - self.y) // (self.item_height + self.border)
            if chosen >= min(len(self.things), self.max_on_screen):
                return
            return self.press(on_screen[chosen])
    
    def press(self, thing):
        return thing
    
    def add(self, item, index=None):
        if index is not None:
            self.things.insert(index, item)
        else:
            self.things.append(item)
    
    def remove(self, item):
        self.things.remove(item)
    
    def get_pos(self, item):
        return self.things.index(item)
    
    def update(self, mouse_pos):
        for item in self.things:
            item.hover = False
        mouse_x, mouse_y = mouse_pos
        if not (self.x <= mouse_x < self.x + self.width and self.y <= mouse_y < self.y + self.height):
            return
        on_screen = self.things[self.current_pos : self.current_pos + self.max_on_screen]
        chosen = (mouse_y - self.y) // self.item_height
        if chosen >= min(len(self.things), self.max_on_screen):
            return
        on_screen[chosen].hover = True
        
    
    def draw(self, win: pygame.surface.Surface):
        rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, COLOURS["snow3"], rect)
        
        draw_scroll_bar = False
        for index, item in enumerate(self.things[self.current_pos:]):
            if index >= self.max_on_screen:
                draw_scroll_bar = True
                break
            x_1, y_1 = self.x + self.border * 5, self.y + index * (self.item_height + self.border) + self.border
            rect = pygame.rect.Rect(x_1, y_1, self.width - self.border * 2, self.item_height)
            item.draw(win, x=x_1, y=y_1)
        
        if draw_scroll_bar or self.current_pos > 0:
            scroll_bar_height = (self.max_on_screen / len(self.things)) * (self.height - self.border * 2)
            start_y = self.y + self.border
            end_y = self.y + self.height - self.border - scroll_bar_height
            scroll_bar_y = start_y + (end_y - start_y) * (self.current_pos / (len(self.things) - self.max_on_screen))
            rect = pygame.rect.Rect(self.x + self.width - self.border * 3, scroll_bar_y, self.border * 2, scroll_bar_height)
            pygame.draw.rect(win, COLOURS["black"], rect)
