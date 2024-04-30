from io import StringIO
from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.reader import Source
from projekt.src.parser.parser import Parser
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.variable import Variable


def create_parser(string: str):
    source = Source(StringIO(string))
    lexer = Lexer(source)
    return Parser(lexer)


def test_parse_parameter_number():
    parser = create_parser("number: int")
    expected = Variable("number", "int", position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameter_string():
    parser = create_parser("name: str")
    expected = Variable("name", "str", position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameters():
    parser = create_parser("number: int, name: str, dec_num: float, is_ok: bool")
    expected = [
        Variable("number", "int", position=(1, 1)),
        Variable("name", "str", position=(1, 13)),
        Variable("dec_num", "float", position=(1, 24)),
        Variable("is_ok", "bool", position=(1, 40)),
    ]
    a = parser.parse_parameters()
    print(a)
    assert a == expected


def test_variable_declaration():
    parser = create_parser("int a = 1 + 3")
    expected = Variable("a", "int", value=AddExpresion(1, 3), position=(1, 1))
    statement = parser.parse_variable_declaration()
    assert statement == expected
