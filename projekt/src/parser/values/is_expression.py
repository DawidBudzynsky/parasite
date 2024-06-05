from parser.values.operator_expression import OperatorExpression


# TODO: position
class IsExpression(OperatorExpression):
    def __init__(self, left_expression=None, right_expression=None, position=None):
        super().__init__(left_expression, right_expression, position)

    def __eq__(self, other):
        return (
            isinstance(other, IsExpression)
            and self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def __repr__(self) -> str:
        return f"({self.left_expression} is {self.right_expression})"

    def accept(self, visitator):
        visitator.visit_is_expr(self)
