from lexer.errors import LexerError
from lexer.reader import Source
from lexer.tokens import Token, Symbol, Type
import sys
from io import StringIO


class Lexer:
    def __init__(self, source: Source):
        self.source = source
        self.position = self.source.get_position()
        self.string_limit = 200
        self.identifier_limit = 200
        self.errors_map = {
            "invalid_escape": "Error, invalid escaping sequence",
            "unclosed_string": "Error, unclosed string;",
            "token_build_failed": "Error, lexer was unable to create token;",
            "string_length": f"Error, string too long, {self.string_limit} char is max;",
            "identifier_length": f"Error, identifier too long, {self.identifier_limit} char is max;",
        }
        self.operators = {
            "{": lambda: self.build_one_char_operator(Type.BRACE_OPEN),
            "}": lambda: self.build_one_char_operator(Type.BRACE_CLOSE),
            "(": lambda: self.build_one_char_operator(Type.PAREN_OPEN),
            ")": lambda: self.build_one_char_operator(Type.PAREN_CLOSE),
            "*": lambda: self.build_one_char_operator(Type.MULTIPLY),
            "+": lambda: self.build_one_char_operator(Type.PLUS),
            ",": lambda: self.build_one_char_operator(Type.COMMA),
            ":": lambda: self.build_one_char_operator(Type.COLON),
            ".": lambda: self.build_one_char_operator(Type.DOT),
            "!": lambda: self.build_two_char_operator(Type.NOT, Type.NOT_EQUALS, "="),
            "-": lambda: self.build_two_char_operator(Type.MINUS, Type.CAST, ">"),
            "<": lambda: self.build_two_char_operator(Type.LESS, Type.LESS_EQUAL, "="),
            ">": lambda: self.build_two_char_operator(
                Type.GREATER, Type.GREATER_EQUAL, "="
            ),
            "=": lambda: self.build_two_char_operator(
                Type.ASSIGNMENT, Type.EQUALS, "="
            ),
        }

    def build_one_char_operator(self, type):
        self.consume()
        return type

    def build_two_char_operator(self, type_one, type_two, expected):
        self.consume()
        if self.source.get_char() == expected:
            self.consume()
            return type_two
        return type_one

    def consume(self):
        self.source.next()
        self.position = self.source.get_position()
        return self.source.get_char()

    def ignore_white_spaces(self):
        while self.source.get_char().isspace():
            self.consume()

    def build_next_token(self):
        self.ignore_white_spaces()
        if token := self.try_to_match():
            return token
        raise LexerError(self.errors_map.get("token_build_failed"), self.position)

    def build_number(self, position):
        if not self.source.get_char().isdecimal():
            return None

        value = int(self.source.get_char())
        self.consume()
        if value != 0:
            while self.source.get_char().isdecimal():
                digit = int(self.source.get_char())
                if value > (sys.maxsize - digit) / 10:
                    raise LexerError(self.errors_map.get("int_max_size"))
                value = value * 10 + digit
                self.consume()

        if self.source.get_char() != ".":
            return Token(Type.INTEGER, value, position)
        self.consume()

        decimals = 0
        dec_value = 0
        while self.source.get_char().isdecimal():
            digit = int(self.source.get_char())
            if dec_value > (sys.maxsize - digit) / 10:
                raise LexerError(self.errors_map.get("int_max_size"))
            dec_value = dec_value * 10 + digit
            decimals += 1
            self.consume()

        return Token(
            Type.FLOAT,
            float(value) + float(dec_value) / pow(10, float(decimals)),
            position,
        )

    def build_identifier(self, position):
        if not self.source.get_char().isalpha():
            return None

        identifier = StringIO()
        identifier.write(self.source.get_char())
        self.consume()
        while (
            self.source.get_char().isalpha()
            or self.source.get_char().isdecimal()
            or self.source.get_char() == "_"
        ):
            if len(identifier.getvalue()) >= 200:
                raise LexerError(self.errors_map.get("string_length"), self.position)
            identifier.write(self.source.get_char())
            self.consume()

        identifier = identifier.getvalue()
        return Token(
            Symbol.key_words.get(identifier, Type.IDENTIFIER), identifier, position
        )

    def handle_escaping(self):
        if self.source.get_char() != "\\":
            return self.source.get_char()
        character = self.consume()
        match character:
            case "n":
                return "\n"
            case "t":
                return "\t"
            case '"':
                return '"'
            case "\\":
                return "\\"
            case _:
                raise LexerError(self.errors_map.get("invalid_escape"), self.position)

    def build_string(self, position):
        if self.source.get_char() != '"':
            return None
        string_builder = StringIO()
        self.consume()
        while self.source.get_char() != '"' and self.source.get_char() != "":
            character_to_append = self.handle_escaping()
            if len(string_builder.getvalue()) >= 200:
                raise LexerError(
                    self.errors_map.get("identifier_length"), self.position
                )
            string_builder.write(character_to_append)
            self.consume()

        if self.source.get_char() != '"':
            raise LexerError(self.errors_map.get("unclosed_string"), self.position)

        self.consume()
        return Token(Type.STRING, string_builder.getvalue(), position)

    def build_comment_or_divide(self, position):
        buff = self.source.get_char()
        if buff != "/":
            return None
        character = self.source.next()
        if character is not None and buff + character == "//":
            self.consume()
            string_builder = StringIO()
            while self.source.get_char() != "\n" and self.source.get_char() != "":
                if len(string_builder.getvalue()) >= 200:
                    raise LexerError(
                        self.errors_map.get("string_length"), self.position
                    )
                string_builder.write(self.source.get_char())
                self.consume()
            return Token(Type.COMMENT, string_builder.getvalue(), position)
        else:
            return Token(Type.DIVIDE, None, position)

    def build_operator(self, position):
        buff = self.source.get_char()
        if fun := self.operators.get(buff):
            return Token(fun(), None, position)
        else:
            return None

    def try_to_match(self):
        position = self.position

        try:
            if self.source.get_char() == "":
                return Token(Type.ETX, None, position)

            if token := self.build_comment_or_divide(position):
                return token

            if token := self.build_string(position):
                return token

            if token := self.build_operator(position):
                return token

            if token := self.build_number(position):
                return token

            if token := self.build_identifier(position):
                return token
            return None
        except LexerError as e:
            print(e)
