import pytest
from projekt.src.parser.exceptions import (
    ASSIGN_OR_CALL_MISSING,
    FUN_CALL_NOT_CLOSED,
    InvalidSyntax,
    InvalidSyntaxVerbose,
    MissingExpression,
)
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "a = 5",
            AssignStatement(Identifier("a", (1, 1)), Integer(5, (1, 5))),
        ),
        (
            "fun(var1, 2)",
            FunCallStatement(
                "fun",
                arguments=[Identifier("var1", (1, 5)), Integer(2, (1, 11))],
            ),
        ),
    ],
)
def test_assign_or_call(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_assign_or_call()
    assert expression == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "fun*",
            InvalidSyntaxVerbose(
                message=ASSIGN_OR_CALL_MISSING % ("(", "="),
                position=(1, 4),
            ),
        ),
        (
            "fun(fun2",
            InvalidSyntax(
                message=FUN_CALL_NOT_CLOSED,
                position=(1, 9),
                expected_type=")",
            ),
        ),
        (
            "fun = ",
            MissingExpression(
                operator="=",
                position=(1, 7),
            ),
        ),
    ],
)
def test_relation_fails(input_str, expected):
    with pytest.raises(Exception) as e_info:
        parser = create_parser(input_str)
        parser.parse_assign_or_call()

    assert isinstance(e_info.value, type(expected))
    assert str(e_info.value) == str(expected)
