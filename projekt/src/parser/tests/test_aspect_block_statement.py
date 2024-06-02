import pytest
from parser.statements.after_statement import AfterStatement
from parser.statements.before_statement import BeforeStatement
from parser.statements.aspect_block_statement import AspectBlock
from parser.statements.block import Block
from parser.tests.test_utils import create_parser
from parser.values.integer import Integer
from parser.values.string import String
from parser.variable import Variable
from parser.type_annotations import TypeAnnotation


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            '{\nint var1 = 12\nbefore{\nstr name = "dawid"\n}\nafter{\nint num = 2\n}}',
            AspectBlock(
                [
                    Variable(
                        "var1",
                        type=TypeAnnotation.INT,
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
                    )
                ),
            ),
        ),
    ],
)
def test_aspect_block(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_aspect_block()
    assert expression == expected
