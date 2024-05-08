MISSING_EXPRESSION = "Error: Missing expresion after [%c] operator; [%d:%d]"


class AspectArgument(Exception):
    def __init__(
        self,
        position=(0, 0),
    ):
        message = (
            f"Warning: Aspect not attached to any function; [{position[0]}:{position[1]}]",
        )
        super().__init__(message)
        self.position = position


class AspectBodyError(Exception):
    def __init__(
        self,
        position=(0, 0),
    ):
        message = (
            f"Error: Aspect must have at least 'before' or 'after' declaration; [{position[0]}:{position[1]}]",
        )
        super().__init__(message)
        self.position = position


class InvalidSyntax(Exception):
    def __init__(
        self, position=(0, 0), expected_type=None, given_type=None, given_value=None
    ):
        message = f"Error: Invalid syntax, wanted: {expected_type}, got: {given_type}; [{position[0]}:{position[1]}]"
        super().__init__(message)
        self.position = position
        self.expected_type = expected_type
        self.given_type = given_type
        self.given_value = given_value


class MissingStatement(Exception):
    def __init__(self, missing_statement, position=(0, 0)):
        message = f"Error: Missing statement {missing_statement}; [{position[0]}:{position[1]}]"
        super().__init__(message)
        self.position = position
        self.missing_statement = missing_statement


class MissingExpression(Exception):
    def __init__(self, operator, position=(0, 0)):
        message = MISSING_EXPRESSION % (operator, position[0], position[1])
        super().__init__(message)
        self.position = position
        self.operator = operator
