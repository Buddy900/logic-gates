from .node import Node


class Switch(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = []
        self.name = "Switch"
        self.on = False
    
    def click(self):
        self.on = not self.on
    
    def value(self, r):
        return self.on
