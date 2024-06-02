from parser.statement import Statement


# TODO: position
class AspectBlock(Statement):
    def __init__(self, variables, before_statement=None, after_statement=None):
        self.variables = variables
        self.before_statement = before_statement
        self.after_statement = after_statement

    def __eq__(self, other):
        if not isinstance(other, AspectBlock):
            return False
        return (
            self.variables == other.variables
            and self.before_statement == other.before_statement
            and self.after_statement == other.after_statement
        )

    def __repr__(self) -> str:
        return f"(aspect block: {self.variables}, {self.before_statement}, {self.after_statement})"

    def accept(self, visitator):
        return visitator.visit_aspect_block(self)
