from parser.node import Node


class NegateExpression(Node):
    def __init__(self, casting, position=(0, 0)):
        super().__init__(position=position)
        self.casting = casting

    def __eq__(self, other):
        return isinstance(other, NegateExpression) and self.casting == other.casting

    def __repr__(self) -> str:
        return f"(Negate: !{self.casting})"

    def accept(self, visitator):
        visitator.visit_negate_expression(self)
