import pytest
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.statements.aspect_statement import Aspect
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.statements.program import Program
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression


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
