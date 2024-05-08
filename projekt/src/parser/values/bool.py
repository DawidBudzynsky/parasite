from projekt.src.parser.node import Node


class Bool(Node):
    def __init__(self, value, position):
        super().__init__(position=position)
        self.value = bool(value)

    def __eq__(self, other):
        return isinstance(other, Bool) and self.value == other.value

    def __repr__(self):
        return f"(BOOL: {self.value}, {self.position})"

    def accept(self, visitator):
        return visitator.visit_bool(self)
