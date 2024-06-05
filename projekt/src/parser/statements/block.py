from parser.statement import Statement


# TODO: position
class Block(Statement):
    def __init__(self, statements=[]):
        self.statements = statements

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.statements == other.statements

    def __repr__(self) -> str:
        return f"(BLOCK:{self.statements})"

    def accept(self, visitator):
        visitator.visit_block(self)
