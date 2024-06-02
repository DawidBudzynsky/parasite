from io import StringIO

from lexer.lexer import Lexer
from lexer.reader import Source
from parser.parser import Parser


def create_parser(string: str):
    source = Source(StringIO(string))
    lexer = Lexer(source)
    return Parser(lexer)
