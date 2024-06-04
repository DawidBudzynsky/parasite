class EmbeddedFunction:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def accept(self, visitator):
        return visitator.visit_embedded_function(self)
