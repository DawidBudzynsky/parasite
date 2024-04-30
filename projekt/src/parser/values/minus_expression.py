from projekt.src.parser.values.operator_expression import OperatorExpression


class SubtractExpression(OperatorExpression):
    def __init__(self, left_expression, right_expression):
        super().__init__(left_expression, right_expression)

    def accept(self, visitator):
        return visitator.visit_minus_expr(self)
