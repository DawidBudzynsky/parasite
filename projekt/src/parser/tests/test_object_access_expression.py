import pytest
from parser.statements.fun_call_statement import FunCallStatement
from parser.tests.test_utils import create_parser
from parser.values.identifier_expression import Identifier
from parser.values.object_access_expression import ObjectAccessExpression


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "obj.name",
            ObjectAccessExpression(
                Identifier("obj", (1, 1)), Identifier("name", (1, 5))
            ),
        ),
        (
            "getFirst().name",
            ObjectAccessExpression(
                FunCallStatement("getFirst", [], (1, 1)),
                Identifier("name", (1, 12)),
            ),
        ),
        (
            "function.arg.type",
            ObjectAccessExpression(
                ObjectAccessExpression(
                    Identifier("function", (1, 1)), Identifier("arg", (1, 10))
                ),
                Identifier("type", (1, 14)),
            ),
        ),
    ],
)
def test_or_expression(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_object_access()
    assert expression == expected
