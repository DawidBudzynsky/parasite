import pytest
from parser.statements.block import Block
from parser.statements.if_statement import IfStatement
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.less_expression import LessExpresion
from parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            """if a<2 { \nint b = 12 \n}""",
            IfStatement(
                conditions_instructions=[
                    (
                        LessExpresion(Identifier("a", (1, 4)), Integer(2, (1, 6))),
                        Block(
                            [
                                Variable(
                                    "b", TypeAnnotation.INT, Integer(12, (2, 9)), (2, 1)
                                ),
                            ]
                        ),
                    ),
                ],
                else_instructions=None,
                position=(1, 1),
            ),
        ),
    ],
)
def test_if_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_if_statement()
    assert expression == expected
