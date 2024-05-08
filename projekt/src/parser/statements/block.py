from typing_extensions import List
from projekt.src.parser.statement import Statement


class Block(Statement):
    def __init__(self, statements: List = []):
        self.statements = statements

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return self.statements == other.statements

    def __repr__(self) -> str:
        return f"(BLOCK:{self.statements})"

    def accept(self, visitator):
        return visitator.visit_block(self)