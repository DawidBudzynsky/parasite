from parser.expression import Expression


# TODO: position
class CastingExpression(Expression):
    def __init__(self, term, type=None):
        self.term = term
        self.type = type

    def __eq__(self, other):
        return (
            isinstance(other, CastingExpression)
            and self.term == other.term
            and self.type == other.type
        )

    def __repr__(self) -> str:
        return f"({self.term} -> {self.type})"

    def accept(self, visitator):
        visitator.visit_cast_expr(self)
