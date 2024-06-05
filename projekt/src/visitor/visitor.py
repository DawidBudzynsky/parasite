import builtins
from parser.function import FunctionDef
from parser.statements.after_statement import AfterStatement
from parser.statements.aspect_block_statement import AspectBlock
from parser.statements.aspect_statement import Aspect
from parser.statements.assign_statement import AssignStatement
from parser.statements.before_statement import BeforeStatement
from parser.statements.block import Block
from parser.statements.for_each_statement import ForEachStatement
from parser.statements.fun_call_statement import FunCallStatement
from parser.statements.if_statement import IfStatement
from parser.statements.loop_statement import LoopStatement
from parser.statements.return_statement import ReturnStatement
from parser.type_annotations import TypeAnnotation
from parser.values.and_expression import AndExpression
from parser.values.bool import Bool
from parser.values.casting_expression import CastingExpression
from parser.values.divide_expression import DivideExpression
from parser.values.equals_expression import EqualsExpression
from parser.values.float import Float
from parser.values.greater_equal_expression import GreaterEqualExpression
from parser.values.greater_expression import GreaterExpression
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
from parser.values.is_expression import IsExpression
from parser.values.less_equal_expression import LessEqualExpresion
from parser.values.less_expression import LessExpresion
from parser.values.minus_expression import SubtractExpression
from parser.values.minus_negate_expression import MinusNegateExpression
from parser.values.multiply_expression import MultiplyExpression
from parser.values.negate_expression import NegateExpression
from parser.values.not_equals_expression import NotEqualsExpression
from parser.values.object_access_expression import ObjectAccessExpression
from parser.values.or_expression import OrExpression
from parser.values.plus_expression import AddExpresion
from parser.values.string import String
from parser.variable import Variable
from typing import Dict

from visitor.visitor_interface import Visitor
from visitor.callstack import CallStack
from visitor.embedded_fun import EmbeddedFunction
from visitor.scope import Scope, ScopeObject, ScopeVariable
from visitor.stack import Stack
from visitor.visitor_exceptions import (
    AspectBlockException,
    CastingException,
    ExprWrongType,
    FunctionNotDeclared,
    InvalidParameters,
    MismatchException,
    NoAttributeException,
    NotDeclared,
    NotIterableException,
    ObjectAccessException,
    RecursionException,
    Redefinition,
    ReturnMissingException,
    TypeMissmatch,
    WrongReturnType,
)


