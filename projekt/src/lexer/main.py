from lexer import Lexer
from tokens import Token, Type
from reader import Source


file_name = "testfile.txt"
with open(file_name, "r") as file:

    source = Source(file)
    lexer = Lexer(source)

    token = Token()
    while token.token_type != Type.ETX:
        token = lexer.build_next_token()
        print(token)
