from parser.statement import Statement


class Aspect(Statement):
    def __init__(self, identifier, aspect_args, aspect_block, position):
        self.identifier = identifier
        self.aspect_args = aspect_args
        self.aspect_block = aspect_block
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, Aspect):
            return False
        return (
            self.identifier == other.identifier
            and self.aspect_args == other.aspect_args
            and self.aspect_block == other.aspect_block
        )

    def __repr__(self) -> str:
        return f"(aspect: {self.identifier}, {self.aspect_args}, {self.aspect_block})"

    def accept(self, visitator):
        return visitator.visit_aspect_statement(self)
