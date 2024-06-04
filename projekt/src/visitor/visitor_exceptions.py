VARIABLE_NOT_DECLARED = "Error: Couldn't find [%s] in scope, declare it first; [%d:%d]"

VARIABLE_REDEFINITION = (
    "Error: Couldn't create, variable [%s] is already in scope; [%d:%d]"
)

EXPRESSION_WRONG_TYPE = (
    "Error: Couldn't create [%s] expression, expression should be of type [%s]; [%d:%d]"
)

WRONG_RETURN_TYPE = "Error: Wrong return type [%s] should be [%s]; [%d:%d]"
INVALID_PARAMETERES = (
    "Error: Invalid number of parameters, given: [%s], expected: [%s]; [%d:%d]"
)

FUNCTION_NOT_DECLARED = (
    "Error: Couldn't find function: [%s] declaration, declare it first; [%d:%d]"
)

OBJECT_ACCESS = "Error: [%s] is not an object, it doesnt have any attributes; [%d:%d]"
OBJECT_NO_ATTR = "Error: [%s] object doesnt have attribute [%s]; [%d:%d]"
ASPECT_BLOCK = (
    "Error: Only variable declarations are available in aspect block; [%d:%d]"
)


class NotDeclared(Exception):
    def __init__(self, message, position=(0, 0)):
        message = VARIABLE_NOT_DECLARED % (message, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class Redefinition(Exception):
    def __init__(self, message, position=(0, 0)):
        message = VARIABLE_REDEFINITION % (message, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class ExprWrongType(Exception):
    def __init__(self, expression, type, position=(0, 0)):
        message = EXPRESSION_WRONG_TYPE % (expression, type, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class WrongReturnType(Exception):
    def __init__(self, given_value, expected_value, position=(0, 0)):
        message = WRONG_RETURN_TYPE % (
            given_value,
            expected_value,
            position[0],
            position[1],
        )
        super().__init__(message)
        self.message = message
        self.position = position


class InvalidParameters(Exception):
    def __init__(self, message, message2, position=(0, 0)):
        message = INVALID_PARAMETERES % (message, message2, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class FunctionNotDeclared(Exception):
    def __init__(self, message, position=(0, 0)):
        message = VARIABLE_NOT_DECLARED % (message, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class ObjectAccessException(Exception):
    def __init__(self, message, position=(0, 0)):
        message = OBJECT_ACCESS % (message, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class NoAttributeException(Exception):
    def __init__(self, base_obj, attr, position=(0, 0)):
        message = OBJECT_NO_ATTR % (base_obj, attr, position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position


class AspectBlockException(Exception):
    def __init__(self, position=(0, 0)):
        message = ASPECT_BLOCK % (position[0], position[1])
        super().__init__(message)
        self.message = message
        self.position = position