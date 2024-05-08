from typing import List
from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.tokens import Token, Type
from projekt.src.parser.statements.after_statement import AfterStatement
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.statements.aspect_statement import Aspect
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.for_each_statement import ForEachStatement
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.statements.if_statement import IfStatement
from projekt.src.parser.statements.loop_statement import LoopStatement
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.bool import Bool
from projekt.src.parser.values.casting_expression import CastingExpression
from projekt.src.parser.values.divide_expression import DivideExpression
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.values.equals_expression import EqualsExpression
from projekt.src.parser.values.float import Float
from projekt.src.parser.values.function_call import FunctionCall
from projekt.src.parser.values.greater_equal_expression import GreaterEqualExpression
from projekt.src.parser.values.greater_expression import GreaterExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
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
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable
from projekt.src.parser.exceptions import (
    AspectArgument,
    AspectBodyError,
    InvalidSyntax,
    MissingExpression,
    MissingStatement,
)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = Token()
        self.consume_token()
        self.symbols_map = {
            Type.GREATER: ">",
            Type.GREATER_EQUAL: ">=",
            Type.LESS: "<",
            Type.LESS_EQUAL: "<=",
            Type.PLUS: "+",
            Type.MINUS: "-",
            Type.MULTIPLY: "*",
            Type.DIVIDE: "/",
            Type.AND: "and",
            Type.OR: "or",
            Type.ASSIGNMENT: "=",
            Type.PAREN_OPEN: "(",
            Type.PAREN_CLOSE: ")",
        }
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
            Type.NOT: NegateExpression,
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
            raise InvalidSyntax(
                position=self.token.position,
                expected_type=self.symbols_map.get(*types),
            )
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
        return functions

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
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )
        return FunctionDef(
            Identifier(name, position), parameters, type, block, position
        )

    # parameters = identifier, ":", type, { ",", identifier, ":", type } ;
    def parse_parameters(self) -> List | None:
        parameters = []
        if (parameter := self.parse_parameter()) is None:
            return parameters
        parameters.append(parameter)
        while self.token.token_type == Type.COMMA:
            self.consume_token()
            if (parameter := self.parse_parameter()) is None:
                raise InvalidSyntax(
                    position=self.token.position,
                    expected_type=Type.IDENTIFIER,
                    given_type=self.token.token_type,
                )
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
        return Variable(Identifier(identifier, position), type, position=position)

    def parse_type_annotation(self):
        if self.token.token_type not in self.types:
            return None
        value = self.token.value
        self.consume_token()
        return value

    # block = "{", {statement}, "}" ;
    def parse_block(self):
        self.__must_be(Type.BRACE_OPEN)
        statements = []
        if (statement := self.parse_statement()) is None:
            return statements  # NOTE: mozemy mieć pusty blok
        statements.append(statement)
        while (statement := self.parse_statement()) is not None:
            statements.append(statement)
        self.__must_be(Type.BRACE_CLOSE)
        return statements

    # statement = variable_declaration | if_statement | loop_statement | for_each_statement | assign_or_call | return_statement ;
    def parse_statement(self):
        if (
            statement := self.parse_variable_declaration()
            or self.parse_if_statement()
            or self.parse_loop_statement()
            or self.parse_for_each_statement()
            or self.parse_assign_or_call()
            or self.parse_return_statement()
        ):
            return statement
        return None

    # variable_declaration = type, identifier, "=", expression ;
    def parse_variable_declaration(self):
        if self.token.token_type not in self.types:
            return None

        position = self.token.position
        type = self.parse_type_annotation()

        identifier_pos = self.token.position
        identifier = self.__must_be(Type.IDENTIFIER)
        self.__must_be(Type.ASSIGNMENT)
        value = self.parse_expression()
        return Variable(Identifier(identifier, identifier_pos), type, value, position)

    # expression = conjunction, { "or", conjunction } ;
    def parse_expression(self):
        if (left_logic_factor := self.parse_conjunction()) is None:
            return None
        while self.token.token_type == Type.OR:
            self.consume_token()
            if (right_logic_factor := self.parse_conjunction()) is None:
                raise MissingStatement(
                    missing_statement=f"expression after [{self.symbols_map.get(Type.OR)}] operator",
                    position=self.token.position,
                )
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
                raise MissingStatement(
                    missing_statement=f"expression after [{self.symbols_map.get(Type.AND)}] operator",
                    position=self.token.position,
                )
            left_logic_factor = AndExpression(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # relation_term = additive_term, [ relation_operator, additive_term ] ;
    # (2+2) < a
    def parse_relation(self):
        if (left_logic_factor := self.parse_additive()) is None:
            return None

        if (constructor := self.relation_operators.get(self.token.token_type)) is None:
            return left_logic_factor
        operator_symbol = self.symbols_map.get(self.token.token_type)
        self.consume_token()

        if (right_logic_factor := self.parse_additive()) is None:
            raise MissingExpression(
                operator=operator_symbol,
                position=self.token.position,
            )

        left_logic_factor = constructor(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # additive_term = multiplicative_term, { ("+" | "-"), multiplicative_term } ;
    def parse_additive(self):
        if (left_logic_factor := self.parse_multiplicative()) is None:
            return None
        while (constructor := self.addition_map.get(self.token.token_type)) is not None:
            operator_symbol = self.symbols_map.get(self.token.token_type)
            self.consume_token()
            if (right_logic_factor := self.parse_multiplicative()) is None:
                raise MissingExpression(
                    operator=operator_symbol,
                    position=self.token.position,
                )

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
            operator_symbol = self.symbols_map.get(self.token.token_type)
            self.consume_token()
            if (right_logic_factor := self.parse_unary()) is None:
                raise MissingExpression(
                    operator=operator_symbol,
                    position=self.token.position,
                )
            left_logic_factor = constructor(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # unary_application = [ ("-" | "!") ], casting ;
    def parse_unary(self):
        if (constructor := self.unary_map.get(self.token.token_type)) is None:
            return self.parse_casting()
        self.consume_token()
        position = self.token.position
        casting = self.parse_casting()
        return constructor(casting, position)

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
        value = self.token.value
        position = self.token.position
        match self.token.token_type:
            case Type.IDENTIFIER:
                return self.parse_object_access()
            case Type.INTEGER:
                self.consume_token()
                return Integer(value, position)
            case Type.FLOAT:
                self.consume_token()
                return Float(value, position)
            case Type.BOOL:
                self.consume_token()
                return Bool(value, position)
            case Type.STRING:
                self.consume_token()
                return String(value, position)
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
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.DOT),
                    position=self.token.position,
                )
            left_item = ObjectAccessExpression(left_item, right_item)
        return left_item

    # identifier_or_call = identifier, ["(", arguments, ")"]
    def parse_identifier_or_call(self):
        if self.token.token_type != Type.IDENTIFIER:
            return None
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
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.COMMA),
                    position=self.token.position,
                )
            expressions.append(right_expr)
        return expressions

    # if_statement = "if", expression, block, { "elif", expression, block }, ["else", block] ;
    def parse_if_statement(self):
        if self.token.token_type != Type.IF:
            return None
        self.consume_token()

        conditions = []
        if (expression := self.parse_expression()) is None:
            raise MissingExpression(
                operator=self.symbols_map.get(Type.IF), position=self.token.position
            )
        conditions.append(expression)

        if_instructions = []
        true_instructions = self.parse_block()  # NOTE: statements can be empty []
        if_instructions.append(true_instructions)

        while self.token.token_type == Type.ELIF:
            self.consume_token()
            if (expression := self.parse_expression()) is None:
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.ELIF),
                    position=self.token.position,
                )
            conditions.append(expression)
            true_instructions = self.parse_block()
            if_instructions.append(true_instructions)

        else_instructions = []
        if self.token.token_type == Type.ELSE:
            self.consume_token()
            else_instructions = self.parse_block()
        return IfStatement(conditions, if_instructions, else_instructions)

    # loop_statement = "while", expression, block ;
    def parse_loop_statement(self):
        if self.token.token_type != Type.WHILE:
            return None
        self.consume_token()
        expression = self.parse_expression()
        block = self.parse_block()
        return LoopStatement(expression, block)

    # for_each_statement = "for", idientifier, "in", expression, block ; NOTE: maybe expression here should be only object_access
    def parse_for_each_statement(self):
        if self.token.token_type != Type.FOR_EACH:
            return None
        self.consume_token()

        identifier_pos = self.token.position
        identifier = self.__must_be(Type.IDENTIFIER)
        self.__must_be(Type.IN)

        expression = self.parse_expression()
        block = self.parse_block()
        return ForEachStatement(
            Identifier(identifier, identifier_pos), expression, block
        )

    # assign_or_call = identifier, [ "(", arguments, ")" ], [ "=", expression ] ;
    def parse_assign_or_call(self):
        if self.token.token_type != Type.IDENTIFIER:
            return None
        identifier = self.token.value
        position = self.token.position
        self.consume_token()

        match self.token.token_type:
            case Type.PAREN_OPEN:
                self.consume_token()
                arguments = self.parse_arguments()
                self.__must_be(Type.PAREN_CLOSE)
                return FunCallStatement(
                    Identifier(identifier, position),
                    arguments,
                )
            case Type.ASSIGNMENT:
                self.consume_token()
                expression = self.parse_expression()
                return AssignStatement(Identifier(identifier, position), expression)
            case _:
                raise InvalidSyntax(
                    position=self.token.position,
                    expected_type=[
                        self.symbols_map.get(Type.PAREN_OPEN),
                        self.symbols_map.get(Type.ASSIGNMENT),
                    ],
                )

    # return_statement = "return", [ expression ] ;
    def parse_return_statement(self):
        if self.token.token_type != Type.RETURN:
            return None
        self.consume_token()
        expression = self.parse_expression()
        return ReturnStatement(expression)

    def identifier_or_regex(self):
        match self.token.token_type:
            case Type.IDENTIFIER:
                return self.parse_identifier_or_call()
            case Type.STRING:
                return self.token.value
            case _:
                raise AspectArgument(position=self.token.position)

    # NOTE: idk if regex is best option
    # aspect_definition = "aspect", identifier, "(", (identifier | string) {"," (identifier | string), ")", aspect_block;
    def parse_aspect_definition(self):
        if self.token.token_type != Type.ASPECT:
            return None
        self.consume_token()
        aspect_pos = self.token.position
        aspect_name = self.__must_be(Type.IDENTIFIER)
        self.__must_be(Type.PAREN_OPEN)

        aspect_args = []
        aspect_args.append(self.identifier_or_regex())

        while self.token.token_type == Type.COMMA:
            self.consume_token()
            aspect_args.append(self.identifier_or_regex())

        self.__must_be(Type.PAREN_CLOSE)
        aspect_block = self.parse_aspect_block()
        return Aspect(Identifier(aspect_name, aspect_pos), aspect_args, aspect_block)

    # aspect_block = "{", { variable_declaration }, aspect_member "}" ;
    def parse_aspect_block(self):
        self.__must_be(Type.BRACE_OPEN)
        variables = []
        while (variable := self.parse_variable_declaration()) is not None:
            variables.append(variable)
        aspect_members = self.parse_aspect_member()
        self.__must_be(Type.BRACE_CLOSE)
        return AspectBlock(variables, *aspect_members)

    # aspect_member = ( before_statement, [ after_statement ] ) |  after_statement) ;  NOTE:changes in EBNF
    def parse_aspect_member(self):
        if (before_statement := self.parse_before_statement()) is None:
            if (after_statement := self.parse_after_statement()) is None:
                raise AspectBodyError(position=self.token.position)
        after_statement = self.parse_after_statement()
        return before_statement, after_statement

    # before_statement = "before", block ;
    def parse_before_statement(self):
        if self.token.token_type != Type.BEFORE:
            return None
        self.consume_token()
        block = self.parse_block()
        return BeforeStatement(block)

    # after_statement = "after", block ;
    def parse_after_statement(self):
        if self.token.token_type != Type.AFTER:
            return None
        self.consume_token()
        block = self.parse_block()
        return AfterStatement(block)
