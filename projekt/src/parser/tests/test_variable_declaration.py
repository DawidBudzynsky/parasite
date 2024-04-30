import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "int a = 1 * 3",
            Variable("a", "int", value=MultiplyExpression(1, 3), position=(1, 1)),
        ),
        (
            "int a = 1 + 2",
            Variable("a", "int", value=AddExpresion(1, 2), position=(1, 1)),
        ),
        (
            "int a = 1 + 2",
            Variable("a", "int", value=AddExpresion(1, 2), position=(1, 1)),
        ),
        (
            "int a = 1 * 2 + 1",
            Variable(
                "a",
                "int",
                value=AddExpresion(MultiplyExpression(1, 2), 1),
                position=(1, 1),
            ),
        ),
        (
            "int a = 3 * (2 + 2)",
            Variable(
                "a",
                "int",
                value=MultiplyExpression(3, AddExpresion(2, 2)),
                position=(1, 1),
            ),
        ),
        (
            "bool a = some_bool",
            Variable(
                "a",
                "bool",
                value="some_bool",
                position=(1, 1),
            ),
        ),
    ],
)
def test_variable_declaration_multiply(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_variable_declaration()
    assert expression == expected
