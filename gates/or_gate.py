from .node import Node


class Or(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = [[], []]
        self.name = "Or"

    @property
    def value(self):
        for inps in self.inputs:
            for inp in inps:
                if inp[0].value(r + 1):
                    return True
        return False
