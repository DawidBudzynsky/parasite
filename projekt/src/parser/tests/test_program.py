import pytest
from parser.exceptions import AspectRedefinition, FunctionRedefinition
from parser.function import FunctionDef
from parser.statements.aspect_block_statement import AspectBlock
from parser.statements.aspect_statement import Aspect
from parser.statements.before_statement import BeforeStatement
from parser.statements.block import Block
from parser.statements.fun_call_statement import FunCallStatement
from parser.statements.program import Program
from parser.statements.return_statement import ReturnStatement
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.object_access_expression import ObjectAccessExpression


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            """fun1() int {\nreturn 1\n}\naspect aspect1(fun1){\nbefore{\nprint(fun1.arg)\n}\n}\n}""",
            Program(
                functions={
                    "fun1": FunctionDef(
                        identifier="fun1",
                        parameters=[],
                        type=TypeAnnotation.INT,
                        position=(1, 1),
                        block=Block([ReturnStatement(Integer(1, (2, 8)))]),
                    )
                },
                aspects={
                    "aspect1": Aspect(
                        identifier="aspect1",
                        aspect_args=[Identifier("fun1", (4, 16))],
                        position=(4, 1),
                        aspect_block=AspectBlock(
                            variables=[],
                            before_statement=BeforeStatement(
                                Block(
                                    [
                                        FunCallStatement(
                                            "print",
                                            arguments=[
                                                ObjectAccessExpression(
                                                    Identifier("fun1", (6, 7)),
                                                    Identifier("arg", (6, 12)),
                                                )
                                            ],
                                        )
                                    ]
                                )
                            ),
                        ),
                    )
                },
            ),
        ),
    ],
)
def test_program(input_str, expected):
    parser = create_parser(input_str)
    program = parser.parse_program()
    assert program == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "fun1(){\nprint(1)\n}\nfun1(){\nprint(2)\n}",
            FunctionRedefinition(function_name="fun1", position=(4, 1)),
        ),
        (
            "fun1(){\nprint(1)\n}\nfun1(arg1: int, arg2: str){\nprint(2)\n}",
            FunctionRedefinition(function_name="fun1", position=(4, 1)),
        ),
        (
            'aspect asp(fun1){\nbefore{print("aspect before triggered")}\n}\naspect asp(fun2){\nbefore{print("aspect before triggered")}\n}',
            AspectRedefinition(aspect_name="asp", position=(4, 8)),
        ),
    ],
)
def test_aspect_definition_fails(input_str, expected):
    with pytest.raises(Exception) as e_info:
        parser = create_parser(input_str)
        parser.parse_program()

    assert isinstance(e_info.value, type(expected))
    assert str(e_info.value) == str(expected)
