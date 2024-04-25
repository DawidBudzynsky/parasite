from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.tokens import Token, Type
from projekt.src.lexer.reader import Source


file_name = "testfile.txt"
with open(file_name, "r") as file:

    source = Source(file)
    lexer = Lexer(source)

    token = Token()
    while token.token_type != Type.ETX:
        token = lexer.build_next_token()
        print(token)
