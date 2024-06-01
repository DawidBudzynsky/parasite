from typing import TypeAlias
from projekt.src.parser.exceptions import InvalidSyntaxVerbose
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.variable import Variable


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
    def __init__(self, value, type, child):
        self.value = value
        self.type = type
        self.child = child

    def __eq__(self, other):
        return (
            isinstance(other, ScopeObject)
            and self.value == other.value
            and self.type == other.type
            and self.child == other.child
        )

    def __repr__(self):
        return f"(ScopeObject {self.value}, {self.type}, {self.child})"


class Scope:
    def __init__(self, parent=None, return_type=None, variables={}):
        self.parent = parent
        self.return_type = return_type
        self.variables = variables

    def __eq__(self, other):
        return isinstance(other, Scope) and self.variables == other.variables

    def __repr__(self):
        return f"{self.variables}"

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

    def put_variable(self, v_name, scope_variable):
        if self.in_current_scope(v_name):
            raise ValueError("variable redefinition")
        self.variables[f"{v_name}"] = scope_variable

    def set_value(self, v_name, value):
        if (variable := self.in_scope(v_name)) is None:
            raise ValueError("Variable not declared")
        new_value = self.check_value_type(variable.type, value)
        variable.value = new_value

    def check_value_type(self, type, value):
        match type:
            case TypeAnnotation.INT:
                if not isinstance(value, int):
                    raise ValueError("cannot assign to variable of type integer")
                return value
            case TypeAnnotation.FLOAT:
                if not isinstance(value, float):
                    raise ValueError("cannot assign to variable of type float")
                return value
            case TypeAnnotation.BOOL:
                if not isinstance(value, bool):
                    raise ValueError("cannot assign to variable of type bool")
                return value
            case TypeAnnotation.STR:
                if not isinstance(value, str):
                    raise ValueError("cannot assign to variable of type string")
                return value
            case _:
                return None  # NOTE: should be some kind of error

    def check_return_type(self, value):
        scope_pointer = self
        while scope_pointer.return_type is None:
            scope_pointer = scope_pointer.parent
        return_type = scope_pointer.return_type
        match return_type:
            case TypeAnnotation.INT:
                if not isinstance(value, int):
                    raise ValueError("Wrong return value, should be int")
                return
            case TypeAnnotation.FLOAT:
                if not isinstance(value, float):
                    raise ValueError("Wrong return value, should be float")
                return
            case TypeAnnotation.STR:
                if not isinstance(value, str):
                    raise ValueError("Wrong return value, should be string")
                return
            case TypeAnnotation.BOOL:
                if not isinstance(value, bool):
                    raise ValueError("Wrong return value, should be boolean")
                return
