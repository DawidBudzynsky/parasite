import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.bool import Bool
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "int a = 1 * 3",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=MultiplyExpression(Integer(1, (1, 9)), Integer(3, (1, 13))),
                position=(1, 1),
            ),
        ),
        (
            "int a = 1 + 2",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=AddExpresion(Integer(1, (1, 9)), Integer(2, (1, 13))),
                position=(1, 1),
            ),
        ),
        (
            "int a = 1 * 2 + 1",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=AddExpresion(
                    MultiplyExpression(Integer(1, (1, 9)), Integer(2, (1, 13))),
                    Integer(1, (1, 17)),
                ),
                position=(1, 1),
            ),
        ),
        (
            "int a = 3 * (2 + 2)",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=MultiplyExpression(
                    Integer(3, (1, 9)),
                    AddExpresion(Integer(2, (1, 14)), Integer(2, (1, 18))),
                ),
                position=(1, 1),
            ),
        ),
        (
            "bool a = some_bool",
            Variable(
                "a",
                TypeAnnotation.BOOL,
                value=Identifier("some_bool", (1, 10)),
                position=(1, 1),
            ),
        ),
        (
            "bool a = true",
            Variable(
                "a",
                TypeAnnotation.BOOL,
                value=Bool(True, (1, 10)),
                position=(1, 1),
            ),
        ),
        (
            "bool a = false",
            Variable(
                "a",
                TypeAnnotation.BOOL,
                value=Bool(False, (1, 10)),
                position=(1, 1),
            ),
        ),
    ],
)
def test_variable_declaration_multiply(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_variable_declaration()
    assert expression == expected
