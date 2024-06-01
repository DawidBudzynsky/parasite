from projekt.src.parser.node import Node


class FunctionDef(Node):
    def __init__(self, identifier, parameters, type, block, position):
        super().__init__(position)
        self.identifier = identifier
        self.parameters = parameters
        self.type = type
        self.block = block

    def accept(self, visitator):
        return visitator.visit_function_declaration(self)

    def __eq__(self, other):
        return (
            isinstance(other, FunctionDef)
            and self.identifier == other.identifier
            and self.parameters == other.parameters
            and self.type == other.type
            and self.block == other.block
        )

    def __repr__(self) -> str:
        return f"(funcDef: {self.identifier}, {self.parameters}, {self.type}, {self.block})"
