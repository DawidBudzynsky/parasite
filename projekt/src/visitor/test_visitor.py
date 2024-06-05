import pytest
from parser.function import FunctionDef
from parser.statements.aspect_block_statement import AspectBlock
from parser.statements.aspect_statement import Aspect
from parser.statements.assign_statement import AssignStatement
from parser.statements.before_statement import BeforeStatement
from parser.statements.block import Block
from parser.statements.for_each_statement import ForEachStatement
from parser.statements.fun_call_statement import FunCallStatement
from parser.statements.if_statement import IfStatement
from parser.statements.loop_statement import LoopStatement
from parser.statements.return_statement import ReturnStatement
from parser.type_annotations import TypeAnnotation
from parser.values.and_expression import AndExpression
from parser.values.bool import Bool
from parser.values.divide_expression import DivideExpression
from parser.values.equals_expression import EqualsExpression
from parser.values.greater_expression import GreaterExpression
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.float import Float
from parser.values.less_expression import LessExpresion
from parser.values.minus_expression import SubtractExpression
from parser.values.minus_negate_expression import MinusNegateExpression
from parser.values.multiply_expression import MultiplyExpression
from parser.values.negate_expression import NegateExpression
from parser.values.not_equals_expression import NotEqualsExpression
from parser.values.object_access_expression import ObjectAccessExpression
from parser.values.or_expression import OrExpression
from parser.values.plus_expression import AddExpresion
from parser.values.string import String
from parser.variable import Variable
from parser.values.casting_expression import CastingExpression
from visitor.scope import Scope, ScopeObject, ScopeVariable
from visitor.visitor import CodeVisitor


@pytest.mark.parametrize(
    "input_expression, expected",
    [
        (
            AddExpresion(
                AddExpresion(
                    Integer(1, position=(1, 1)),
                    Integer(2, position=(1, 2)),
                    position=(0, 0),
                ),
                Integer(3, position=(1, 3)),
                position=(1, 2),
            ),
            6,
        ),
        (
            AddExpresion(
                String("a", position=(1, 1)),
                String("b", position=(1, 2)),
                position=(0, 0),
            ),
            "ab",
        ),
        (
            AddExpresion(
                Float(1.0, position=(1, 1)),
                Integer(2, position=(1, 2)),
                position=(0, 0),
            ),
            3.0,
        ),
        (MinusNegateExpression(Integer(1, position=(1, 1))), -1),
        (MinusNegateExpression(Float(1.5, position=(1, 1))), -1.5),
        (
            SubtractExpression(
                Integer(2, position=(1, 1)),
                Integer(1, position=(1, 2)),
                position=(0, 0),
            ),
            1,
        ),
        (
            SubtractExpression(
                Float(2, position=(1, 1)), Integer(1, position=(1, 2)), position=(0, 0)
            ),
            1.0,
        ),
        (
            MultiplyExpression(
                Float(2, position=(1, 1)), Integer(3, position=(1, 2)), position=(0, 0)
            ),
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
            EqualsExpression(
                Integer(1, position=(1, 1)),
                Integer(1, position=(1, 2)),
                position=(0, 0),
            ),
            True,
        ),
        (
            NotEqualsExpression(
                Integer(1, position=(1, 1)),
                Integer(2, position=(1, 2)),
                position=(0, 0),
            ),
            True,
        ),
        (
            NotEqualsExpression(
                Integer(1, position=(1, 1)),
                Integer(1, position=(1, 2)),
                position=(0, 0),
            ),
            False,
        ),
    ],
)
def test_add_expression(input_expression, expected):
    v = CodeVisitor()
    input_expression.accept(v)
    result = v.last_result
    assert result == expected


def test_assign():
    v = CodeVisitor()
    Variable(
        name="a",
        value=Integer(1, position=(0, 0)),
        type=TypeAnnotation.INT,
        position=(1, 1),
    ).accept(v)
    AssignStatement(
        identifier=Identifier("a", position=(0, 0)),
        expression=AddExpresion(
            Integer(2, position=(2, 1)), Integer(2, position=(2, 2)), position=(0, 0)
        ),
        position=(1, 1),
    ).accept(v)
    scope = Scope()
    scope.variables = {"a": ScopeVariable(value=4, type=TypeAnnotation.INT)}
    assert v.curr_scope == scope


