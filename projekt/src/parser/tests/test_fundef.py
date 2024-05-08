import pytest
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "func(num: int) int {\nreturn num }",
            FunctionDef(
                Identifier("func", (1, 1)),
                [Variable(Identifier("num", (1, 6)), "int", position=(1, 6))],
                "int",
                [ReturnStatement(Identifier("num", (2, 8)))],
                (1, 1),
            ),
        ),
    ],
)
def test_fun_def(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_fun_def()
    assert expression == expected
