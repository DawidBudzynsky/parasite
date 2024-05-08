from enum import Enum, auto


class Type(Enum):
    EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    AND = auto()
    OR = auto()
    NEGATE = auto()
    IS = auto()
    PAREN_OPEN = auto()
    PAREN_CLOSE = auto()
    BRACE_OPEN = auto()
    BRACE_CLOSE = auto()
    WHILE = auto()
    FOR_EACH = auto()
    IN = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    ASPECT = auto()
    BEFORE = auto()
    AFTER = auto()
    RETURN = auto()
    COMMENT = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    INTEGER_TYPE = auto()
    FLOAT = auto()
    FLOAT_TYPE = auto()
    STRING = auto()
    STRING_TYPE = auto()
    TRUE = auto()
    FALSE = auto()
    BOOL_TYPE = auto()
    TYPE = auto()
    COMMA = auto()
    COLON = auto()
    ASSIGNMENT = auto()
    CAST = auto()
    ETX = auto()
    EOL = auto()
    DOT = auto()
    NOT = auto()
    UNIDENTIFIED = auto()


class Symbol:
    key_words = {
        "int": Type.INTEGER_TYPE,
        "float": Type.FLOAT_TYPE,
        "str": Type.STRING_TYPE,
        "bool": Type.BOOL_TYPE,
        "true": Type.TRUE,
        "false": Type.FALSE,
        "while": Type.WHILE,
        "for": Type.FOR_EACH,
        "in": Type.IN,
        "if": Type.IF,
        "is": Type.IS,
        "elif": Type.ELIF,
        "else": Type.ELSE,
        "aspect": Type.ASPECT,
        "before": Type.BEFORE,
        "after": Type.AFTER,
        "return": Type.RETURN,
        "and": Type.AND,
        "or": Type.OR,
        "->": Type.CAST,
    }


class Token:
    def __init__(self, token_type=Type.IDENTIFIER, value=None, position=None):
        self.token_type = token_type
        self.value = value
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (
            self.token_type == other.token_type
            and self.value == other.value
            and self.position == other.position
        )

    def __repr__(self):
        return f"{str(self.position).ljust(9)} {str(self.token_type).ljust(25)} {self.value}"

    def get_column(self):
        return self.column

    def get_line(self):
        return self.line

    def get_type(self):
        return self.token_type

    def get_value(self):
        return self.value

    def get_position(self):
        return self.line, self.column

    def set_position(self, line, column):
        self.line = line
        self.column = column
