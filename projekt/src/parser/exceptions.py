MISSING_EXPRESSION = "Error: Missing expresion after [%c] operator; [%d:%d]"
MISSING_STATEMENT = "Error: Missing statement [%s]; [%d:%d]"
INVALID_SYNTAX = "Error: Invalid syntax, wanted: [%s], got: [%s]; [%d:%d]"
TYPE_ANNOTATION = "Error: Missing type annotation; [%d:%d]"
FUNC_REDEFINITION = "Error: Function redefinition, function name: [%s]; [%d:%d]"
ASPECT_REDEFINITION = "Error: Aspect redefinition, aspect name: [%s]; [%d:%d]"


class FunctionRedefinition(Exception):
    def __init__(self, function_name, position=(0, 0)):
        message = FUNC_REDEFINITION % (function_name, position[0], position[1])
        super().__init__(message)
        self.function_name = function_name
        self.position = position


class AspectRedefinition(Exception):
    def __init__(self, aspect_name, position=(0, 0)):
        message = ASPECT_REDEFINITION % (aspect_name, position[0], position[1])
        super().__init__(message)
        self.aspect_name = aspect_name
        self.position = position


class AspectArgument(Exception):
    def __init__(self, position=(0, 0)):
        message = (
            f"Warning: Aspect not attached to any function; [{position[0]}:{position[1]}]",
        )
        super().__init__(message)
        self.position = position


class AspectBodyError(Exception):
    def __init__(self, position=(0, 0)):
        message = (
            f"Error: Aspect must have at least 'before' or 'after' declaration; [{position[0]}:{position[1]}]",
        )
        super().__init__(message)
        self.position = position


class InvalidSyntax(Exception):
    def __init__(
        self, position=(0, 0), expected_type=None, given_type=None, given_value=None
    ):
        message = INVALID_SYNTAX % (expected_type, given_type, position[0], position[1])
        super().__init__(message)
        self.position = position
        self.expected_type = expected_type
        self.given_type = given_type
        self.given_value = given_value


class MissingTypeAnnotation(Exception):
    def __init__(self, position=(0, 0)):
        message = TYPE_ANNOTATION % (position[0], position[1])
        super().__init__(message)
        self.position = position


class MissingStatement(Exception):
    def __init__(self, missing_statement, position=(0, 0)):
        message = MISSING_STATEMENT % (missing_statement, position[0], position[1])
        super().__init__(message)
        self.position = position
        self.missing_statement = missing_statement


class MissingExpression(Exception):
    def __init__(self, operator, position=(0, 0)):
        message = MISSING_EXPRESSION % (operator, position[0], position[1])
        super().__init__(message)
        self.position = position
        self.operator = operator