def test_return():
    v = CodeVisitor()
    v.curr_scope = Scope(parent=None, variables={})
    ReturnStatement(
        expression=AddExpresion(
            Integer(2, position=(1, 1)), Integer(2, position=(1, 2)), position=(0, 0)
        )
    ).accept(v)
    result = v.last_result
    assert result == 4
    assert v.returning_flag


def test_visit_fun_call():
    v = CodeVisitor()
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
                            position=(0, 0),
                        ),
                        position=(0, 0),
                    ),
                    ReturnStatement(expression=Identifier("c", position=(0, 0))),
                ]
            ),
            position=(0, 0),
        )
    }
    FunCallStatement(
        identifier="add",
        arguments=[Integer(1, position=(0, 0)), Integer(2, position=(0, 0))],
        position=(0, 0),
    ).accept(v)
    result = v.last_result
    assert result == 3


def test_visit_while():
    v = CodeVisitor()
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
                                position=(0, 0),
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
    v = CodeVisitor()
    v.curr_scope.variables = {
        "function": ScopeObject(name="test_fun", value=None, type=None, args=None)
    }
    ObjectAccessExpression(
        left_expression=Identifier("function", position=(0, 0)),
        right_expression=Identifier("name", position=(0, 0)),
    ).accept(v)
    result = v.last_result
    assert result == "test_fun"


def test_object_access_v2():
    v = CodeVisitor()
    v.curr_scope.variables = {
        "arg": ScopeObject(
            type=TypeAnnotation.STR, name="arg", value="hello", args=None
        ),
    }
    ObjectAccessExpression(
        left_expression=Identifier("arg", position=(0, 0)),
        right_expression=Identifier("type", position=(0, 0)),
    ).accept(v)
    result = v.last_result
    assert result == TypeAnnotation.STR


# for arg in function.args {
#     if arg.value == 2 {
#         return "arg is 2"
#     }
# }


def test_for_each_statement():
    v = CodeVisitor()
    v.curr_scope = Scope(
        parent=None,
        variables={
            "function": ScopeObject(
                type=FunctionDef,
                name="fun_name",
                value=None,
                args=[
                    ScopeObject(name="a", value=1, type=TypeAnnotation.INT, args=None),
                    ScopeObject(name="b", value=2, type=TypeAnnotation.INT, args=None),
                ],
            )
        },
    )
    ForEachStatement(
        identifier=Identifier("arg", position=(0, 0)),
        expression=ObjectAccessExpression(
            left_expression=Identifier(name="function", position=(0, 0)),
            right_expression=Identifier(name="args", position=(0, 0)),
        ),
        block=Block(
            statements=[
                IfStatement(
                    conditions_instructions=[
                        (
                            EqualsExpression(
                                left_expression=ObjectAccessExpression(
                                    left_expression=Identifier(
                                        name="arg", position=(0, 0)
                                    ),
                                    right_expression=Identifier(
                                        name="value", position=(0, 0)
                                    ),
                                ),
                                right_expression=Integer(2, position=(0, 0)),
                            ),
                            Block(
                                statements=[
                                    ReturnStatement(
                                        String(value="arg is 2", position=(0, 0))
                                    )
                                ]
                            ),
                        )
                    ],
                    else_instructions=None,
                    position=(0, 0),
                )
            ]
        ),
    ).accept(v)
    result = v.last_result
    assert result == "arg is 2"


# fun1(a,b)int{
#   return a + b
# }
#
# aspect asp1(fun1){
#   before{
#       int var = 0
#   }
# }


