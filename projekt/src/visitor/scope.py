class ScopeVariable:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __eq__(self, other):
        return (
            isinstance(other, ScopeVariable)
            and self.value == other.value
            and self.type == other.type
        )

    def __repr__(self):
        return f"(ScopeVariable {self.value}, {self.type})"


class ScopeObject:
    def __init__(self, value, type, name=None, args=None):
        self.name = name
        self.value = value
        self.type = type
        self.args = args

    def __eq__(self, other):
        return (
            isinstance(other, ScopeObject)
            and self.value == other.value
            and self.type == other.type
            and self.name == other.name
            and self.args == other.args
        )

    def __repr__(self):
        return f"(ScopeObject {self.name}, {self.value}, {self.type}, {self.args})"


class Scope:
    def __init__(self, parent=None, variables={}):
        self.parent = parent
        self.variables = variables

    def __eq__(self, other):
        return isinstance(other, Scope) and self.variables == other.variables

    def __repr__(self):
        return f"Scope:{self.parent}, {self.variables}"

    def in_scope(self, name):
        if name not in self.variables:
            if self.parent is not None:
                return self.parent.in_scope(name)
            else:
                return None
        return self.variables.get(name)

    def in_current_scope(self, name):
        if name not in self.variables:
            return None
        return self.variables.get(name)
