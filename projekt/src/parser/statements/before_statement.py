from projekt.src.parser.statement import Statement


class BeforeStatement(Statement):
    def __init__(self, block):
        self.block = block

    def __eq__(self, other):
        if not isinstance(other, BeforeStatement):
            return False
        return self.block == other.block

    def __repr__(self) -> str:
        return f"(before: {self.block})"

    def accept(self, visitator):
        return visitator.visit_before_statement(self)
