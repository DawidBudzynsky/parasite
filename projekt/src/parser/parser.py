from typing import List
from projekt.src.lexer.lexer import Lexer
from projekt.src.lexer.tokens import Token, Type
from projekt.src.parser.statements.after_statement import AfterStatement
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.statements.aspect_statement import Aspect
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.for_each_statement import ForEachStatement
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.statements.if_statement import IfStatement
from projekt.src.parser.statements.loop_statement import LoopStatement
from projekt.src.parser.statements.program import Program
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.bool import Bool
from projekt.src.parser.values.casting_expression import CastingExpression
from projekt.src.parser.values.divide_expression import DivideExpression
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.values.equals_expression import EqualsExpression
from projekt.src.parser.values.float import Float
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
    ASPECT_BLOCK_MISSING,
    ASPECT_BLOCK_NOT_CLOSED,
    ASPECT_DEF_NOT_CLOSED,
    ASPECT_DEF_PAREN_OPEN_MISSING,
    ASPECT_MISSING_NAME,
    ASSIGN_OR_CALL_MISSING,
    BLOCK_NOT_CLOSED,
    ETX_MISSING,
    EXPREESION_NOT_CLOSED,
    FOR_EACH_IDENTIFIER,
    FOR_EACH_IN_MISSING,
    FUN_CALL_NOT_CLOSED,
    FUN_DEF_PAREN_CLOSE_MISSING,
    FUN_DEF_PAREN_OPEN_MISSING,
    MISSING_IDENTIFIER_AFTER_COMMA,
    PARAMETER_COLON_MISSING,
    PARAMETER_IDENTIFIER,
    VAR_DECLARATION_COLON,
    VAR_DECLARATION_IDENTIFIER,
    AspectArgument,
    AspectBodyError,
    AspectRedefinition,
    FunctionRedefinition,
    InvalidSyntax,
    InvalidSyntaxVerbose,
    MissingExpression,
    MissingStatement,
    MissingTypeAnnotation,
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
            Type.WHILE: "while",
            Type.IN: "in",
            Type.COMMA: ",",
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
        self.true_values_map = {
            Type.INTEGER_TYPE: TypeAnnotation.INT,
            Type.FLOAT_TYPE: TypeAnnotation.FLOAT,
            Type.STRING_TYPE: TypeAnnotation.STR,
            Type.BOOL_TYPE: TypeAnnotation.BOOL,
        }
        self.types = [
            Type.INTEGER_TYPE,
            Type.FLOAT_TYPE,
            Type.STRING_TYPE,
            Type.BOOL_TYPE,
        ]

    def consume_token(self):
        self.token = self.lexer.build_next_token()

    def __add_to_dict(self, dictionary, key, value, exception):
        if key in dictionary:
            raise exception
        else:
            dictionary[key] = value

    def __must_be(self, *types, message):
        if self.token.token_type not in types:
            raise InvalidSyntax(
                message=message,
                position=self.token.position,
                expected_type=self.symbols_map.get(*types),
            )
        value = self.token.value
        self.consume_token()
        return value

    # program = { function_definition | aspect_definition } ;
    def parse_program(self):
        functions = {}
        aspects = {}
        while self.parse_fun_def(
            lambda fun_def: self.__add_to_dict(
                functions,
                fun_def.identifier,
                fun_def,
                exception=FunctionRedefinition(
                    function_name=fun_def.identifier, position=fun_def.position
                ),
            )
        ) or self.parse_aspect_definition(
            lambda aspect_def: self.__add_to_dict(
                aspects,
                aspect_def.identifier,
                aspect_def,
                exception=AspectRedefinition(
                    aspect_def.identifier, aspect_def.position
                ),
            )
        ):
            continue
        self.consume_token()
        self.__must_be(Type.ETX, message=ETX_MISSING)
        return Program(functions, aspects)

    # function_definition = identifier, "(", [ parameters ], ")", [ type ], block ;
    def parse_fun_def(self, handler):
        if self.token.token_type != Type.IDENTIFIER:
            return None

        # name = self.token.value
        position = self.token.position
        name = self.token.value
        self.consume_token()

        self.__must_be(
            Type.PAREN_OPEN,
            message=FUN_DEF_PAREN_OPEN_MISSING,
        )
        parameters = self.parse_parameters()
        self.__must_be(
            Type.PAREN_CLOSE,
            message=FUN_DEF_PAREN_CLOSE_MISSING,
        )

        type = self.parse_type_annotation()
        if (block := self.parse_block()) is None:
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )

        handler(FunctionDef(name, parameters, type, block, position))
        return True

    # parameters = identifier, ":", type, { ",", identifier, ":", type } ;
    def parse_parameters(self) -> List | None:
        parameters = []
        if (parameter := self.parse_parameter()) is None:
            return parameters
        parameters.append(parameter)
        while self.token.token_type == Type.COMMA:
            self.consume_token()
            if (parameter := self.parse_parameter()) is None:
                raise InvalidSyntaxVerbose(
                    message=MISSING_IDENTIFIER_AFTER_COMMA,
                    position=self.token.position,
                )
            parameters.append(parameter)
        return parameters

    # parameter = identifier, ":", type
    def parse_parameter(self):
        if self.token.token_type != Type.IDENTIFIER:
            return None

        position = self.token.position  # idk moze niepotrzebne
        identifier = self.__must_be(Type.IDENTIFIER, message=PARAMETER_IDENTIFIER)

        self.__must_be(Type.COLON, message=PARAMETER_COLON_MISSING)
        if (type := self.parse_type_annotation()) is None:
            raise MissingTypeAnnotation(self.token.position)

        return Variable(identifier, type, position=position)

    def parse_type_annotation(self):
        if (value := self.true_values_map.get(self.token.token_type)) is None:
            return None
        self.consume_token()
        return value

    # block = "{", {statement}, "}" ;
    def parse_block(self):
        if self.token.token_type != Type.BRACE_OPEN:
            return None
        self.consume_token()

        statements = []
        while (statement := self.parse_statement()) is not None:
            statements.append(statement)
        self.__must_be(Type.BRACE_CLOSE, message=BLOCK_NOT_CLOSED)
        return Block(statements)

    # statement = variable_declaration | if_statement | loop_statement | for_each_statement | assign_or_call | return_statement ;
    def parse_statement(self):
        return (
            self.parse_variable_declaration()
            or self.parse_if_statement()
            or self.parse_loop_statement()
            or self.parse_for_each_statement()
            or self.parse_assign_or_call()
            or self.parse_return_statement()
        )

    # variable_declaration = type, identifier, "=", expression ;
    def parse_variable_declaration(self):
        position = self.token.position
        if (type := self.parse_type_annotation()) is None:
            return None

        name = self.__must_be(Type.IDENTIFIER, message=VAR_DECLARATION_IDENTIFIER)
        self.__must_be(Type.ASSIGNMENT, message=VAR_DECLARATION_COLON)
        if (value := self.parse_expression()) is None:
            raise MissingExpression(
                operator=self.symbols_map.get(Type.ASSIGNMENT),
                position=self.token.position,
            )
        return Variable(name, type, value, position)

    # expression = conjunction, { "or", conjunction } ;
    def parse_expression(self):
        if (left_logic_factor := self.parse_conjunction()) is None:
            return None
        while self.token.token_type == Type.OR:
            self.consume_token()
            if (right_logic_factor := self.parse_conjunction()) is None:
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.OR),
                    position=self.token.position,
                )
            left_logic_factor = OrExpression(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # conjunction = relation_term, { "and", relation_term } ;
    def parse_conjunction(self):
        if (left_logic_factor := self.parse_relation()) is None:
            return None
        while self.token.token_type == Type.AND:
            self.consume_token()
            if (right_logic_factor := self.parse_relation()) is None:
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.AND),
                    position=self.token.position,
                )
            left_logic_factor = AndExpression(left_logic_factor, right_logic_factor)
        return left_logic_factor

    # relation_term = additive_term, [ relation_operator, additive_term ] ;
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
        if (casting := self.parse_casting()) is None:
            raise ValueError("fds")  # TODO: uzupelnij
        return constructor(casting, position)

    # casting = term, [ "->", type ] ;
    def parse_casting(self):
        if (term := self.parse_term()) is None:
            return None

        if self.token.token_type != Type.CAST:
            return term
        self.consume_token()
        if (type := self.parse_type_annotation()) is None:
            raise MissingTypeAnnotation(self.token.position)
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
            case Type.TRUE:
                self.consume_token()
                return Bool(True, position)
            case Type.FALSE:
                self.consume_token()
                return Bool(False, position)
            case Type.STRING:
                self.consume_token()
                return String(value, position)
            case Type.PAREN_OPEN:
                self.consume_token()
                if (expression := self.parse_expression()) is None:
                    raise MissingExpression(
                        operator=self.symbols_map.get(Type.PAREN_OPEN),
                        position=self.token.position,
                    )
                self.__must_be(Type.PAREN_CLOSE, message=EXPREESION_NOT_CLOSED)
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
        name = self.token.value
        self.consume_token()

        if self.token.token_type != Type.PAREN_OPEN:
            return Identifier(name, position)
        self.consume_token()
        arguments = self.parse_arguments()
        self.__must_be(Type.PAREN_CLOSE, message=FUN_CALL_NOT_CLOSED)
        return FunCallStatement(name, arguments, position)

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
        position = self.token.position
        self.consume_token()

        conditions_instructions = []
        if (expression := self.parse_expression()) is None:
            raise MissingExpression(
                operator=self.symbols_map.get(Type.IF), position=self.token.position
            )

        if (true_instructions := self.parse_block()) is None:
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )

        conditions_instructions.append((expression, true_instructions))

        while self.token.token_type == Type.ELIF:
            self.consume_token()
            if (expression := self.parse_expression()) is None:
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.ELIF),
                    position=self.token.position,
                )
            if (true_instructions := self.parse_block()) is None:
                raise MissingStatement(
                    missing_statement="block", position=self.token.position
                )
            conditions_instructions.append((expression, true_instructions))

        else_instructions = []
        if self.token.token_type == Type.ELSE:
            self.consume_token()
            if (else_instructions := self.parse_block()) is None:
                raise MissingStatement(
                    missing_statement="block", position=self.token.position
                )
        return IfStatement(
            conditions_instructions, else_instructions, position=position
        )

    # loop_statement = "while", expression, block ;
    def parse_loop_statement(self):
        if self.token.token_type != Type.WHILE:
            return None
        position = self.token.position
        self.consume_token()
        if (expression := self.parse_expression()) is None:
            raise MissingExpression(
                operator=self.symbols_map.get(Type.WHILE), position=self.token.position
            )
        if (block := self.parse_block()) is None:
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )
        return LoopStatement(expression, block, position=position)

    # for_each_statement = "for", idientifier, "in", expression, block ;
    def parse_for_each_statement(self):
        if self.token.token_type != Type.FOR_EACH:
            return None
        self.consume_token()

        identifier_pos = self.token.position
        identifier = self.__must_be(Type.IDENTIFIER, message=FOR_EACH_IDENTIFIER)
        self.__must_be(Type.IN, message=FOR_EACH_IN_MISSING)

        if (expression := self.parse_expression()) is None:
            raise MissingExpression(
                operator=self.symbols_map.get(Type.IN), position=self.token.position
            )
        if (block := self.parse_block()) is None:
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )
        return ForEachStatement(
            Identifier(identifier, identifier_pos), expression, block
        )

    # assign_or_call = identifier, ( "(", arguments, ")"  |  "=", expression ) ;
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
                self.__must_be(Type.PAREN_CLOSE, message=FUN_CALL_NOT_CLOSED)
                return FunCallStatement(identifier, arguments, position)
            case Type.ASSIGNMENT:
                self.consume_token()
                if (expression := self.parse_expression()) is None:
                    raise MissingExpression(
                        operator=self.symbols_map.get(Type.ASSIGNMENT),
                        position=self.token.position,
                    )
                return AssignStatement(
                    Identifier(identifier, position), expression, position=position
                )
            case _:
                raise InvalidSyntaxVerbose(
                    message=ASSIGN_OR_CALL_MISSING
                    % (
                        self.symbols_map.get(Type.PAREN_OPEN),
                        self.symbols_map.get(Type.ASSIGNMENT),
                    ),
                    position=self.token.position,
                )

    # return_statement = "return", [ expression ] ;
    def parse_return_statement(self):
        if self.token.token_type != Type.RETURN:
            return None
        self.consume_token()
        expression = self.parse_expression()
        return ReturnStatement(expression)

    def identifier_or_regex(self):
        if result := self.parse_identifier_or_call():
            return result
        if self.token.token_type == Type.STRING:
            return self.token.value
        return None

    # aspect_definition = "aspect", identifier, "(", (identifier | string) {"," (identifier | string), ")", aspect_block;
    def parse_aspect_definition(self, handler):
        if self.token.token_type != Type.ASPECT:
            return None
        self.consume_token()
        aspect_pos = self.token.position
        aspect_name = self.__must_be(Type.IDENTIFIER, message=ASPECT_MISSING_NAME)
        self.__must_be(Type.PAREN_OPEN, message=ASPECT_DEF_PAREN_OPEN_MISSING)

        aspect_args = []
        if (identifier_or_regex := self.identifier_or_regex()) is None:
            raise AspectArgument(position=self.token.position)
        aspect_args.append(identifier_or_regex)

        while self.token.token_type == Type.COMMA:
            self.consume_token()
            if (identifier_or_regex := self.identifier_or_regex()) is None:
                raise MissingExpression(
                    operator=self.symbols_map.get(Type.COMMA),
                    position=self.token.position,
                )
            aspect_args.append(identifier_or_regex)

        self.__must_be(Type.PAREN_CLOSE, message=ASPECT_DEF_NOT_CLOSED)
        aspect_block = self.parse_aspect_block()
        handler(Aspect(aspect_name, aspect_args, aspect_block, aspect_pos))
        return True

    # aspect_block = "{", { variable_declaration }, aspect_member "}" ;
    def parse_aspect_block(self):
        self.__must_be(Type.BRACE_OPEN, message=ASPECT_BLOCK_MISSING)
        variables = []
        while (variable := self.parse_variable_declaration()) is not None:
            variables.append(variable)
        if (aspect_members := self.parse_aspect_members()) is None:
            raise AspectBodyError(position=self.token.position)
        before_member, after_member = aspect_members
        self.__must_be(Type.BRACE_CLOSE, message=ASPECT_BLOCK_NOT_CLOSED)
        return AspectBlock(variables, before_member, after_member)

    # aspect_members = ( before_statement, [ after_statement ] ) |  after_statement) ;
    def parse_aspect_members(self):
        if before_statement := self.parse_before_statement():
            after_statement = self.parse_after_statement()
            return before_statement, after_statement

        if after_statement := self.parse_after_statement():
            before_statement = self.parse_before_statement()
            return before_statement, after_statement
        return None

    # before_statement = "before", block ;
    def parse_before_statement(self):
        if self.token.token_type != Type.BEFORE:
            return None
        self.consume_token()
        if (block := self.parse_block()) is None:
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )
        return BeforeStatement(block)

    # after_statement = "after", block ;
    def parse_after_statement(self):
        if self.token.token_type != Type.AFTER:
            return None
        self.consume_token()
        if (block := self.parse_block()) is None:
            raise MissingStatement(
                missing_statement="block", position=self.token.position
            )
        return AfterStatement(block)
