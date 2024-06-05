from parser.statement import Statement


# TODO: position
class ForEachStatement(Statement):
    def __init__(self, identifier, expression, block=[], position=None):
        self.identifier = identifier
        self.expression = expression
        self.block = block
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, ForEachStatement):
            return False
        return (
            self.identifier == other.identifier
            and self.expression == other.expression
            and self.block == other.block
        )

    def __repr__(self) -> str:
        return f"(foreach: {self.identifier}, {self.expression}, {self.block})"

    def accept(self, visitator):
        visitator.visit_for_each_statement(self)
