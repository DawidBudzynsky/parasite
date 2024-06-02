import pytest
from parser.statements.block import Block
from parser.statements.return_statement import ReturnStatement
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.identifier_expression import Identifier
from parser.values.string import String
from parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            '{\nstr name = "dawid"\nreturn name }',
            Block(
                [
                    Variable(
                        "name",
                        type=TypeAnnotation.STR,
                        value=String("dawid", (2, 12)),
                        position=(2, 1),
                    ),
                    ReturnStatement(Identifier("name", (3, 8))),
                ],
            ),
        ),
    ],
)
def test_parse_block(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_block()
    assert expression == expected
