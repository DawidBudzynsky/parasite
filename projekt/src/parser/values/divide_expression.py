from parser.values.operator_expression import OperatorExpression


# TODO: position
class DivideExpression(OperatorExpression):
    def __init__(self, left_expression, right_expression):
        super().__init__(left_expression, right_expression)

    def __repr__(self) -> str:
        return f"({self.left_expression} / {self.right_expression})"

    def accept(self, visitator):
        return visitator.visit_divide_expression(self)
