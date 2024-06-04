import pytest
from parser.tests.test_utils import create_parser
from parser.type_annotations import TypeAnnotation
from parser.values.identifier_expression import Identifier
from parser.values.is_expression import IsExpression


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            """arg is int""",
            IsExpression(
                left_expression=Identifier(name="arg", position=(1, 1)),
                right_expression=TypeAnnotation.INT,
            ),
        ),
    ],
)
def test_if_statement(input_str, expected):
    parser = create_parser(input_str)
    expression = parser.parse_relation()
    assert expression == expected
