from projekt.src.parser.values.operator_expression import OperatorExpression


class IsExpression(OperatorExpression):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def accept(self, visitator):
        return visitator.visit_is_expr(self)
