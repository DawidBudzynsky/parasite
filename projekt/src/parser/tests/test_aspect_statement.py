import pytest
from parser.exceptions import (
    ASPECT_DEF_PAREN_OPEN_MISSING,
    AspectArgument,
    AspectBodyError,
    InvalidSyntax,
)
from parser.statements.after_statement import AfterStatement
from parser.statements.before_statement import BeforeStatement
from parser.statements.aspect_block_statement import AspectBlock
from parser.statements.aspect_statement import Aspect
from parser.statements.block import Block
from parser.statements.fun_call_statement import FunCallStatement
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.object_access_expression import ObjectAccessExpression
from parser.values.string import String
from parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            'aspect aspect_func(func1, func2){\nint var1 = 12\nbefore{\nstr name = "dawid"\n}\nafter{\nint num = 2\n}}',
            Aspect(
                identifier="aspect_func",
                aspect_args=[
                    Identifier("func1", (1, 20)),
                    Identifier("func2", (1, 27)),
                ],
                aspect_block=AspectBlock(
                    [
                        Variable(
                            "var1",
                            TypeAnnotation.INT,
                            value=Integer(12, (2, 12)),
                            position=(2, 1),
                        )
                    ],
                    BeforeStatement(
                        Block(
                            [
                                Variable(
                                    "name",
                                    type=TypeAnnotation.STR,
                                    value=String("dawid", (4, 12)),
                                    position=(4, 1),
                                ),
                            ],
                        ),
                    ),
                    AfterStatement(
                        Block(
                            [
                                Variable(
                                    "num",
                                    type=TypeAnnotation.INT,
                                    value=Integer(2, (7, 11)),
                                    position=(7, 1),
                                ),
                            ],
                        ),
                    ),
                ),
                position=(1, 1),
            ),
        ),
        (
            'aspect logging_aspect(func){\nbefore{\nprint("Entering function:", func.name)\n}\nafter{\nprint("Exiting function:", func.name)\n}}',
            Aspect(
                identifier="logging_aspect",
                aspect_args=[Identifier("func", (1, 23))],
                aspect_block=AspectBlock(
                    [],
                    BeforeStatement(
                        Block(
                            [
                                FunCallStatement(
                                    "print",
                                    arguments=[
                                        String("Entering function:", (3, 7)),
                                        ObjectAccessExpression(
                                            Identifier("func", (3, 29)),
                                            Identifier("name", (3, 34)),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    AfterStatement(
                        Block(
                            [
                                FunCallStatement(
                                    "print",
                                    arguments=[
                                        String("Exiting function:", (6, 7)),
                                        ObjectAccessExpression(
                                            Identifier("func", (6, 28)),
                                            Identifier("name", (6, 33)),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ),
                position=(1, 1),
            ),
        ),
    ],
)
def test_aspect_definition(input_str, expected):
    parser = create_parser(input_str)
    expressions = []
    parser.parse_aspect_definition(expressions.append)
    assert expressions[0] == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "aspect logging_aspect(func){}",
            AspectBodyError(position=(1, 29)),
        ),
        (
            "aspect logging_aspect(){}",
            AspectArgument(position=(1, 23)),
        ),
        (
            "aspect logging_aspect{}",
            InvalidSyntax(
                message=ASPECT_DEF_PAREN_OPEN_MISSING,
                position=(1, 22),
                expected_type="(",
            ),
        ),
    ],
)
def test_aspect_definition_fails(input_str, expected):
    with pytest.raises(Exception) as e_info:
        expressions = []
        parser = create_parser(input_str)
        parser.parse_aspect_definition(expressions.append)

    assert isinstance(e_info.value, type(expected))
    assert str(e_info.value) == str(expected)
