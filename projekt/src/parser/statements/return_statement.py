from parser.statement import Statement


# TODO: position
class ReturnStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        if not isinstance(other, ReturnStatement):
            return False
        return self.expression == other.expression

    def __repr__(self) -> str:
        return f"(return: {self.expression})"

    def accept(self, visitator):
        return visitator.visit_return_statement(self)
