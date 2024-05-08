from projekt.src.parser.node import Node
from projekt.src.parser.statement import Statement


class Variable(Node, Statement):
    def __init__(self, identifier, type, value=None, position=None):
        super().__init__(position)
        self.identifier = identifier
        self.type = type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return (
            self.identifier == other.identifier
            and self.type == other.type
            and self.value == other.value
            and self.position == other.position
        )

    def __repr__(self) -> str:
        return f"(variable: {self.identifier, self.type, self.value, self.position})"

    def accept(self, visitator):
        return visitator.visit_function(self)
