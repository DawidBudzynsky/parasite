import pytest
from projekt.src.parser.exceptions import AspectArgument, AspectBodyError, InvalidSyntax
from projekt.src.parser.statements.after_statement import AfterStatement
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.statements.aspect_statement import Aspect
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            'aspect aspect_func(func1, func2){\nint var1 = 12\nbefore{\nstr name = "dawid"\n}\nafter{\nint num = 2\n}}',
            Aspect(
                identifier=Identifier("aspect_func", (1, 8)),
                aspect_args=[
                    Identifier("func1", (1, 20)),
                    Identifier("func2", (1, 27)),
                ],
                aspect_block=AspectBlock(
                    [
                        Variable(
                            Identifier("var1", (2, 5)),
                            "int",
                            value=Integer(12, (2, 12)),
                            position=(2, 1),
                        )
                    ],
                    BeforeStatement(
                        [
                            Variable(
                                Identifier("name", (4, 5)),
                                type="str",
                                value=String("dawid", (4, 12)),
                                position=(4, 1),
                            ),
                        ],
                    ),
                    AfterStatement(
                        [
                            Variable(
                                Identifier("num", (7, 5)),
                                type="int",
                                value=Integer(2, (7, 11)),
                                position=(7, 1),
                            ),
                        ],
                    ),
                ),
            ),
        ),
        (
            'aspect logging_aspect(func){\nbefore{\nprint("Entering function:", func.name)\n}\nafter{\nprint("Exiting function:", func.name)\n}}',
            Aspect(
                identifier=Identifier("logging_aspect", (1, 8)),
                aspect_args=[Identifier("func", (1, 23))],
                aspect_block=AspectBlock(
                    [],
                    BeforeStatement(
                        [
                            FunCallStatement(
                                Identifier("print", (3, 1)),
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
                    AfterStatement(
                        [
                            FunCallStatement(
                                Identifier("print", (6, 1)),
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
        ),
    ],
)
def test_aspect_definition(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_aspect_definition()
    assert expression == expected


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
                position=(1, 22),
                expected_type="(",
            ),
        ),
    ],
)
def test_aspect_definition_fails(input_str, expected):
    with pytest.raises(Exception) as e_info:
        parser = create_parser(input_str)
        parser.parse_aspect_definition()

    assert isinstance(e_info.value, type(expected))
    assert str(e_info.value) == str(expected)
