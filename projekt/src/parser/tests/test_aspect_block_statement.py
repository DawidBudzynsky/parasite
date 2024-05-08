import pytest
from projekt.src.parser.statements.after_statement import AfterStatement
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            '{\nint var1 = 12\nbefore{\nstr name = "dawid"\n}\nafter{\nint num = 2\n}}',
            AspectBlock(
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
    ],
)
def test_aspect_block(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_aspect_block()
    assert expression == expected
