from parser.values.operator_expression import OperatorExpression


# TODO: position
class ObjectAccessExpression(OperatorExpression):
    def __init__(self, left_expression, right_expression, position=None):
        super().__init__(left_expression, right_expression, position)

    def __eq__(self, other):
        return (
            isinstance(other, ObjectAccessExpression)
            and self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def __repr__(self) -> str:
        return f"(Object_access: {self.left_expression}.{self.right_expression})"

    def accept(self, visitator):
        visitator.visit_access_expr(self)
