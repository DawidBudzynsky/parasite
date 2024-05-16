import pytest
from projekt.src.lexer.tokens import Type
from projekt.src.parser.exceptions import (
    MISSING_IDENTIFIER_AFTER_COMMA,
    InvalidSyntaxVerbose,
)
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.variable import Variable


def test_parse_parameter_number():
    parser = create_parser("number: int")
    expected = Variable("number", TypeAnnotation.INT, position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameter_string():
    parser = create_parser("name: str")
    expected = Variable("name", TypeAnnotation.STR, position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameters_multiple():
    parser = create_parser("number: int, name: str, dec_num: float, is_ok: bool")
    expected = [
        Variable("number", TypeAnnotation.INT, position=(1, 1)),
        Variable("name", TypeAnnotation.STR, position=(1, 14)),
        Variable("dec_num", TypeAnnotation.FLOAT, position=(1, 25)),
        Variable("is_ok", TypeAnnotation.BOOL, position=(1, 41)),
    ]
    a = parser.parse_parameters()
    assert a == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "number: int, int",
            InvalidSyntaxVerbose(
                message=MISSING_IDENTIFIER_AFTER_COMMA,
                position=(1, 14),
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
