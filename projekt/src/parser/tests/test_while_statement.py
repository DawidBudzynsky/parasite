from typing_extensions import ParamSpec
import pytest
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.loop_statement import LoopStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.greater_equal_expression import GreaterEqualExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.less_expression import LessExpresion
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "while i<5 {}",
            LoopStatement(
                LessExpresion(Identifier("i", (1, 7)), Integer(5, (1, 9))), Block([])
            ),
        ),
        (
            "while var1 >= 12 {}",
            LoopStatement(
                GreaterEqualExpression(
                    Identifier("var1", (1, 7)), Integer(12, (1, 15))
                ),
                Block([]),
            ),
        ),
        (
            "while var1 >= 12 { var2 = 10 }",
            LoopStatement(
                GreaterEqualExpression(
                    Identifier("var1", (1, 7)), Integer(12, (1, 15))
                ),
                Block(
                    [
                        AssignStatement(
                            Identifier("var2", (1, 20)),
                            Integer(10, (1, 27)),
                            position=(1, 20),
                        )
                    ],
                ),
            ),
        ),
        (
            "while var1 >= 12 { int var2 = 5 \nvar2 = 10 }",
            LoopStatement(
                GreaterEqualExpression(
                    Identifier("var1", (1, 7)), Integer(12, (1, 15))
                ),
                Block(
                    [
                        Variable(
                            "var2",
                            TypeAnnotation.INT,
                            value=Integer(5, (1, 31)),
                            position=(1, 20),
                        ),
                        AssignStatement(
                            Identifier("var2", (2, 1)),
                            Integer(10, (2, 8)),
                            position=(2, 1),
                        ),
                    ],
                ),
            ),
        ),
    ],
)
def test_while_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_loop_statement()
    assert expression == expected
