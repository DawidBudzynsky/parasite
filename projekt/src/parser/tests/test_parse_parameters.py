import pytest
from projekt.src.lexer.tokens import Type
from projekt.src.parser.exceptions import InvalidSyntax
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.variable import Variable


def test_parse_parameter_number():
    parser = create_parser("number: int")
    expected = Variable(Identifier("number", (1, 1)), "int", position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameter_string():
    parser = create_parser("name: str")
    expected = Variable(Identifier("name", (1, 1)), "str", position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameters_multiple():
    parser = create_parser("number: int, name: str, dec_num: float, is_ok: bool")
    expected = [
        Variable(Identifier("number", (1, 1)), "int", position=(1, 1)),
        Variable(Identifier("name", (1, 14)), "str", position=(1, 14)),
        Variable(Identifier("dec_num", (1, 25)), "float", position=(1, 25)),
        Variable(Identifier("is_ok", (1, 41)), "bool", position=(1, 41)),
    ]
    a = parser.parse_parameters()
    assert a == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "number: int, int",
            InvalidSyntax(
                position=(1, 14),
                expected_type=Type.IDENTIFIER,
                given_type=Type.INTEGER_TYPE,
            ),
        ),
    ],
)
def test_parse_parameters_fail(input_str, expected):
    with pytest.raises(Exception) as e_info:
        parser = create_parser(input_str)
        parser.parse_parameters()

    assert isinstance(e_info.value, type(expected))
    assert str(e_info.value) == str(expected)
