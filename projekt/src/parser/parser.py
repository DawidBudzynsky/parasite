from typing import List

from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.tokens import Token, Type
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.casting_expression import CastingExpression
from projekt.src.parser.values.divide_expression import DivideExpression
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.values.equals_expression import EqualsExpression
from projekt.src.parser.values.function_call import FunctionCall
from projekt.src.parser.values.greater_equal_expression import GreaterEqualExpression
from projekt.src.parser.values.greater_expression import GreaterExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.is_expression import IsExpression
from projekt.src.parser.values.less_equal_expression import LessEqualExpresion
from projekt.src.parser.values.less_expression import LessExpresion
from projekt.src.parser.values.minus_negate_expression import MinusNegateExpression
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.negate_expression import NegateExpression
from projekt.src.parser.values.minus_expression import SubtractExpression
from projekt.src.parser.values.not_equals_expression import NotEqualsExpression
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression
from projekt.src.parser.values.or_expression import OrExpression
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.variable import Variable


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = Token()
        self.consume_token()
        self.addition_map = {
            Type.PLUS: AddExpresion,
            Type.MINUS: SubtractExpression,
        }
        self.multiply_or_divide_map = {
            Type.MULTIPLY: MultiplyExpression,
            Type.DIVIDE: DivideExpression,
        }
        self.unary_map = {
            Type.MINUS: MinusNegateExpression,
            Type.NEGATE: NegateExpression,
        }
        self.relation_operators = {
            Type.GREATER: GreaterExpression,
            Type.GREATER_EQUAL: GreaterEqualExpression,
            Type.LESS: LessExpresion,
            Type.LESS_EQUAL: LessEqualExpresion,
            Type.EQUALS: EqualsExpression,
            Type.NOT_EQUALS: NotEqualsExpression,
            Type.IS: IsExpression,
        }
        self.types = [
            Type.INTEGER_TYPE,
            Type.FLOAT_TYPE,
            Type.STRING_TYPE,
            Type.BOOL_TYPE,
        ]

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
        type = self.__must_be(*self.types)
        return Variable(identifier, type, position=position)

    def parse_type_annotation(self):
        if self.token.token_type not in self.types:
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

    # TODO: parse_statement
    def parse_statement(self):
        pass

    # variable_declaration = type, identifier, "=", expression ;
    def parse_variable_declaration(self):
        if self.token.token_type not in self.types:
            return None
        position = self.token.position
        type = self.parse_type_annotation()
        identifier = self.__must_be(Type.IDENTIFIER)
        self.__must_be(Type.ASSIGNMENT)
        value = self.parse_expression()
        return Variable(identifier, type, value, position)

    # expression = conjunction, { "or", conjunction } ;
    def parse_expression(self):
        if (left_logic_factor := self.parse_conjunction()) is None:
            return None
        while self.token.token_type == Type.OR:
            # position = self.token.position
            self.consume_token()
            if (right_logic_factor := self.parse_conjunction()) is None:
                raise ValueError("brak expression po OR")
            left_logic_factor = OrExpression(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # conjunction = relation_term, { "and", relation_term } ;
    def parse_conjunction(self):
        if (left_logic_factor := self.parse_relation()) is None:
            return None
        while self.token.token_type == Type.AND:
            # position = self.token.position
            self.consume_token()
            if (right_logic_factor := self.parse_relation()) is None:
                raise ValueError("brak expression po AND")
            left_logic_factor = AndExpression(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # relation_term = additive_term, [ relation_operator, additive_term ] ;
    # (2+2) < a
    def parse_relation(self):
        if (left_logic_factor := self.parse_additive()) is None:
            return None

        if (constructor := self.relation_operators.get(self.token.token_type)) is None:
            return left_logic_factor

        if (right_logic_factor := self.parse_additive()) is None:
            raise ValueError("brak expression po operatorze")
        left_logic_factor = constructor(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # additive_term = multiplicative_term, { ("+" | "-"), multiplicative_term } ;
    def parse_additive(self):
        if (left_logic_factor := self.parse_multiplicative()) is None:
            return None
        while (constructor := self.addition_map.get(self.token.token_type)) is not None:
            # position = self.token.position  # NOTE: not sure if i need it here
            self.consume_token()
            if (right_logic_factor := self.parse_multiplicative()) is None:
                raise ValueError("brak expression po AND")
            left_logic_factor = constructor(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # multiplicative_term = unary_application, { ("*" | "/"), unary_application } ;
    def parse_multiplicative(self):
        if (left_logic_factor := self.parse_unary()) is None:
            return None
        # self.consume_token()
        while (
            constructor := self.multiply_or_divide_map.get(self.token.token_type)
        ) is not None:
            # position = self.token.position  # NOTE: not sure if i need it here
            self.consume_token()
            if (right_logic_factor := self.parse_unary()) is None:
                raise ValueError("brak expression po AND")
            left_logic_factor = constructor(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # unary_application = [ ("-" | "!") ], casting ;
    def parse_unary(self):
        if (constructor := self.unary_map.get(self.token.token_type)) is None:
            return self.parse_casting()
        casting = self.parse_casting()
        return constructor(casting)

    # casting = term, [ "->", type ] ;
    def parse_casting(self):
        if (term := self.parse_term()) is None:
            return None

        if self.token.token_type != Type.CAST:
            return term

        self.__must_be(Type.CAST)
        type = self.parse_type_annotation()
        return CastingExpression(term, type)

    # term = integer | float | bool | string | object_access | "(", expression, ")";
    def parse_term(self):
        # NOTE: somehow i have to ensure what type is returned
        value = self.token.value
        match self.token.token_type:
            case Type.IDENTIFIER:
                self.consume_token()
                return value
            case Type.INTEGER:
                self.consume_token()
                return value
            case Type.FLOAT:
                self.consume_token()
                return value
            case Type.BOOL:
                self.consume_token()
                return value
            case Type.STRING:
                self.consume_token()
                return value
            case Type.PAREN_OPEN:
                self.consume_token()
                expression = self.parse_expression()
                self.__must_be(Type.PAREN_CLOSE)
                return expression

    # object_access = identifier_or_call, {".", identifier_or_call}
    def parse_object_access(self):
        if (left_item := self.parse_identifier_or_call()) is None:
            return None
        while self.token.token_type == Type.DOT:
            self.consume_token()
            if (right_item := self.parse_identifier_or_call()) is None:
                raise ValueError("brak item po '.'")
            left_item = ObjectAccessExpression(left_item, right_item)
        return left_item

    # identifier_or_call = identifier, ["(", arguments, ")"]
    def parse_identifier_or_call(self):
        if self.token.token_type != Type.IDENTIFIER:
            return None
        # identifier = self.parse_identifier() NOTE: może potem zrobić
        position = self.token.position
        name = self.__must_be(Type.IDENTIFIER)
        identifier = Identifier(name, position)

        if self.token.token_type != Type.PAREN_OPEN:
            return identifier
        self.consume_token()
        arguments = self.parse_arguments()
        self.__must_be(Type.PAREN_CLOSE)
        return FunctionCall(identifier, arguments)

    # arguments = [ expression, {",", expression } ] ;
    def parse_arguments(self):
        expressions = []
        if (left_expr := self.parse_expression()) is None:
            return expressions
        expressions.append(left_expr)
        while self.token.token_type == Type.COMMA:
            self.consume_token()
            if (right_expr := self.parse_expression()) is None:
                raise ValueError("nie ma expression po przecinku")
            expressions.append(right_expr)
        return expressions

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
