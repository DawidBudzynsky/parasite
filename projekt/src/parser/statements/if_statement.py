from projekt.src.parser.statement import Statement


class IfStatement(Statement):
    def __init__(self, conditions_instructions, else_instructions):
        self.conditions_instructions = conditions_instructions
        self.else_instructions = else_instructions

    def __eq__(self, other):
        if not isinstance(other, IfStatement):
            return False
        return (
            self.conditions_instructions == other.conditions_instructions
            and self.else_instructions == other.else_instructions
        )

    def __repr__(self) -> str:
        return f"(if_conditions: {self.conditions_instructions}, else:{self.else_instructions})"

    def accept(self, visitator):
        return visitator.visit_if_statement(self)
