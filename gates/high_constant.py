from .node import Node


class HighConstant(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = []
        self.name = "True"
    
    def value(self, r):
        return True