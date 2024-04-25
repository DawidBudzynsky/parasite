from typing import List
from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.tokens import Token, Type
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.variable import Variable

TYPES = [Type.INTEGER_TYPE, Type.FLOAT_TYPE, Type.STRING_TYPE, Type.BOOL_TYPE]


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = Token()
        self.consume_token()

    def consume_token(self):
        self.token = self.lexer.build_next_token()

    def __add_to_dict(self, dictionary, key, value):
        if key in dictionary:
            raise ValueError(f"Key '{key}' already exists in the dictionary.")
        else:
            dictionary[key] = value

    def __must_be(self, *types):
        if self.token.token_type not in types:
            raise ValueError("synatx error czy cos")
        value = self.token.value
        self.consume_token()
        return value

    # program = { function_definition | aspect_definition } ;
    def parse_program(self):
        functions = {}
        while fun_def := self.parse_fun_def():
            try:
                self.__add_to_dict(functions, fun_def.identifier, fun_def)
            except ValueError as e:
                print(e)
        return Program(functions)

    # function_definition = identifier, "(", [ parameters ], ")", [ type ], block ;
    def parse_fun_def(self) -> FunctionDef | None:
        if self.token.token_type != Type.IDENTIFIER:
            return None

        # name = self.token.value
        position = self.token.position
        name = self.__must_be(Type.IDENTIFIER)

        self.__must_be(Type.PAREN_OPEN)
        parameters = self.parse_parameters()
        self.__must_be(Type.PAREN_CLOSE)

        # NOTE: czy funkcja void powina mieć type None?
        type = self.parse_type_annotation()
        if (block := self.parse_block()) is None:
            raise ValueError("nie ma bloku")
        return FunctionDef(name, parameters, type, block, position)

    # parameters = identifier, ":", type, { ",", identifier, ":", type } ;
    def parse_parameters(self) -> List | None:
        parameters = []
        if (parameter := self.parse_parameter()) is None:
            return parameters
        parameters.append(parameter)
        while self.token.token_type == Type.COMMA:
            self.consume_token()
            if (parameter := self.parse_parameter()) is None:
                raise ValueError("blad skladniowy")
            parameters.append(parameter)
        return parameters

    # parameter = identifier, ":", type
    def parse_parameter(self):
        if self.token.token_type != Type.IDENTIFIER:
            return None

        position = self.token.position  # idk moze niepotrzebne
        identifier = self.__must_be(Type.IDENTIFIER)

        self.__must_be(Type.COLON)
        type = self.__must_be(*TYPES)
        return Variable(identifier, type, position)

    def parse_type_annotation(self):
        if self.token.token_type not in TYPES:
            return None
        value = self.token.value
        self.consume_token()
        return value

    # block = "{", {statement}, "}" ;
    def parse_block(self):
        self.__must_be(Type.BRACE_OPEN)
        if (statement := self.parse_statement()) is None:
            raise ValueError("brak stamentu")
        statements = []
        statements.append(statement)
        while (statement := self.parse_statement()) is not None:
            statements.append(statement)
        self.__must_be(Type.BRACE_CLOSE)
        return statements

    def parse_statement(self):
        pass

    # variable_declaration = type, identifier, "=", expression ;
    def parse_variable_declaration(self):
        if self.token.token_type not in TYPES:
            return None
        position = self.token.position
        type = self.parse_type_annotation()
        identifier = self.__must_be(Type.IDENTIFIER)
        self.__must_be(Type.ASSIGNMENT)
        value = self.parse_expression()
        return Variable(identifier, type, value, position)

    # if_statement = "if", expression, block, { "elif", expression, block }, ["else", block] ;
    def parse_if_statement(self):
        if self.token.token_type != Type.IF:
            return None
        self.consume_token()

        value = self.parse_expression()
        block = self.parse_block()

        while self.token.token_type == Type.ELIF:
            value = self.parse_expression()
            block = self.parse_block()

        if self.token.token_type == Type.ELSE:
            block = self.parse_block()

    def parse_loop_statement(self):
        pass

    def parse_for_each_statement(self):
        pass

    def parse_assign_or_call(self):
        pass

    def parse_return_statement(self):
        pass

    def parse_expression(self):
        pass
