import pytest
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.bool import Bool
from parser.values.casting_expression import CastingExpression
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.multiply_expression import MultiplyExpression
from parser.values.plus_expression import AddExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "a -> int",
            CastingExpression(Identifier("a", (1, 1)), TypeAnnotation.INT),
        ),
        (
            "a -> str",
            CastingExpression(Identifier("a", (1, 1)), TypeAnnotation.STR),
        ),
        (
            "(a+b) -> str",
            CastingExpression(
                AddExpresion(
                    Identifier("a", (1, 2)), Identifier("b", (1, 4)), position=(1, 7)
                ),
                TypeAnnotation.STR,
            ),
        ),
        (
            "true -> str",
            CastingExpression(Bool(True, (1, 1)), TypeAnnotation.STR),
        ),
        (
            "(2*3) -> str",
            CastingExpression(
                MultiplyExpression(
                    Integer(2, (1, 2)), Integer(3, (1, 4)), position=(1, 3)
                ),
                TypeAnnotation.STR,
            ),
        ),
    ],
)
def test_variable_declaration_multiply(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_casting()
    assert expression == expected
