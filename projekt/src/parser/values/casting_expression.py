from projekt.src.parser.expression import Expression


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

    def accept(self, visitator):
        return visitator.visit_cast_expr(self)
