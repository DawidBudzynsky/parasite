import pytest
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.or_expression import OrExpression
from projekt.src.parser.values.plus_expression import AddExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("a or b", OrExpression(Identifier("a", (1, 1)), Identifier("b", (1, 6)))),
        ("a and b", AndExpression(Identifier("a", (1, 1)), Identifier("b", (1, 7)))),
        (
            "1 and (2+3)",
            AndExpression(
                Integer(1, (1, 1)),
                AddExpresion(Integer(2, (1, 8)), Integer(3, (1, 10))),
            ),
        ),
        (
            "a or b or c",
            OrExpression(
                OrExpression(Identifier("a", (1, 1)), Identifier("b", (1, 6))),
                Identifier("c", (1, 11)),
            ),
        ),
        (
            "a or b and c",
            OrExpression(
                Identifier("a", (1, 1)),
                AndExpression(Identifier("b", (1, 6)), Identifier("c", (1, 12))),
            ),
        ),
    ],
)
def test_or_expression(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_expression()
    assert expression == expected
