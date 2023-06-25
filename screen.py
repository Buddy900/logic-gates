from consts import *
from gates import Node

import pygame


class Screen:
    def __init__(self, win):
        self.win = win
        self.nodes = []
        
        self.selected_node = None
    
    def update(self):
        for i in self.nodes:
            i.update()
    
    def draw(self):
        self.win.fill(COLOURS["white"])
        
        for node in self.nodes:
            node.draw(self.win)
        
        pygame.display.update()
    
    def handle_key_down(self, event):
        match event.key:
            case pygame.K_n:
                self.nodes.append(Node("not", 50, 50, 50, 50))
            case pygame.K_a:
                self.nodes.append(Node("and", 50, 50, 50, 50))
            case pygame.K_o:
                self.nodes.append(Node("or", 50, 50, 50, 50))
            case pygame.K_r:
                self.nodes.append(Node("nor", 50, 50, 50, 50))
            case pygame.K_z:
                self.nodes.append(Node("xnor", 50, 50, 50, 50))
            case pygame.K_t:
                self.nodes.append(Node("high_constant", 50, 50, 50, 50))
            case pygame.K_f:
                self.nodes.append(Node("low_constant", 50, 50, 50, 50))
            case pygame.K_b:
                self.nodes.append(Node("bulb", 50, 50, 50, 50))
            case pygame.K_d:
                self.nodes.append(Node("nand", 50, 50, 50, 50))
            case pygame.K_u:
                self.nodes.append(Node("buffer", 50, 50, 50, 50))
            case pygame.K_x:
                self.nodes.append(Node("xor", 50, 50, 50, 50))
            case pygame.K_s:
                self.nodes.append(Node("switch", 50, 50, 50, 50))
            case pygame.K_RSHIFT:
                self.nodes.append(Node("node", 50, 50, 50, 50))
            case pygame.K_1:
                self.nodes.append(Node("half_adder", 50, 50, 50, 50))
            case pygame.K_2:
                self.nodes.append(Node("full_adder", 50, 50, 50, 50))
            case pygame.K_c:
                self.nodes.append(Node("clock", 50, 50, 50, 50))
            case pygame.K_h:
                self.nodes.append(Node("4_bit_number", 50, 50, 50, 50))
            case pygame.K_RCTRL:
                self.nodes.append(Node("_example", 50, 50, 50, 50))
    
    def handle_key_up(self, event):
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
