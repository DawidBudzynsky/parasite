from projekt.src.parser.node import Node


class MinusNegateExpression(Node):
    def __init__(self, casting, position=(0, 0)):
        super().__init__(position=position)
        self.casting = casting

    def __eq__(self, other):
        return (
            isinstance(other, MinusNegateExpression) and self.casting == other.casting
        )

    def __repr__(self) -> str:
        return f"(MinusNegate: -{self.casting})"

    def accept(self, visitator):
        return visitator.visit_minus_negate(self)
