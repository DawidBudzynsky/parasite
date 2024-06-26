from parser.node import Node
from parser.values.operator_expression import OperatorExpression


class OrExpression(OperatorExpression, Node):
    def __init__(self, left_expression=None, right_expression=None, position=None):
        super().__init__(left_expression, right_expression, position)

    def __repr__(self) -> str:
        return f"({self.left_expression} or {self.right_expression})"

    def __eq__(self, other):
        return (
            isinstance(other, OrExpression)
            and self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def accept(self, visitator):
        visitator.visit_or_expression(self)
