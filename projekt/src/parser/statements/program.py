from parser.statement import Statement


class Program(Statement):
    def __init__(self, functions, aspects):
        self.functions = functions
        self.aspects = aspects

    def __eq__(self, other):
        if not isinstance(other, Program):
            return False
        return self.functions == other.functions and self.aspects == other.aspects

    def __repr__(self) -> str:
        return f"(PROGRAM: functions: {self.functions}, aspects: {self.aspects})"

    def accept(self, visitator):
        visitator.visit_program(self)
