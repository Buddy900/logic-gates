from .node import Node


class Bulb(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = []
        self.inputs = [[]]
        self.name = "Bulb"

    @property
    def value(self, r):
        for inp in self.inputs[0]:
            if inp[0].value:
                return True
