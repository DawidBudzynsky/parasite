import pytest
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.bool import Bool
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.multiply_expression import MultiplyExpression
from parser.values.plus_expression import AddExpresion
from parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "int a = 1 * 3",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=MultiplyExpression(
                    Integer(1, (1, 9)), Integer(3, (1, 13)), position=(1, 11)
                ),
                position=(1, 1),
            ),
        ),
        (
            "int a = 1 + 2",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=AddExpresion(
                    Integer(1, (1, 9)), Integer(2, (1, 13)), position=(1, 11)
                ),
                position=(1, 1),
            ),
        ),
        (
            "int a = 1 * 2 + 1",
            Variable(
                "a",
                TypeAnnotation.INT,
                value=AddExpresion(
                    MultiplyExpression(
                        Integer(1, (1, 9)), Integer(2, (1, 13)), position=(1, 11)
                    ),
                    Integer(1, (1, 17)),
                    position=(1, 15),
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
                    AddExpresion(
                        Integer(2, (1, 14)), Integer(2, (1, 18)), position=(1, 16)
                    ),
                    position=(1, 11),
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
