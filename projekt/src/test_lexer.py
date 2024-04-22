from io import StringIO
import pytest
from errors import LexerError
from reader import Source
from lexer import Lexer
from tokens import Type, Token


@pytest.fixture
def lexer():
    source = Source(StringIO("fjdkasl"))
    return Lexer(source)


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("{", Token(Type.BRACE_OPEN, None, (1, 1))),
        ("}", Token(Type.BRACE_CLOSE, None, (1, 1))),
        ("(", Token(Type.PAREN_OPEN, None, (1, 1))),
        (")", Token(Type.PAREN_CLOSE, None, (1, 1))),
        ("*", Token(Type.MULTIPLY, None, (1, 1))),
        ("/", Token(Type.DIVIDE, None, (1, 1))),
        ("+", Token(Type.PLUS, None, (1, 1))),
        ("-", Token(Type.MINUS, None, (1, 1))),
        ("<", Token(Type.LESS, None, (1, 1))),
        (">", Token(Type.GREATER, None, (1, 1))),
        ("=", Token(Type.ASSIGNMENT, None, (1, 1))),
        (",", Token(Type.COMMA, None, (1, 1))),
        (":", Token(Type.COLON, None, (1, 1))),
        (".", Token(Type.DOT, None, (1, 1))),
        ("!", Token(Type.NOT, None, (1, 1))),
        ("<=", Token(Type.LESS_EQUAL, None, (1, 1))),
        (">=", Token(Type.GREATER_EQUAL, None, (1, 1))),
        ("==", Token(Type.EQUALS, None, (1, 1))),
        ("!=", Token(Type.NOT_EQUALS, None, (1, 1))),
        ("->", Token(Type.CAST, None, (1, 1))),
        ("int", Token(Type.INTEGER_TYPE, "int", (1, 1))),
        ("float", Token(Type.FLOAT_TYPE, "float", (1, 1))),
        ("str", Token(Type.STRING_TYPE, "str", (1, 1))),
        ("bool", Token(Type.BOOL_TYPE, "bool", (1, 1))),
        ("true", Token(Type.BOOL, "true", (1, 1))),
        ("false", Token(Type.BOOL, "false", (1, 1))),
        ("while", Token(Type.WHILE, "while", (1, 1))),
        ("for", Token(Type.FOR_EACH, "for", (1, 1))),
        ("in", Token(Type.IN, "in", (1, 1))),
        ("if", Token(Type.IF, "if", (1, 1))),
        ("is", Token(Type.IS, "is", (1, 1))),
        ("elif", Token(Type.ELIF, "elif", (1, 1))),
        ("else", Token(Type.ELSE, "else", (1, 1))),
        ("aspect", Token(Type.ASPECT, "aspect", (1, 1))),
        ("before", Token(Type.BEFORE, "before", (1, 1))),
        ("after", Token(Type.AFTER, "after", (1, 1))),
        ("return", Token(Type.RETURN, "return", (1, 1))),
        ("print", Token(Type.PRINT, "print", (1, 1))),
        ("and", Token(Type.AND, "and", (1, 1))),
        ("or", Token(Type.OR, "or", (1, 1))),
        ("->", Token(Type.CAST, None, (1, 1))),
        # values
        ("15", Token(Type.INTEGER, 15, (1, 1))),
        ("0.314", Token(Type.FLOAT, 0.314, (1, 1))),
        ('"test_string\ntesting"', Token(Type.STRING, "test_string\ntesting", (1, 1))),
        ("identifier_test", Token(Type.IDENTIFIER, "identifier_test", (1, 1))),
        ("//comment", Token(Type.COMMENT, "comment", (1, 1))),
    ],
)
def test_tokens(lexer, input_str, expected):
    lexer.source = Source(StringIO(input_str))
    token = lexer.build_next_token()
    assert token == expected


def test_unclosed_string_error():
    lexer = Lexer(Source(StringIO('"something')))
    with pytest.raises(LexerError):
        lexer.build_next_token()


def test_code_example():
    input = 'int a = 3\nint b = 4\nif a != b{ print("hello") }'
    expected_tokens = [
        Token(Type.INTEGER_TYPE, "int", (1, 1)),
        Token(Type.IDENTIFIER, "a", (1, 5)),
        Token(Type.ASSIGNMENT, None, (1, 7)),
        Token(Type.INTEGER, 3, (1, 9)),
        Token(Type.INTEGER_TYPE, "int", (2, 1)),
        Token(Type.IDENTIFIER, "b", (2, 5)),
        Token(Type.ASSIGNMENT, None, (2, 7)),
        Token(Type.INTEGER, 4, (2, 9)),
        Token(Type.IF, "if", (3, 1)),
        Token(Type.IDENTIFIER, "a", (3, 4)),
        Token(Type.NOT_EQUALS, None, (3, 6)),
        Token(Type.IDENTIFIER, "b", (3, 9)),
        Token(Type.BRACE_OPEN, None, (3, 10)),
        Token(Type.PRINT, "print", (3, 12)),
        Token(Type.PAREN_OPEN, None, (3, 17)),
        Token(Type.STRING, "hello", (3, 18)),
        Token(Type.PAREN_CLOSE, None, (3, 25)),
        Token(Type.BRACE_CLOSE, None, (3, 27)),
        Token(Type.ETX, None, (3, 28)),
    ]
    source = Source(StringIO(input))
    lexer = Lexer(source)
    tokens = []

    token = Token()
    while token.token_type != Type.ETX:
        token = lexer.build_next_token()
        tokens.append(token)
    assert tokens == expected_tokens
