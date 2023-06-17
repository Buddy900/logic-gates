from .node import Node
from consts import MAX_RECURSION_DEPTH


class Buffer(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = [[]]
        self.name = "Buffer"

    @property
    def value(self):
        for inp in self.inputs[0]:
            if inp[0].value:
                return True
        return False
