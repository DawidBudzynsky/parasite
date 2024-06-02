import pytest
from parser.exceptions import MissingExpression
from parser.tests.test_utils import create_parser
from parser.values.greater_equal_expression import GreaterEqualExpression
from parser.values.greater_expression import GreaterExpression
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.less_equal_expression import LessEqualExpresion
from parser.values.less_expression import LessExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("i<5", LessExpresion(Identifier("i", (1, 1)), Integer(5, (1, 3)))),
        ("i<=5", LessEqualExpresion(Identifier("i", (1, 1)), Integer(5, (1, 4)))),
        ("i>5", GreaterExpression(Identifier("i", (1, 1)), Integer(5, (1, 3)))),
        ("i>=5", GreaterEqualExpression(Identifier("i", (1, 1)), Integer(5, (1, 4)))),
    ],
)
def test_relation(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_relation()
    assert expression == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "i<",
            MissingExpression(operator="<", position=(1, 3)),
        ),
    ],
)
def test_relation_fails(input_str, expected):
    with pytest.raises(Exception) as e_info:
        parser = create_parser(input_str)
        parser.parse_relation()

    assert isinstance(e_info.value, type(expected))
    assert str(e_info.value) == str(expected)
