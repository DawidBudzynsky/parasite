from projekt.src.parser.values.operator_expression import OperatorExpression


# TODO: position
class EqualsExpression(OperatorExpression):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __eq__(self, other):
        if not isinstance(other, EqualsExpression):
            return False
        return (
            self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def __repr__(self) -> str:
        return f"({self.left_expression} == {self.right_expression})"

    def accept(self, visitator):
        return visitator.visit_equals_expr(self)
