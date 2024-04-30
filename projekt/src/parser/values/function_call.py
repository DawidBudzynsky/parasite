from projekt.src.parser.node import Node


class FunctionCall(Node):
    def __init__(self, identifier, arguments=[]) -> None:
        super().__init__(identifier.position)
        self.identifier = identifier
        self.arguments = arguments

    def __eq__(self, other):
        return (
            isinstance(other, FunctionCall)
            and self.identifier == other.identifier
            and self.arguments == other.arguments
        )

    def accept(self, visitator):
        return visitator.visit_funcall(self)
