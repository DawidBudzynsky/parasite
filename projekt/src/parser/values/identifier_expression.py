from projekt.src.parser.node import Node


class Identifier(Node):
    def __init__(self, name, position) -> None:
        super().__init__(position)
        self.name = name
        self.position = position

    def __eq__(self, other):
        return (
            isinstance(other, Identifier)
            and self.name == other.name
            and self.position == other.position
        )

    def accept(self, visitator):
        return visitator.visit_identifier(self)
