import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.casting_expression import CastingExpression
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.plus_expression import AddExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "a -> int",
            CastingExpression("a", "int"),
        ),
        (
            "a -> str",
            CastingExpression("a", "str"),
        ),
        (
            "(a+b) -> str",
            CastingExpression(AddExpresion("a", "b"), "str"),
        ),
        (
            "true -> str",
            CastingExpression("true", "str"),
        ),
        (
            "(2*3) -> str",
            CastingExpression(MultiplyExpression(2, 3), "str"),
        ),
    ],
)
def test_variable_declaration_multiply(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_casting()
    assert expression == expected
