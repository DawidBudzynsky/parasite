import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.or_expression import OrExpression
from projekt.src.parser.values.plus_expression import AddExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("a or b", OrExpression("a", "b")),
        ("a and b", AndExpression("a", "b")),
        ("1 and (2+3)", AndExpression(1, AddExpresion(2, 3))),
        ("a or b or c", OrExpression(OrExpression("a", "b"), "c")),
        ("a or b and c", OrExpression("a", AndExpression("b", "c"))),
    ],
)
def test_or_expression(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_expression()
    assert expression == expected
