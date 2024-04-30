from projekt.src.parser.expression import Expression


class CastingExpression(Expression):
    def __init__(self, term, type=None):
        self.term = term
        self.type = type

    def accept(self, visitator):
        return visitator.visit_cast_expr(self)
