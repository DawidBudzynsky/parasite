from parser.statement import Statement


class LoopStatement(Statement):
    def __init__(self, expression, block=[], position=(0, 0)):
        self.expression = expression
        self.block = block
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, LoopStatement):
            return False
        return self.expression == other.expression and self.block == other.block

    def __repr__(self) -> str:
        return f"(while: {self.expression}, {self.block})"

    def accept(self, visitator):
        return visitator.visit_loop_statement(self)
