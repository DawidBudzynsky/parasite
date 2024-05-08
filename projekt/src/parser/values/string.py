from projekt.src.parser.node import Node


class String(Node):
    def __init__(self, value, position):
        super().__init__(position=position)
        self.value = str(value)

    def __eq__(self, other):
        return isinstance(other, String) and self.value == other.value

    def __repr__(self):
        return f"(STRING: {self.value}, {self.position})"

    def accept(self, visitator):
        return visitator.visit_string(self)
