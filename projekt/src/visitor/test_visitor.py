import pytest
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.statements.aspect_statement import Aspect
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.for_each_statement import ForEachStatement
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.statements.loop_statement import LoopStatement
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.bool import Bool
from projekt.src.parser.values.divide_expression import DivideExpression
from projekt.src.parser.values.equals_expression import EqualsExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.float import Float
from projekt.src.parser.values.less_expression import LessExpresion
from projekt.src.parser.values.minus_expression import SubtractExpression
from projekt.src.parser.values.minus_negate_expression import MinusNegateExpression
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.negate_expression import NegateExpression
from projekt.src.parser.values.not_equals_expression import NotEqualsExpression
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression
from projekt.src.parser.values.or_expression import OrExpression
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable
from projekt.src.visitor.scope import Scope, ScopeObject, ScopeVariable
from projekt.src.visitor.visitor import ParserVisitor


@pytest.mark.parametrize(
    "input_expression, expected",
    [
        (
            AddExpresion(
                AddExpresion(Integer(1, position=(1, 1)), Integer(2, position=(1, 2))),
                Integer(3, position=(1, 3)),
            ),
            6,
        ),
        (
            AddExpresion(
                String("a", position=(1, 1)),
                String("b", position=(1, 2)),
            ),
            "ab",
        ),
        (
            AddExpresion(
                Float(1.0, position=(1, 1)),
                Integer(2, position=(1, 2)),
            ),
            3.0,
        ),
        (MinusNegateExpression(Integer(1, position=(1, 1))), -1),
        (MinusNegateExpression(Float(1.5, position=(1, 1))), -1.5),
        (
            SubtractExpression(
                Integer(2, position=(1, 1)), Integer(1, position=(1, 2))
            ),
            1,
        ),
        (
            SubtractExpression(Float(2, position=(1, 1)), Integer(1, position=(1, 2))),
            1.0,
        ),
        (
            MultiplyExpression(Float(2, position=(1, 1)), Integer(3, position=(1, 2))),
            6.0,
        ),
        (
            DivideExpression(Float(6, position=(1, 1)), Integer(3, position=(1, 2))),
            2.0,
        ),
        (
            NegateExpression(Bool(True, position=(1, 1))),
            False,
        ),
        (
            AndExpression(Bool(True, position=(1, 1)), Bool(False, position=(1, 2))),
            False,
        ),
        (
            OrExpression(Bool(True, position=(1, 1)), Bool(False, position=(1, 2))),
            True,
        ),
        (
            EqualsExpression(Integer(1, position=(1, 1)), Integer(1, position=(1, 2))),
            True,
        ),
        # NOTE: works with integer == float now
        (
            EqualsExpression(Integer(1, position=(1, 1)), Float(1, position=(1, 2))),
            True,
        ),
        (
            NotEqualsExpression(
                Integer(1, position=(1, 1)), Integer(2, position=(1, 2))
            ),
            True,
        ),
        (
            NotEqualsExpression(
                Integer(1, position=(1, 1)), Integer(1, position=(1, 2))
            ),
            False,
        ),
    ],
)
def test_add_expression(input_expression, expected):
    v = ParserVisitor()
    result = input_expression.accept(v)
    assert result == expected


def test_assign():
    v = ParserVisitor()
    Variable(
        name="a",
        value=Integer(1, position=(0, 0)),
        type=TypeAnnotation.INT,
        position=(1, 1),
    ).accept(v)
    AssignStatement(
        identifier=Identifier("a", position=(0, 0)),
        expression=AddExpresion(
            Integer(2, position=(2, 1)), Integer(2, position=(2, 2))
        ),
        position=(1, 1),
    ).accept(v)
    scope = Scope()
    scope.variables = {"a": ScopeVariable(value=4, type=TypeAnnotation.INT)}
    assert v.curr_scope == scope


def test_return():
    v = ParserVisitor()
    v.curr_scope = Scope(parent=None, return_type=TypeAnnotation.INT, variables={})
    result = ReturnStatement(
        expression=AddExpresion(
            Integer(2, position=(1, 1)), Integer(2, position=(1, 2))
        )
    ).accept(v)
    assert result == 4
    assert v.returning_flag


def test_visit_fun_call():
    v = ParserVisitor()
    v.functions = {
        "add": FunctionDef(
            identifier="add",
            parameters=[
                Variable(name="a", type=TypeAnnotation.INT),
                Variable(name="b", type=TypeAnnotation.INT),
            ],
            type=TypeAnnotation.INT,
            block=Block(
                statements=[
                    Variable(
                        name="c",
                        type=TypeAnnotation.INT,
                        value=AddExpresion(
                            Identifier("a", position=(0, 0)),
                            Identifier("b", position=(0, 0)),
                        ),
                        position=(0, 0),
                    ),
                    ReturnStatement(expression=Identifier("c", position=(0, 0))),
                ]
            ),
            position=(0, 0),
        )
    }
    result = FunCallStatement(
        identifier="add",
        arguments=[Integer(1, position=(0, 0)), Integer(2, position=(0, 0))],
        position=(0, 0),
    ).accept(v)
    assert result == 3


