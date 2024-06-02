import pytest
from parser.tests.test_utils import create_parser
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.minus_negate_expression import MinusNegateExpression
from parser.values.negate_expression import NegateExpression


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "!var1",
            NegateExpression(Identifier("var1", (1, 2)), (1, 1)),
        ),
        (
            "-12",
            MinusNegateExpression(Integer(12, (1, 2))),
        ),
    ],
)
def test_parse_unary(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_unary()
    assert expression == expected
