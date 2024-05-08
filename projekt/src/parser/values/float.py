from projekt.src.parser.node import Node


class Float(Node):
    def __init__(self, value, position):
        super().__init__(position=position)
        self.value = float(value)

    def __eq__(self, other):
        return isinstance(other, Float) and self.value == other.value

    def __repr__(self):
        return f"(FLOAT: {self.value}, {self.position})"

    def accept(self, visitator):
        return visitator.visit_float(self)
