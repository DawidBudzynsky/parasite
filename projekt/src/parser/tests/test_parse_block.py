import pytest
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            '{\nstr name = "dawid"\nreturn name }',
            [
                Variable(
                    Identifier("name", (2, 5)),
                    type="str",
                    value=String("dawid", (2, 12)),
                    position=(2, 1),
                ),
                ReturnStatement(Identifier("name", (3, 8))),
            ],
        ),
    ],
)
def test_parse_block(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_block()
    assert expression == expected
