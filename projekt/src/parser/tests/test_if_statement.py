import pytest
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.if_statement import IfStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.less_expression import LessExpresion
from projekt.src.parser.variable import Variable


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
                else_instructions=[],
            ),
        ),
    ],
)
def test_if_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_if_statement()
    assert expression == expected
