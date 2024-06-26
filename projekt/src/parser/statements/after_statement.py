from parser.statement import Statement


class AfterStatement(Statement):
    def __init__(self, block):
        self.block = block

    def __eq__(self, other):
        if not isinstance(other, AfterStatement):
            return False
        return self.block == other.block

    def __repr__(self) -> str:
        return f"(after: {self.block})"

    def accept(self, visitator):
        visitator.visit_after_statement(self)
