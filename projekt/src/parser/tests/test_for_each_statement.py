import pytest
from parser.statements.block import Block
from parser.statements.for_each_statement import ForEachStatement
from parser.tests.test_utils import create_parser
from parser.values.identifier_expression import Identifier
from parser.values.object_access_expression import ObjectAccessExpression


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "for a in function.args {}",
            ForEachStatement(
                Identifier("a", (1, 5)),
                ObjectAccessExpression(
                    Identifier("function", (1, 10)), Identifier("args", (1, 19))
                ),
                Block([]),
            ),
        ),
    ],
)
def test_for_each_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_for_each_statement()
    assert expression == expected
