from projekt.src.parser.statement import Statement


class IfStatement(Statement):
    def __init__(self, conditions, if_instructions, else_instructions):
        self.conditions = conditions
        self.if_instructions = if_instructions
        self.else_instructions = else_instructions

    def __eq__(self, other):
        if not isinstance(other, IfStatement):
            return False
        return (
            self.conditions == other.conditions
            and self.if_instructions == other.if_instructions
            and self.else_instructions == other.else_instructions
        )

    def __repr__(self) -> str:
        return (
            f"(if: {self.conditions}, {self.if_instructions}, {self.else_instructions})"
        )

    def accept(self, visitator):
        return visitator.visit_if_statement(self)
