from _pytest.main import pytest_collect_directory
import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.function_call import FunctionCall
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression


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
                FunctionCall(Identifier("getFirst", (1, 1))),
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
# NOTE: right now, each side before and after the "DOT" is an Identifier, not sure if it should be like that
def test_or_expression(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_object_access()
    assert expression == expected
