from parser.values.operator_expression import OperatorExpression


class GreaterEqualExpression(OperatorExpression):
    def __init__(self, left_expression=None, right_expression=None, position=None):
        super().__init__(left_expression, right_expression, position)

    def __eq__(self, other):
        if not isinstance(other, GreaterEqualExpression):
            return False
        return (
            self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def __repr__(self) -> str:
        return f"({self.left_expression} >= {self.right_expression})"

    def accept(self, visitator):
        visitator.visit_greater_equal_expr(self)
