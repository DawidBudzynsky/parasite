from _pytest import assertion
import pytest
from reader import Source
from io import StringIO


def test_read():
    test_data = [
        {
            "input": "abc",
            "expected_chars": ["a", "b", "c"],
            "expected_pos": [(1, 1), (1, 2), (1, 3)],
        },
        {
            "input": "hello\nworld",
            "expected_chars": ["h", "e", "l", "l", "o", "\n", "w", "o", "r", "l", "d"],
            "expected_pos": [
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 5),
                (1, 6),
                (2, 1),
                (2, 2),
                (2, 3),
                (2, 4),
                (2, 5),
            ],
        },
    ]
    for test_case in test_data:
        reader = Source(StringIO(test_case.get("input")))
        result_chars = []
        result_position = []
        while char := reader.get_char():
            result_chars.append(char)
            result_position.append(reader.get_position())
            reader.next()
        assert result_chars == test_case.get("expected_chars")
        assert result_position == test_case.get("expected_pos")


def test_multiple_eof():
    input = ""
    expected_chars = ""
    reader = Source(StringIO(input))
    char = reader.get_char()
    assert char == expected_chars


def test_backslash_r():
    input = "\r\tt\t\r\na"
    expected_chars = "\r\tt\t\na"
    reader = Source(StringIO(input))
    f = []
    while char := reader.get_char():
        f.append(char)
        reader.next()
    assert "".join(f) == expected_chars
