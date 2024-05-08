from io import StringIO

from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.reader import Source
from projekt.src.parser.parser import Parser


def create_parser(string: str):
    source = Source(StringIO(string))
    lexer = Lexer(source)
    return Parser(lexer)
