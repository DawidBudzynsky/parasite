import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.bool import Bool
from projekt.src.parser.values.casting_expression import CastingExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.plus_expression import AddExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "a -> int",
            CastingExpression(Identifier("a", (1, 1)), "int"),
        ),
        (
            "a -> str",
            CastingExpression(Identifier("a", (1, 1)), "str"),
        ),
        (
            "(a+b) -> str",
            CastingExpression(
                AddExpresion(Identifier("a", (1, 2)), Identifier("b", (1, 4))), "str"
            ),
        ),
        (
            "true -> str",
            CastingExpression(Bool(True, (1, 1)), "str"),
        ),
        (
            "(2*3) -> str",
            CastingExpression(
                MultiplyExpression(Integer(2, (1, 2)), Integer(3, (1, 4))), "str"
            ),
        ),
    ],
)
def test_variable_declaration_multiply(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_casting()
    assert expression == expected
