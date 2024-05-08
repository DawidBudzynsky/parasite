from projekt.src.parser.node import Node


class Integer(Node):
    def __init__(self, value, position):
        super().__init__(position=position)
        self.value = int(value)

    def __eq__(self, other):
        return isinstance(other, Integer) and self.value == other.value

    def __repr__(self):
        return f"(INTEGER: {self.value}, {self.position})"

    def accept(self, visitator):
        return visitator.visit_integer(self)
