from projekt.src.parser.node import Node


# NOTE: for now variable takes type as value, not Type.Something
class Variable(Node):
    def __init__(self, identifier, type, value=None, position=None):
        super().__init__(position)
        self.identifier = identifier
        self.type = type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.identifier == other.identifier and self.type == other.type

    def accept(self, visitator):
        return visitator.visit_function(self)
