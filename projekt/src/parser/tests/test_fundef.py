import pytest
from parser.function import FunctionDef
from parser.statements.block import Block
from parser.statements.return_statement import ReturnStatement
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.identifier_expression import Identifier
from parser.variable import Variable


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "func(num: int) int {\nreturn num }",
            FunctionDef(
                "func",
                [Variable("num", TypeAnnotation.INT, position=(1, 6))],
                TypeAnnotation.INT,
                Block(
                    [ReturnStatement(Identifier("num", (2, 8)))],
                ),
                (1, 1),
            ),
        ),
    ],
)
def test_fun_def(input_str, expected):
    parser = create_parser(input_str)
    expressions = []
    parser.parse_fun_def(expressions.append)
    assert expressions[0] == expected
