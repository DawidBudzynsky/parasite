from parser.values.operator_expression import OperatorExpression


# TODO: position
class DivideExpression(OperatorExpression):
    def __init__(self, left_expression, right_expression, position=None):
        super().__init__(left_expression, right_expression, position)

    def __repr__(self) -> str:
        return f"({self.left_expression} / {self.right_expression})"

    def accept(self, visitator):
        visitator.visit_divide_expression(self)
