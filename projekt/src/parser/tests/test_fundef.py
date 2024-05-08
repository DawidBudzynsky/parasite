import pytest
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.variable import Variable


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
    # __import__("pdb").set_trace()
    parser.parse_fun_def(expressions.append)
    assert expressions[0] == expected
