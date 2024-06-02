import pytest
from parser.statements.after_statement import AfterStatement
from parser.statements.block import Block
from parser.tests.test_utils import create_parser
from parser.values.string import String
from parser.variable import Variable
from parser.type_annotations import TypeAnnotation


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            'after {\nstr name = "dawid"\n}',
            AfterStatement(
                Block(
                    [
                        Variable(
                            "name",
                            type=TypeAnnotation.STR,
                            value=String("dawid", (2, 12)),
                            position=(2, 1),
                        ),
                    ],
                ),
            ),
        ),
    ],
)
def test_after_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_after_statement()
    assert expression == expected