class CodeVisitor(Visitor):
    def __init__(self):
        self.functions = {"print": EmbeddedFunction(name="print", func=print)}
        self.aspects: Dict[str, Aspect] = {}
        self.scope_stack = Stack()
        self.curr_scope = Scope(parent=None, variables={})
        self.aspects_scope_map = {}
        self.curr_aspect_stack = Stack()
        self.fun_aspect_map = {}
        self.returning_flag = False
        self.curr_aspect_fun = {}
        self.last_result = []
        self.type_annotations = {
            TypeAnnotation.INT: "int",
            TypeAnnotation.FLOAT: "float",
            TypeAnnotation.STR: "str",
            TypeAnnotation.BOOL: "bool",
        }
        self.max_depth = 200
        self.call_stack = CallStack()

    def create_new_scope(self):
        new_scope = Scope(parent=self.curr_scope, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope

    def set_function_to_aspect_map(self, fun_aspect_map):
        self.fun_aspect_map = fun_aspect_map

    def set_functions(self, functions):
        for fun_name, fundef in functions.items():
            self.functions[fun_name] = fundef

    def set_aspects(self, aspects):
        self.aspects = aspects

    def visit_integer(self, element: Integer):
        self.last_result = element.value

    def visit_float(self, element: Float):
        self.last_result = element.value

    def visit_string(self, element: String):
        self.last_result = element.value

    def visit_bool(self, element: Bool):
        self.last_result = element.value

    def visit_identifier(self, element: Identifier):
        if (scope_variable := self.curr_scope.in_scope(element.name)) is None:
            raise NotDeclared(message=element.name, position=element.position)

        # interfejsy do scopeobject i scopevariable
        if isinstance(scope_variable, ScopeObject):
            self.last_result = scope_variable

        if isinstance(scope_variable, ScopeVariable):
            self.last_result = scope_variable.value

    def visit_variable(self, element: Variable):
        value = None
        if element.value is not None:
            element.value.accept(self)
            value = self.last_result

        self.put_variable(
            element.name,
            element.position,
            ScopeVariable(type=element.type, value=value),
        )

    def visit_minus_negate_expression(self, element: MinusNegateExpression):
        element.casting.accept(self)
        ex = self.last_result
        if not isinstance(ex, (int, float)):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        self.last_result = -1 * ex

    def visit_add_expr(self, element: AddExpresion):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result

        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            self.last_result = lex + rex
        # string concatenation
        elif isinstance(rex, str) and isinstance(lex, str):
            self.last_result = str(lex + rex)
        else:
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                position=element.position,
            )

    def visit_sub_expr(self, element: SubtractExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result
        if isinstance(lex, (int, float)) and isinstance(rex, (int, float)):
            self.last_result = lex - rex
        else:
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                position=element.position,
            )

    def visit_multiply_expr(self, element: MultiplyExpression) -> None:
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result
        if isinstance(lex, (int, float)) and isinstance(rex, (int, float)):
            self.last_result = lex * rex
        else:
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                position=element.position,
            )

    def visit_divide_expression(self, element: DivideExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result
        if isinstance(lex, (int, float)) and isinstance(rex, (int, float)):
            self.last_result = lex / rex
        else:
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                element.position,
            )

    def visit_negate_expression(self, element: NegateExpression):
        element.casting.accept(self)
        obj = self.last_result
        if not isinstance(obj, bool):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.BOOL)}",
                position=element.position,
            )
        self.last_result = not bool(obj)

    def visit_and_expression(self, element: AndExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.BOOL)}",
                position=element.position,
            )
        self.last_result = bool(lex) and bool(rex)

    def visit_or_expression(self, element: OrExpression):
        element.left_expression.accept(self)
        if (lex := self.last_result) is True:
            self.last_result = True
        element.right_expression.accept(self)
        rex = self.last_result
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.BOOL)}",
                position=element.position,
            )
        self.last_result = bool(lex) or bool(rex)

    def visit_equals_expr(self, element: EqualsExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result
        if type(lex) != type(rex):
            raise MismatchException(element.__class__.__name__, element.position)
        self.last_result = lex == rex

    def visit_not_equals_expr(self, element: NotEqualsExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result
        if type(lex) != type(rex):
            raise MismatchException(element.__class__.__name__, element.position)
        self.last_result = lex != rex

    def visit_greater_equal_expr(self, element: GreaterEqualExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        self.last_result = lex >= rex

    def visit_greater_expr(self, element: GreaterExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        self.last_result = lex > rex

    def visit_less_equal_expr(self, element: LessEqualExpresion):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        self.last_result = lex <= rex

    def visit_less_expr(self, element: LessExpresion):
        element.left_expression.accept(self)
        lex = self.last_result
        element.right_expression.accept(self)
        rex = self.last_result

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                element.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        self.last_result = lex < rex

    def visit_assign_statement(self, element: AssignStatement):
        name = element.identifier.name
        element.expression.accept(self)
        value = self.last_result
        self.set_value(name, element.position, value)

    def visit_return_statement(self, element: ReturnStatement):
        if (expression := element.expression) is None:
            self.last_result = None
        else:
            expression.accept(self)
        value = self.last_result

        self.returning_flag = True
        self.last_result = value

    def visit_fun_call_statement(self, element: FunCallStatement):
        if (fundef := self.functions.get(element.name)) is None:
            raise FunctionNotDeclared(element.name, element.position)

        if self.call_stack.recursion_count(element.name) >= self.max_depth:
            raise RecursionException(position=element.position)

        values = []
        for argument in element.arguments:
            argument.accept(self)
            values.append((self.last_result, argument.position))
        self.last_result = values

        fundef.accept(self)
        result = self.last_result

        self.last_result = result

    def visit_function_declaration(self, element: FunctionDef):
        if len(element.parameters) != len(self.last_result):
            raise InvalidParameters(
                len(self.last_result), len(element.parameters), element.position
            )

        values = self.last_result.copy()

        self.create_new_scope()

        aspects_list = self.fun_aspect_map.get(element.identifier)
        arguments = []
        for value_pos, param in zip(values, element.parameters):
            value, pos = value_pos
            self.check_value_type(type=param.type, value=value, position=pos)
            self.put_variable(
                param.name, param.position, ScopeVariable(value=value, type=param.type)
            )
            if aspects_list:
                arguments.append(
                    ScopeObject(
                        name=param.name, value=value, type=param.type, args=None
                    )
                )
        if aspects_list:
            self.curr_aspect_fun = ScopeObject(
                name=element.identifier, type=element.type, args=arguments, value=None
            )

        if aspects_list:
            self.scope_stack.push(self.curr_scope)
            for aspect in aspects_list:
                aspect.accept(self)
                if aspect.aspect_block.before_statement is not None:
                    aspect.aspect_block.before_statement.accept(self)
            self.curr_scope = self.scope_stack.pop()

        element.block.accept(self)
        if element.type and not self.returning_flag:
            raise ReturnMissingException(
                message=self.type_annotations.get(element.type),
                position=element.position,
            )
        result = self.last_result
        self.curr_scope = self.scope_stack.pop()

        if aspects_list:
            self.scope_stack.push(self.curr_scope)
            for aspect in aspects_list:
                if aspect.aspect_block.after_statement is not None:
                    self.last_result = result
                    aspect.aspect_block.after_statement.accept(self)
            self.curr_scope = self.scope_stack.pop()

        if self.returning_flag:
            self.returning_flag = False

        self.check_return_type_fun(result, element.type, element.position)
        self.last_result = result

    def check_return_type_fun(self, value, return_type, position):
        match return_type:
            case TypeAnnotation.INT:
                if isinstance(value, bool):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.INT),
                        position=position,
                    )

                if not isinstance(value, int):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.INT),
                        position=position,
                    )
                return
            case TypeAnnotation.FLOAT:
                if not isinstance(value, float):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.FLOAT),
                        position=position,
                    )
                return
            case TypeAnnotation.STR:
                if not isinstance(value, str):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.STR),
                        position=position,
                    )
                return
            case TypeAnnotation.BOOL:
                if not isinstance(value, bool):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.BOOL),
                        position=position,
                    )
                return

    def visit_embedded_function(self, element: EmbeddedFunction):
        for arg in self.last_result:
            value, _ = arg
            element.func(value)

    def visit_block(self, element: Block):
        for statement in element.statements:
            statement.accept(self)
            if self.returning_flag:
                break

    def visit_if_statement(self, element: IfStatement):
        self.create_new_scope()

        executed = False
        for condition_instruction in element.conditions_instructions:
            condition, instruction = condition_instruction
            condition.accept(self)
            if self.last_result:
                instruction.accept(self)
                executed = True
                break

        if not executed and element.else_instructions is not None:
            element.else_instructions.accept(self)

        self.curr_scope = self.scope_stack.pop()

    def visit_loop_statement(self, element: LoopStatement):
        self.create_new_scope()

        element.expression.accept(self)
        while self.last_result:
            element.block.accept(self)
            if self.returning_flag:
                break
            element.expression.accept(self)

        self.curr_scope = self.scope_stack.pop()

    def visit_for_each_statement(self, element: ForEachStatement):
        self.create_new_scope()

        element.expression.accept(self)
        arg_list = self.last_result
        if not isinstance(arg_list, list):
            raise NotIterableException(element.position)
        for arg in arg_list:
            self.curr_scope.variables[element.identifier.name] = arg
            element.block.accept(self)
            if self.returning_flag:
                break

        self.curr_scope = self.scope_stack.pop()

    def visit_access_expr(self, element: ObjectAccessExpression):
        element.left_expression.accept(self)
        base_object = self.last_result
        if not isinstance(base_object, ScopeObject):
            raise ObjectAccessException(element.left_expression.name)
        if not isinstance(element.right_expression, Identifier):
            raise ObjectAccessException(element.right_expression.name)

        attribute_name = element.right_expression.name
        if not hasattr(base_object, attribute_name):
            raise NoAttributeException(base_object.name, attribute_name)
        attribute = getattr(base_object, attribute_name)
        self.last_result = attribute

    def visit_cast_expr(self, element: CastingExpression):
        element.term.accept(self)
        value = self.last_result
        match element.type:
            case TypeAnnotation.INT:
                self.last_result = self.try_cast_to(value, int, element.position)
            case TypeAnnotation.FLOAT:
                self.last_result = self.try_cast_to(value, float, element.position)
            case TypeAnnotation.STR:
                self.last_result = self.try_cast_to(value, str, element.position)
            case TypeAnnotation.BOOL:
                self.last_result = self.try_cast_to(value, bool, element.position)

    # TODO: try i rzucać wyjątki
    def try_cast_to(self, value, cast_type, position):
        match type(value):
            case builtins.int:
                return cast_type(value)
            case builtins.float:
                return cast_type(value)
            case builtins.str:
                if cast_type == int:
                    raise CastingException(
                        value, self.type_annotations.get(TypeAnnotation.INT), position
                    )
                if cast_type == float:
                    raise CastingException(
                        value, self.type_annotations.get(TypeAnnotation.FLOAT), position
                    )
                return cast_type(value)
            case builtins.bool:
                return cast_type(value)
            case _:
                return None

    def visit_aspect_block(self, element: AspectBlock):
        for variable_declaration in element.variables:
            if not isinstance(variable_declaration, Variable):
                raise AspectBlockException()
            variable_declaration.accept(self)

    def visit_aspect_statement(self, element: Aspect):
        if (stack := self.aspects_scope_map.get(element.identifier)) is None:
            stack = Stack()
            stack.push(Scope(parent=None, variables={}))
            self.aspects_scope_map[element.identifier] = stack

        self.curr_aspect_stack = self.aspects_scope_map.get(element.identifier)
        self.curr_scope = self.curr_aspect_stack.peek()
        self.curr_scope.variables["function"] = self.curr_aspect_fun
        if len(self.curr_scope.variables) == 1:
            element.aspect_block.accept(self)

    def visit_before_statement(self, element: BeforeStatement):
        new_aspect_scope = Scope(parent=self.curr_scope, variables={})
        self.curr_scope = new_aspect_scope
        element.block.accept(self)
        self.curr_scope = self.curr_aspect_stack.peek()

    def visit_after_statement(self, element: AfterStatement):
        self.curr_scope = self.curr_aspect_stack.peek()
        self.curr_scope.variables["function"].result = self.last_result
        new_aspect_scope = Scope(parent=self.curr_scope, variables={})
        self.curr_scope = new_aspect_scope
        element.block.accept(self)
        self.curr_scope = self.curr_aspect_stack.peek()

    def visit_is_expr(self, element: IsExpression):
        element.left_expression.accept(self)
        lex = self.last_result
        if not isinstance(lex, TypeAnnotation):
            raise ValueError(
                f"Error: Left expression of {element.__class__.__name__} should be a type"
            )
        type = element.right_expression
        if not isinstance(lex, TypeAnnotation):
            raise ValueError(
                f"Error: Right expression of {element.__class__.__name__} should be a type"
            )
        self.last_result = lex == type

    def check_return_type(self, value, position):
        scope_pointer = self.curr_scope
        while scope_pointer.return_type is None:
            scope_pointer = scope_pointer.parent
        return_type = scope_pointer.return_type
        match return_type:
            case TypeAnnotation.INT:
                if isinstance(value, bool):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.INT),
                        position=position,
                    )

                if not isinstance(value, int):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.INT),
                        position=position,
                    )
                return
            case TypeAnnotation.FLOAT:
                if not isinstance(value, float):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.FLOAT),
                        position=position,
                    )
                return
            case TypeAnnotation.STR:
                if not isinstance(value, str):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.STR),
                        position=position,
                    )
                return
            case TypeAnnotation.BOOL:
                if not isinstance(value, bool):
                    raise WrongReturnType(
                        given_value=type(value).__name__,
                        expected_value=self.type_annotations.get(TypeAnnotation.BOOL),
                        position=position,
                    )
                return

    def check_value_type(self, type, value, position):
        match type:
            case TypeAnnotation.INT:
                if isinstance(value, bool) or not isinstance(value, int):
                    raise TypeMissmatch(
                        self.type_annotations.get(TypeAnnotation.INT), position
                    )
                return value
            case TypeAnnotation.FLOAT:
                if not isinstance(value, float):
                    raise TypeMissmatch(
                        self.type_annotations.get(TypeAnnotation.FLOAT), position
                    )
                return value
            case TypeAnnotation.BOOL:
                if not isinstance(value, bool):
                    raise TypeMissmatch(
                        self.type_annotations.get(TypeAnnotation.BOOL), position
                    )
                return value
            case TypeAnnotation.STR:
                if not isinstance(value, str):
                    raise TypeMissmatch(
                        self.type_annotations.get(TypeAnnotation.STR), position
                    )
                return value
            case _:
                return None

    def put_variable(self, v_name, position, scope_variable):
        if self.curr_scope.in_current_scope(v_name):
            raise Redefinition(v_name, position)
        self.check_value_type(scope_variable.type, scope_variable.value, position)
        self.curr_scope.variables[v_name] = scope_variable

    def set_value(self, v_name, position, value):
        if (variable := self.curr_scope.in_scope(v_name)) is None:
            raise NotDeclared(v_name, position)
        new_value = self.check_value_type(variable.type, value, position)
        variable.value = new_value
