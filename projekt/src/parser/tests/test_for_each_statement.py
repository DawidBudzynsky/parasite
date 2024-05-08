import pytest
from projekt.src.parser.statements.for_each_statement import ForEachStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression


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
            ),
        ),
    ],
)
def test_for_each_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_for_each_statement()
    assert expression == expected
