import pytest
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            'before{\nstr name = "dawid"\n}',
            BeforeStatement(
                Block(
                    [
                        Variable(
                            "name",
                            type=TypeAnnotation.STR,
                            value=String("dawid", (2, 12)),
                            position=(2, 1),
                        ),
                    ],
                )
            ),
        ),
    ],
)
def test_before_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_before_statement()
    assert expression == expected