def test_fun_call_with_aspect():
    v = CodeVisitor()
    v.aspects = {
        "asp1": Aspect(
            identifier="asp1",
            aspect_args=["fun1"],
            aspect_block=AspectBlock(
                variables=[],
                before_statement=BeforeStatement(
                    block=Block(
                        statements=[
                            Variable(
                                name="var",
                                type=TypeAnnotation.INT,
                                value=Integer(0, position=(0, 0)),
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
            parameters=[
                Variable(name="a", type=TypeAnnotation.INT),
                Variable(name="b", type=TypeAnnotation.INT),
            ],
            type=TypeAnnotation.INT,
            block=Block(
                statements=[
                    ReturnStatement(
                        expression=AddExpresion(
                            left_expression=Identifier("a", position=(0, 0)),
                            right_expression=Identifier("b", position=(0, 0)),
                            position=(0, 0),
                        )
                    ),
                ]
            ),
            position=(0, 0),
        ),
    }
    v.fun_aspect_map = {"fun1": [v.aspects.get("asp1")]}

    FunCallStatement(
        identifier="fun1",
        arguments=[
            Integer(value=1, position=(0, 0)),
            Integer(value=2, position=(0, 0)),
        ],
        position=(0, 0),
    ).accept(v)
    result = v.aspects_scope_map.get("asp1").peek().variables.get("function").name
    assert result == "fun1"


# fun1(a: int) str {
#     if a > 2 {
#         return "a>2"
#     } else {
#         return "a<2"
#     }
# }


def test_visit_if_statement():
    v = CodeVisitor()
    v.curr_scope = Scope(
        parent=None,
        variables={"a": ScopeVariable(value=3, type=TypeAnnotation.INT)},
    )
    IfStatement(
        conditions_instructions=[
            (
                GreaterExpression(
                    left_expression=Identifier("a", position=(0, 0)),
                    right_expression=Integer(value=2, position=(0, 0)),
                ),
                Block(
                    statements=[ReturnStatement(String(value="a>2", position=(0, 0)))]
                ),
            )
        ],
        else_instructions=Block(
            statements=[ReturnStatement(String(value="a<2", position=(0, 0)))]
        ),
        position=(0, 0),
    ).accept(v)
    result = v.last_result
    assert result == "a>2"


def test_print_func():
    v = CodeVisitor()
    import io
    import sys

    captured_output = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output
    FunCallStatement(
        identifier="print", arguments=[String(value="a", position=(0, 0))]
    ).accept(v)
    sys.stdout = original_stdout
    assert captured_output.getvalue().rstrip() == "a"


def test_visit_cast():
    v = CodeVisitor()
    CastingExpression(
        term=Integer(value="0", position=(0, 0)), type=TypeAnnotation.BOOL
    ).accept(v)
    result = v.last_result
    assert result is False


@pytest.mark.parametrize(
    "input_expression, expected",
    [
        (
            CastingExpression(
                term=Integer(value=0, position=(0, 0)),
                type=TypeAnnotation.BOOL,
                position=(0, 0),
            ),
            False,
        ),
        (
            CastingExpression(
                term=Integer(value=0, position=(0, 0)),
                type=TypeAnnotation.FLOAT,
                position=(0, 0),
            ),
            0.0,
        ),
        (
            CastingExpression(
                term=Integer(value=0, position=(0, 0)),
                type=TypeAnnotation.STR,
                position=(0, 0),
            ),
            "0",
        ),
        (
            CastingExpression(
                term=String(value="12", position=(0, 0)),
                type=TypeAnnotation.BOOL,
                position=(0, 0),
            ),
            True,
        ),
        (
            CastingExpression(
                term=Float(value=12.0, position=(0, 0)),
                type=TypeAnnotation.INT,
                position=(0, 0),
            ),
            12,
        ),
        (
            CastingExpression(
                term=Float(value=12.0, position=(0, 0)),
                type=TypeAnnotation.STR,
                position=(0, 0),
            ),
            "12.0",
        ),
        (
            CastingExpression(
                term=Float(value=12.0, position=(0, 0)),
                type=TypeAnnotation.BOOL,
                position=(0, 0),
            ),
            True,
        ),
    ],
)
def test_visit_cast_table_test(input_expression, expected):
    v = CodeVisitor()
    input_expression.accept(v)
    result = v.last_result
    assert result == expected
