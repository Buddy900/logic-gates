from .node import Node


class Nand(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = [[], []]
        self.name = "Nand"
    
    def value(self, r):
        inp_1 = False
        inp_2 = False
        for inp in self.inputs[0]:
            inp_1 = inp_1 or inp[0].value(r + 1)
        
        for inp in self.inputs[1]:
            inp_2 = inp_2 or inp[0].value(r + 1)
        
        return not (inp_1 and inp_2)
