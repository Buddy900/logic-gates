from consts import *
from .movable import Movable

import pygame
import json


class Node(Movable):
    def __init__(self, name, x, y, width, height):
        super().__init__(x, y, width, height)
        self.selected = None
        self.file_name = f"{name}.json"
        self.load_json()

    @property
    def value(self):
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
                pygame.draw.rect(win, COLOURS["green"], rect, border_bottom_right_radius=2, border_top_right_radius=2)
            elif self.value and not self.name in ["Bulb", "Switch"]:
                pygame.draw.rect(win, COLOURS["cyan"], rect, border_bottom_right_radius=2, border_top_right_radius=2)
            else:
                pygame.draw.rect(win, COLOURS["red"], rect, border_bottom_right_radius=2, border_top_right_radius=2)
        
        # draw lines from input rects to output rects
        for i, output in enumerate(self.outputs):
            for this_index, (other) in enumerate(output):
                if other is None:
                    continue
                other_node, other_index = other
                pygame.draw.line(win, COLOURS["black"], self.output_rects()[i].center, other_node.input_rects()[other_index].center)
    
    def draw_input_rects(self, win):
        for rect in self.input_rects():
            pygame.draw.rect(win, COLOURS["red"], rect, border_bottom_left_radius=2, border_top_left_radius=2)
    
    def draw(self, win):
        if self.value and self.name in ["bulb", "switch"]:
            colour = COLOURS["cyan"]
        else:
            colour = COLOURS["black"]
        pygame.draw.rect(win, colour, self.rect, border_radius=3)
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
    
    
    
    def load_json(self):
        with open(f"gates\\gate_json\\{self.file_name}", "r") as file:
            data = json.load(file)
            self.name = data["name"]
            self.num_inputs = data["num_inputs"]
            self.inputs = [[] for _ in range(self.num_inputs)]
            self.num_outputs = data["num_outputs"]
            self.outputs = [[] for _ in range(self.num_outputs)]
            self.structure = data["structure"]
            self.output_values = {i: False for i in range(self.num_outputs)}
            self.clickable == False

    def gate(self, name, *args):
        if name == "and":
            print(args)
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
    
    def get_input_value(self, input_index):
        if len(self.inputs[input_index]) == 0:
            return False
        return self.inputs[input_index][0][0].value

    def updated_value(self):
        gates = {str(i): self.get_input_value(i) for i in range(self.num_inputs)}
        for gate, data in self.structure["gates"].items():
            if data == "on_click":
                self.clickable = True
                gates[gate] = False
            if len(data) == 1:
                gates[gate] = self.gate(data[0])
            elif len(data) == 2:
                gates[gate] = self.gate(data[0], gates[data[1]])
            else:
                gates[gate] = self.gate(data[0], *[gates[data[i]] for i in range(1, len(data))])
        
        print(gates)
        
        for output, data in self.structure["outputs"].items():
            self.output_values[int(output)] = gates[data]
        
        print(self.output_values)
