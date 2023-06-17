from .node import Node


class LowConstant(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = []
        self.name = "False"

    @property
    def value(self):
        return False
