import pytest
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.minus_expression import SubtractExpression
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.plus_expression import AddExpresion


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "return variable",
            ReturnStatement(Identifier("variable", (1, 8))),
        ),
        (
            "return (20+14)",
            ReturnStatement(AddExpresion(Integer(20, (1, 9)), Integer(14, (1, 12)))),
        ),
        (
            "return ((7+3)*(4-2))",
            ReturnStatement(
                MultiplyExpression(
                    AddExpresion(Integer(7, (1, 10)), Integer(3, (1, 12))),
                    SubtractExpression(Integer(4, (1, 16)), Integer(2, (1, 18))),
                )
            ),
        ),
        (
            "return ((7+3) * identifier1)",
            ReturnStatement(
                MultiplyExpression(
                    AddExpresion(Integer(7, (1, 10)), Integer(3, (1, 12))),
                    Identifier("identifier1", (1, 17)),
                )
            ),
        ),
    ],
)
def test_return_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_return_statement()
    assert expression == expected
