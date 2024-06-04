from parser.values.operator_expression import OperatorExpression


# TODO: position
class NotEqualsExpression(OperatorExpression):
    def __init__(self, left_expression=None, right_expression=None, position=None):
        super().__init__(left_expression, right_expression, position)

    def __repr__(self):
        return f"({self.left_expression} != {self.right_expression})"

    def accept(self, visitator):
        return visitator.visit_not_equals_expr(self)
