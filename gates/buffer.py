from .node import Node
from consts import MAX_RECURSION_DEPTH


class Buffer(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = [[]]
        self.name = "Buffer"
    
    def value(self, r):
        if r >= MAX_RECURSION_DEPTH:
            return False
        for inp in self.inputs[0]:
            if inp[0].value(r + 1):
                return True
        return False
