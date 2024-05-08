import pytest
from projekt.src.parser.statements.after_statement import AfterStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable
from projekt.src.parser.type_annotations import TypeAnnotation


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            'after{\nstr name = "dawid"\n}',
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
