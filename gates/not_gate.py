from .node import Node


class Not(Node):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.outputs = [[]]
        self.inputs = [[]]
        self.name = "Not"

    @property
    def value(self):
        for inp in self.inputs[0]:
            if inp[0].value:
                return False
        return True
