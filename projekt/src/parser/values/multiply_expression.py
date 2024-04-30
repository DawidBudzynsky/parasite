from projekt.src.parser.values.operator_expression import OperatorExpression


class MultiplyExpression(OperatorExpression):
    def __init__(self, left_expression, right_expression):
        super().__init__(left_expression, right_expression)
