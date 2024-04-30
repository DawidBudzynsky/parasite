from projekt.src.parser.tests.test_utils import create_parser
from projekt.src.parser.variable import Variable


def test_parse_parameter_number():
    parser = create_parser("number: int")
    expected = Variable("number", "int", position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameter_string():
    parser = create_parser("name: str")
    expected = Variable("name", "str", position=(1, 1))
    print(expected)
    a = parser.parse_parameter()
    assert a == expected


def test_parse_parameters_multiple():
    parser = create_parser("number: int, name: str, dec_num: float, is_ok: bool")
    expected = [
        Variable("number", "int", position=(1, 1)),
        Variable("name", "str", position=(1, 13)),
        Variable("dec_num", "float", position=(1, 24)),
        Variable("is_ok", "bool", position=(1, 40)),
    ]
    a = parser.parse_parameters()
    print(a)
    assert a == expected