def test_visit_while():
    v = ParserVisitor()
    Block(
        statements=[
            Variable(
                name="i", type=TypeAnnotation.INT, value=Integer(0, position=(0, 0))
            ),
            LoopStatement(
                expression=LessExpresion(
                    left_expression=Identifier(name="i", position=(0, 0)),
                    right_expression=Integer(3, position=(0, 0)),
                ),
                block=Block(
                    statements=[
                        AssignStatement(
                            Identifier(name="i", position=(0, 0)),
                            AddExpresion(
                                left_expression=Identifier(name="i", position=(0, 0)),
                                right_expression=Integer(1, position=(0, 0)),
                            ),
                            position=(0, 0),
                        )
                    ]
                ),
            ),
        ]
    ).accept(v)
    res = v.curr_scope.variables.get("i").value
    assert res == 3


def test_object_access():
    v = ParserVisitor()
    v.curr_scope.variables = {
        "function": ScopeVariable(
            type=FunctionDef,
            value={"name": "test_fun"},
        )
    }
    result = ObjectAccessExpression(
        left_expression=Identifier("function", position=(0, 0)),
        right_expression=Identifier("name", position=(0, 0)),
    ).accept(v)
    assert result == "test_fun"


def test_object_access_v2():
    v = ParserVisitor()
    v.curr_scope.variables = {
        "arg": ScopeVariable(
            type=TypeAnnotation.INT,
            value={"type": TypeAnnotation.STR},
        )
    }
    result = ObjectAccessExpression(
        left_expression=Identifier("arg", position=(0, 0)),
        right_expression=Identifier("type", position=(0, 0)),
    ).accept(v)
    assert result == TypeAnnotation.STR


# def test_for_each_statement():
#     v = ParserVisitor()
#     v.curr_scope.variables = {
#         "function": ScopeVariable(
#             type=None,
#             value={"args": [{""}]},
#         )
#     }
#     result = ForEachStatement(
#         identifier=Identifier("a", position=(0, 0)),
#         expression=ObjectAccessExpression(
#             left_expression=Identifier(name="function", position=(0, 0)),
#             right_expression=Identifier(name="args", position=(0, 0)),
#         ),
#     )
#     assert result == TypeAnnotation.STR


def test_fun_call_with_aspect():
    v = ParserVisitor()
    v.aspects = {
        "aspect1": Aspect(
            identifier="aspect1",
            aspect_args=["fun1", "fun2"],
            aspect_block=AspectBlock(
                variables=[
                    Variable(
                        name="i",
                        value=Integer(value=0, position=(0, 0)),
                        type=TypeAnnotation.INT,
                        position=(0, 0),
                    )
                ],
                before_statement=BeforeStatement(
                    block=Block(
                        statements=[
                            AssignStatement(
                                identifier=Identifier("i", position=(0, 0)),
                                expression=AddExpresion(
                                    left_expression=Identifier(
                                        name="i", position=(0, 0)
                                    ),
                                    right_expression=Integer(value=1, position=(0, 0)),
                                ),
                                position=(0, 0),
                            )
                        ]
                    )
                ),
            ),
            position=(0, 0),
        )
    }
    v.functions = {
        "fun1": FunctionDef(
            identifier="fun1",
            parameters=[],
            block=Block(
                statements=[
                    Variable(
                        name="var",
                        type=TypeAnnotation.INT,
                        value=Integer(1, position=(0, 0)),
                    )
                ]
            ),
            type=TypeAnnotation.INT,
            position=(0, 0),
        ),
        "fun2": FunctionDef(
            identifier="fun2",
            parameters=[],
            block=Block(
                statements=[
                    Variable(
                        name="var2",
                        # TODO: it doesnt matter what fun return type is set right now, repair it
                        type=None,
                        value=Integer(1, position=(0, 0)),
                    )
                ]
            ),
            type=TypeAnnotation.INT,
            position=(0, 0),
        ),
    }
    v.fun_aspect_map = {"fun1": ["aspect1"], "fun2": ["aspect1"]}
    # __import__("pdb").set_trace()
    FunCallStatement(identifier="fun1", arguments=[], position=(0, 0)).accept(v)
    FunCallStatement(identifier="fun2", arguments=[], position=(0, 0)).accept(v)
    result = v.aspects_scope_map.get("aspect1").peek().variables.get("i").value
    assert result == 2
