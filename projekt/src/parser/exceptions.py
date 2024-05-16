MISSING_EXPRESSION = "Error: Missing expresion after [%c] operator; [%d:%d]"
MISSING_STATEMENT = "Error: Missing statement [%s]; [%d:%d]"
INVALID_SYNTAX = "Error: Invalid syntax, wanted: [%s] %s; [%d:%d]"
TYPE_ANNOTATION = "Error: Missing type annotation; [%d:%d]"
FUNC_REDEFINITION = "Error: Function redefinition, function name: [%s]; [%d:%d]"
ASPECT_REDEFINITION = "Error: Aspect redefinition, aspect name: [%s]; [%d:%d]"
VERBOSE = "Error: %s; [%d:%d]"

MISSING_IDENTIFIER_AFTER_COMMA = "Missing identifier after [,]"
ASSIGN_OR_CALL_MISSING = "Missing [%s] or [%s] after identifier"
FUN_DEF_PAREN_OPEN_MISSING = (
    "You should use [(] after identifier when defining a function"
)

FUN_DEF_PAREN_CLOSE_MISSING = (
    "Function definition not closed, you should use [)] after parameters"
)

ASPECT_DEF_PAREN_OPEN_MISSING = "Use [(] after identifier when defining an aspect"
ASPECT_MISSING_NAME = "Missing aspect name"
ASPECT_DEF_NOT_CLOSED = "Aspect definition not closed"
ASPECT_BLOCK_MISSING = "No block defined for aspect"
ASPECT_BLOCK_NOT_CLOSED = "Aspect block not closed"
FUN_CALL_NOT_CLOSED = "Function call not closed"
ETX_MISSING = "No End of Text symbol were found"
PARAMETER_IDENTIFIER = "Parameter must be an identifier"
PARAMETER_COLON_MISSING = "Use [:] after identifier when defining a parameter"
BLOCK_NOT_CLOSED = "Block is not closed"
VAR_DECLARATION_IDENTIFIER = (
    "You should name your variable, use identifier after [type]"
)
VAR_DECLARATION_COLON = "Use [=] to assign value to variable"
EXPREESION_NOT_CLOSED = "Expression not closed"
FOR_EACH_IDENTIFIER = "Define what identifier to iterate over"
FOR_EACH_IN_MISSING = "Use [in] after identifier in for loop"


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
