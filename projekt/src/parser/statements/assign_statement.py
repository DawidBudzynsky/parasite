from parser.statement import Statement


class AssignStatement(Statement):
    def __init__(self, identifier, expression, position):
        self.identifier = identifier
        self.expression = expression
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, AssignStatement):
            return False
        return (
            self.expression == other.expression and self.identifier == other.identifier
        )

    def __repr__(self) -> str:
        return f"(assign: {self.identifier} = {self.expression})"

    def accept(self, visitator):
        return visitator.visit_assign_statement(self)
