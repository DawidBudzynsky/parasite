import pytest
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.for_each_statement import ForEachStatement
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.statements.if_statement import IfStatement
from projekt.src.parser.statements.loop_statement import LoopStatement
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.greater_equal_expression import GreaterEqualExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.less_expression import LessExpresion
from projekt.src.parser.values.minus_expression import SubtractExpression
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
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
                    )
                ],
                else_instructions=[],
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
                            Identifier("var2", (1, 20)), Integer(10, (1, 27))
                        )
                    ],
                ),
            ),
        ),
        (
            "for a in function.args {}",
            ForEachStatement(
                Identifier("a", (1, 5)),
                ObjectAccessExpression(
                    Identifier("function", (1, 10)), Identifier("args", (1, 19))
                ),
                Block([]),
            ),
        ),
        (
            "a = 5",
            AssignStatement(Identifier("a", (1, 1)), Integer(5, (1, 5))),
        ),
        (
            "fun(var1, 2)",
            FunCallStatement(
                "fun",
                arguments=[Identifier("var1", (1, 5)), Integer(2, (1, 11))],
            ),
        ),
        (
            "return ((7+3)*(4-2))",
            ReturnStatement(
                MultiplyExpression(
                    AddExpresion(Integer(7, (1, 10)), Integer(3, (1, 12))),
                    SubtractExpression(Integer(4, (1, 16)), Integer(2, (1, 18))),
                )
            ),
        ),
    ],
)
def test_parse_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_statement()
    assert expression == expected
