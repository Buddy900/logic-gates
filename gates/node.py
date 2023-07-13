from consts import *
from .movable import Movable

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import json


class Node(Movable):
    def __init__(self, name, x, y, width, height):
        self.file_name = f"{name}.json"
        self.load_json()
        self.name = self.data["name"]
        self.num_inputs = self.data["num_inputs"]
        self.inputs = [[] for _ in range(self.num_inputs)]
        self.num_outputs = self.data["num_outputs"]
        self.outputs = [[] for _ in range(self.num_outputs)]
        self.structure = self.data["structure"]
        self.output_values = {i: False for i in range(self.num_outputs)}
        self.light = False
        self.clickable = False
        self.on = False
        super().__init__(x, y, width, height)
        self.selected = None
        self.text = self.name
        
        self.draw_x, self.draw_y = self.x, self.y
    
    @property
    def rect(self):
        return pygame.Rect(self.draw_x, self.draw_y, self.width, self.height)
    
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
    
    def click(self):
        self.on = not self.on
        self.output_values[0] = self.on
    
    def output_rects(self):
        rects = []
        for i, other in enumerate(self.outputs):
            x = self.draw_x + self.width
            y = self.draw_y + self.height / len(self.outputs) * i + (self.height / len(self.outputs) - self.height / (len(self.outputs) + 1)) / 2
            width = 10
            height = self.height / (len(self.outputs) + 1)
            rects.append(pygame.Rect(x, y, width, height))
        return rects
    
    def input_rects(self):
        rects = []
        for i, other in enumerate(self.inputs):
            x = self.draw_x - 10
            y = self.draw_y + self.height / len(self.inputs) * i + (self.height / len(self.inputs) - self.height / (len(self.inputs) + 1)) / 2
            width = 10
            height = self.height / (len(self.inputs) + 1)
            rects.append(pygame.Rect(x, y, width, height))
        return rects
    
    def draw_output_rects(self, win):
        for i, output in enumerate(self.outputs):
            for this_index, (other) in enumerate(output):
                if other is None:
                    continue
                other_node, other_index = other
                if self.output_values[i]:
                    colour = COLOURS["orange"]
                else:
                    colour = COLOURS["black"]
                self.draw_wire(win, self.output_rects()[i].center, other_node.input_rects()[other_index].center, colour)
        
        for i, rect in enumerate(self.output_rects()):
            if i == self.selected:
                pygame.draw.rect(win, COLOURS["green"], rect, border_bottom_right_radius=2, border_top_right_radius=2)
            elif self.output_values[i] and not self.light:
                pygame.draw.rect(win, COLOURS["cyan"], rect, border_bottom_right_radius=2, border_top_right_radius=2)
            else:
                pygame.draw.rect(win, COLOURS["red"], rect, border_bottom_right_radius=2, border_top_right_radius=2)
    
    def draw_input_rects(self, win):
        for rect in self.input_rects():
            pygame.draw.rect(win, COLOURS["red"], rect, border_bottom_left_radius=2, border_top_left_radius=2)
    
    def draw(self, win, x_offset=0, y_offset=0):
        self.draw_x = self.x + x_offset
        self.draw_y = self.y + y_offset
        if self.light:
            colour = COLOURS["cyan"]
            text_colour = COLOURS["red"]
        else:
            colour = COLOURS["black"]
            text_colour = COLOURS["white"]
        
        pygame.draw.rect(win, colour, self.rect, border_radius=3)
        text = NODE_FONT.render(self.text, 1, text_colour)
        win.blit(text, (self.draw_x + self.width / 2 - text.get_width() / 2, self.draw_y + self.height / 2 - text.get_height() / 2))
        self.draw_input_rects(win)
        self.draw_output_rects(win)
    
    def draw_wire(self, win, point_1, point_2, colour):
        start_x, start_y  = point_1[0] + 20, point_1[1]
        end_x, end_y = point_2[0] - 20, point_2[1]
        diff_x = end_x - start_x
        diff_y = end_y - start_y
        mid_1 = (start_x, start_y + diff_y / 2)
        mid_2 = (end_x, start_y + diff_y / 2)
        pygame.draw.lines(win, colour, False, [point_1, (start_x, start_y), mid_1, mid_2, (end_x, end_y), point_2])
    
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
    
    def load_json(self):
        with open(os.path.join("gates", "gate_json", self.file_name)) as file:
            self.data = json.load(file)

    def gate(self, name, *args):
        if name == "and":
            return all(args)
        elif name == "or":
            return any(args)
        elif name == "not":
            return not args[0]
        elif name == "xor":
            return args[0] != args[1]
        elif name == "nand":
            return not all(args)
        elif name == "nor":
            return not any(args)
        elif name == "xnor":
            return args[0] == args[1]
        elif name == "false":
            return False
        elif name == "true":
            return True
        elif name == "hexadecimal":
            return str(hex(int("".join([str(int(i)) for i in args]), 2)))[2:]
    
    def get_input_value(self, input_index):
        for node, index in self.inputs[input_index]:
            if node.output_values[index]:
                return True
        return False

    def update_value(self):
        gates = {str(i): self.get_input_value(i) for i in range(self.num_inputs)}
        for gate, data in self.structure["gates"].items():
            if data == "on_click":
                self.clickable = True
                gates[gate] = self.on
            elif len(data) == 1:
                gates[gate] = self.gate(data[0])
            else:
                args = [gates.get(data[i], False) if data[i][0] != "o" else self.output_values[int(data[i][1:])] for i in range(1, len(data))]
                gates[gate] = self.gate(data[0], *args)
        
        for output, data in self.structure["outputs"].items():
            if output == "text":
                self.text = str(gates[data])
            elif output == "light":
                self.light = gates[data]
            else:
                self.output_values[int(output)] = gates[data]
    
    def update(self):
        super().update()
        self.update_value()
