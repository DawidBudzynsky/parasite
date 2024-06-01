from projekt.src.parser.values.operator_expression import OperatorExpression


# TODO: position
class SubtractExpression(OperatorExpression):
    def __init__(self, left_expression, right_expression):
        super().__init__(left_expression, right_expression)

    def __eq__(self, other):
        return (
            isinstance(other, SubtractExpression)
            and self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def __repr__(self) -> str:
        return f"({self.left_expression} - {self.right_expression})"

    def accept(self, visitator):
        return visitator.visit_sub_expr(self)
