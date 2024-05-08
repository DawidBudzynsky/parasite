from projekt.src.parser.statement import Statement


class FunCallStatement(Statement):
    def __init__(self, identifier, arguments, position=(0, 0)):
        self.identifier = identifier
        self.arguments = arguments
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, FunCallStatement):
            return False
        return self.identifier == other.identifier and self.arguments == other.arguments

    def __repr__(self) -> str:
        return f"(funcall: {self.identifier}({self.arguments}))"

    def accept(self, visitator):
        return visitator.visit_fun_call_statement(self)