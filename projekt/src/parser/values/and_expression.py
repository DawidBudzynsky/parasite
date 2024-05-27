from projekt.src.parser.node import Node
from projekt.src.parser.values.operator_expression import OperatorExpression


# TODO: position
class AndExpression(OperatorExpression, Node):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __repr__(self) -> str:
        return f"({self.left_expression} and {self.right_expression})"

    def __eq__(self, other):
        return (
            isinstance(other, AndExpression)
            and self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def accept(self, visitator):
        return visitator.visit_and_expression(self)
