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

from visitor.callstack import CallStack
from visitor.embedded_fun import EmbeddedFunction
from visitor.scope import Scope, ScopeObject, ScopeVariable
from visitor.stack import Stack
from visitor.visitor_exceptions import (
    AspectBlockException,
    ExprWrongType,
    FunctionNotDeclared,
    InvalidParameters,
    NoAttributeException,
    NotDeclared,
    ObjectAccessException,
    Redefinition,
    TypeMissmatch,
    WrongReturnType,
)


class ParserVisitor:
    def __init__(self):
        self.functions = {"print": EmbeddedFunction(name="print", func=print)}
        self.aspects: Dict[str, Aspect] = {}
        self.scope_stack = Stack()
        self.curr_scope = Scope(parent=None, return_type=None, variables={})
        self.aspects_scope_map = {}
        self.curr_aspect_stack = None
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

    def set_function_to_aspect_map(self, fun_aspect_map):
        self.fun_aspect_map = fun_aspect_map

    def set_functions(self, functions):
        for fun_name, fundef in functions.items():
            self.functions[fun_name] = fundef

    def set_aspects(self, aspects):
        self.aspects = aspects

    def visit_integer(self, integer: Integer):
        return integer.value

    def visit_float(self, float: Float):
        return float.value

    def visit_string(self, string: String):
        return string.value

    def visit_bool(self, bool: Bool):
        return bool.value

    def visit_identifier(self, identifier: Identifier):
        if (scope_variable := self.curr_scope.in_scope(identifier.name)) is None:
            raise NotDeclared(message=identifier.name, position=identifier.position)
        if isinstance(scope_variable, ScopeObject):
            return scope_variable
        return scope_variable.value

    def visit_variable(self, variable: Variable):
        value = None
        if variable.value is not None:
            value = variable.value.accept(self)
        self.put_variable(
            variable.name,
            variable.position,
            ScopeVariable(type=variable.type, value=value),
        )

    def visit_minus_negate_expression(self, minus_operator: MinusNegateExpression):
        ex = minus_operator.casting.accept(self)
        if not isinstance(ex, (int, float)):
            raise ExprWrongType(
                minus_operator.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        return -1 * ex

    def visit_add_expr(self, sum: AddExpresion):
        lex = sum.left_expression.accept(self)
        rex = sum.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return lex + rex
        # string concatenation
        if isinstance(rex, str) and isinstance(lex, str):
            return str(lex + rex)
        else:
            raise ExprWrongType(
                sum.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                position=sum.position,
            )

    def visit_sub_expr(self, sub: SubtractExpression):
        rex = sub.left_expression.accept(self)
        lex = sub.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex - lex
        else:
            raise ExprWrongType(
                sub.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                position=sub.position,
            )

    def visit_multiply_expr(self, mul: MultiplyExpression):
        rex = mul.left_expression.accept(self)
        lex = mul.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex * lex
        else:
            raise ExprWrongType(
                mul.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                position=mul.position,
            )

    def visit_divide_expression(self, div: DivideExpression):
        rex = div.left_expression.accept(self)
        lex = div.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex / lex
        else:
            raise ExprWrongType(
                div.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
                div.position,
            )

    def visit_negate_expression(self, not_operator: NegateExpression):
        obj = not_operator.casting.accept(self)
        if not isinstance(obj, bool):
            raise ExprWrongType(
                not_operator.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.BOOL)}",
                position=not_operator.position,
            )
        return not bool(obj)

    def visit_and_expression(self, and_expr: AndExpression):
        lex = and_expr.left_expression.accept(self)
        rex = and_expr.right_expression.accept(self)
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ExprWrongType(
                and_expr.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.BOOL)}",
                position=and_expr.position,
            )
        return bool(lex) and bool(rex)

    def visit_or_expression(self, or_expr: OrExpression):
        lex = or_expr.left_expression.accept(self)
        rex = or_expr.right_expression.accept(self)
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ExprWrongType(
                or_expr.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.BOOL)}",
                position=or_expr.position,
            )
        return bool(lex) or bool(rex)

    def visit_equals_expr(self, equals: EqualsExpression):
        lex = equals.left_expression.accept(self)
        rex = equals.right_expression.accept(self)
        return lex == rex

    def visit_not_equals_expr(self, not_equals: NotEqualsExpression):
        lex = not_equals.left_expression.accept(self)
        rex = not_equals.right_expression.accept(self)
        return lex != rex

    def visit_greater_equal_expr(self, greater_equal: GreaterEqualExpression):
        lex = greater_equal.left_expression.accept(self)
        rex = greater_equal.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                greater_equal.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        return lex >= rex

    def visit_greater_expr(self, greater: GreaterExpression):
        lex = greater.left_expression.accept(self)
        rex = greater.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                greater.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        return lex > rex

    def visit_less_equal_expr(self, less_equal: LessEqualExpresion):
        lex = less_equal.left_expression.accept(self)
        rex = less_equal.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                less_equal.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        return lex <= rex

    def visit_less_expr(self, less: LessExpresion):
        lex = less.left_expression.accept(self)
        rex = less.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ExprWrongType(
                less.__class__.__name__,
                f"{self.type_annotations.get(TypeAnnotation.INT)}, {self.type_annotations.get(TypeAnnotation.FLOAT)}",
            )
        return lex < rex

    def visit_assign_statement(self, assign: AssignStatement):
        name = assign.identifier.name
        value = assign.expression.accept(self)
        self.set_value(name, assign.position, value)

    def visit_return_statement(self, rs: ReturnStatement):
        # expression can be None
        if (expression := rs.expression) is None:
            return None
        value = expression.accept(self)

        # NOTE: position for now
        position = None
        if hasattr(expression, "position"):
            position = expression.position

        # NOTE: może tutaj powininem sprawdzać errory
        self.check_return_type(value, position)
        self.returning_flag = True
        return value

    def visit_fun_call_statement(self, fun: FunCallStatement):
        if (fundef := self.functions.get(fun.name)) is None:
            raise FunctionNotDeclared(fun.name, fun.position)

        if self.call_stack.recursion_count(fun.name) > self.max_depth:
            raise ValueError("recursion depth error")

        values = []
        for argument in fun.arguments:
            values.append((argument.accept(self), argument.position))
        self.last_result = values  # NOTE: i guess i can do that differently

        self.call_stack.push(fun.name)
        result = fundef.accept(self)
        self.call_stack.pop(fun.name)

        return result

    def visit_function_declaration(self, fundef: FunctionDef):
        if len(fundef.parameters) != len(self.last_result):
            raise InvalidParameters(
                len(self.last_result), len(fundef.parameters), fundef.position
            )

        if (aspects_list := self.fun_aspect_map.get(fundef.identifier)) is not None:
            return self.run_function_with_aspect(aspects_list, fundef)

        values = self.last_result.copy()
        new_scope = Scope(parent=self.curr_scope, return_type=fundef.type, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope
        for value_pos, param in zip(values, fundef.parameters):
            value, pos = value_pos
            self.check_value_type(type=param.type, value=value, position=pos)
            self.put_variable(
                param.name, param.position, ScopeVariable(value=value, type=param.type)
            )
        result = fundef.block.accept(self)
        self.last_result = result
        self.curr_scope = self.scope_stack.pop()

        if self.returning_flag:
            self.returning_flag = False
        return result

    def visit_embedded_function(self, e_func: EmbeddedFunction):
        for arg in self.last_result:
            value, _ = arg
            e_func.func(value)

    def run_function_with_aspect(self, aspects_list, fundef):
        values = self.last_result.copy()
        # prepare args for aspect
        arguments = []
        for value_pos, param in zip(values, fundef.parameters):
            value, pos = value_pos
            self.check_value_type(type=param.type, value=value, position=pos)
            arguments.append(
                ScopeObject(name=param.name, value=value, type=param.type, args=None)
            )

        # setting curr_aspect_fun to know which function we are currently aspecting
        self.curr_aspect_fun = ScopeObject(
            name=fundef.identifier, type=fundef.type, args=arguments, value=None
        )

        self.scope_stack.push(self.curr_scope)
        for aspect_name in aspects_list:
            aspect = self.aspects.get(aspect_name)
            aspect.accept(self)
            if aspect.aspect_block.before_statement is not None:
                aspect.aspect_block.before_statement.accept(self)
        self.curr_scope = self.scope_stack.pop()

        new_scope = Scope(parent=self.curr_scope, return_type=fundef.type, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope
        for value_pos, param in zip(values, fundef.parameters):
            value, pos = value_pos
            self.check_value_type(type=param.type, value=value, position=pos)
            self.put_variable(
                param.name, param.position, ScopeVariable(value=value, type=param.type)
            )
        result = fundef.block.accept(self)
        self.last_result = result
        self.curr_scope = self.scope_stack.pop()
        if self.returning_flag:
            self.returning_flag = False

        self.scope_stack.push(self.curr_scope)
        for aspect_name in aspects_list:
            aspect = self.aspects.get(aspect_name)
            if aspect.aspect_block.after_statement is not None:
                self.last_result = result
                aspect.aspect_block.after_statement.accept(self)
        self.curr_scope = self.scope_stack.pop()

        return result

    def visit_block(self, block: Block):
        for statement in block.statements:
            result = statement.accept(self)
            if self.returning_flag:
                return result

    def visit_if_statement(self, if_s: IfStatement):
        new_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope

        for condition_instruction in if_s.conditions_instructions:
            condition, instruction = condition_instruction
            if condition.accept(self):
                result = instruction.accept(self)
                self.curr_scope = self.scope_stack.pop()
                return result

        if if_s.else_instructions is not None:
            result = if_s.else_instructions.accept(self)
            self.curr_scope = self.scope_stack.pop()
            return result

        self.curr_scope = self.scope_stack.pop()
        return None

    def visit_loop_statement(self, loop: LoopStatement):
        new_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope
        while loop.expression.accept(self):
            if (result := self.visit_block(loop.block)) is not None:
                self.curr_scope = self.scope_stack.pop()
                return result
        self.curr_scope = self.scope_stack.pop()
        return None

    def visit_for_each_statement(self, for_s: ForEachStatement):
        new_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope

        # initialize "arg" in scope
        self.put_variable(
            v_name=for_s.identifier.name, position=None, scope_variable=None
        )
        arg_list = for_s.expression.accept(self)  # visiting object_access
        for arg in arg_list:
            # set currently iterating arg
            # NOTE: arg must be ScopeObject thats for sure
            self.curr_scope.variables[for_s.identifier.name] = arg
            if (result := for_s.block.accept(self)) is not None:
                self.curr_scope = self.scope_stack.pop()
                return result
        self.curr_scope = self.scope_stack.pop()
        return None

    def visit_access_expr(self, obj: ObjectAccessExpression):
        base_object = obj.left_expression.accept(self)
        if not isinstance(base_object, ScopeObject):
            raise ObjectAccessException(obj.left_expression.name)
        if not isinstance(obj.right_expression, Identifier):
            raise ObjectAccessException(obj.right_expression.name)

        attribute_name = obj.right_expression.name
        if not hasattr(base_object, attribute_name):
            raise NoAttributeException(base_object.name, attribute_name)
        attribute = getattr(base_object, attribute_name)
        return attribute

    def visit_cast_expr(self, cast_expr: CastingExpression):
        value = cast_expr.term.accept(self)
        match cast_expr.type:
            case TypeAnnotation.INT:
                return self.try_cast_to(value, int)
            case TypeAnnotation.FLOAT:
                return self.try_cast_to(value, float)
            case TypeAnnotation.STR:
                return self.try_cast_to(value, str)
            case TypeAnnotation.BOOL:
                return self.try_cast_to(value, bool)

    def try_cast_to(self, value, cast_type):
        match type(value):
            case builtins.int:
                return cast_type(value)
            case builtins.float:
                return cast_type(value)
            case builtins.str:
                return cast_type(value)
            case builtins.bool:
                return cast_type(value)
            case _:
                return None

    def visit_aspect_block(self, block: AspectBlock):
        for variable_declaration in block.variables:
            if not isinstance(variable_declaration, Variable):
                raise AspectBlockException()
            variable_declaration.accept(self)

    def visit_aspect_statement(self, aspect: Aspect):
        if (stack := self.aspects_scope_map.get(aspect.identifier)) is None:
            stack = Stack()
            stack.push(Scope(parent=None, return_type=None, variables={}))
            self.aspects_scope_map[aspect.identifier] = stack

        self.curr_aspect_stack = self.aspects_scope_map.get(aspect.identifier)
        self.curr_scope = self.curr_aspect_stack.peek()
        self.curr_scope.variables["function"] = self.curr_aspect_fun
        if len(self.curr_scope.variables) == 1:
            aspect.aspect_block.accept(self)

    def visit_before_statement(self, before: BeforeStatement):
        new_aspect_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.curr_scope = new_aspect_scope
        before.block.accept(self)
        self.curr_scope = self.curr_aspect_stack.peek()

    def visit_after_statement(self, after: AfterStatement):
        self.curr_scope = self.curr_aspect_stack.peek()
        self.curr_scope.variables["function"].result = self.last_result
        new_aspect_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.curr_scope = new_aspect_scope
        after.block.accept(self)
        self.curr_scope = self.curr_aspect_stack.peek()

    def visit_is_expr(self, is_expr: IsExpression):
        lex = is_expr.left_expression.accept(self)
        if not isinstance(lex, TypeAnnotation):
            raise ValueError(
                f"Error: Left expression of {is_expr.__class__.__name__} should be a type"
            )
        type = is_expr.right_expression
        if not isinstance(lex, TypeAnnotation):
            raise ValueError(
                f"Error: Right expression of {is_expr.__class__.__name__} should be a type"
            )
        return lex == type

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

    # TODO: lepsze errory tutaj i pozycja
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
                return None  # NOTE: should be some kind of error

    def put_variable(self, v_name, position, scope_variable):
        if self.curr_scope.in_current_scope(v_name):
            raise Redefinition(v_name, position)
        if scope_variable is not None:
            self.check_value_type(scope_variable.type, scope_variable.value, position)
        self.curr_scope.variables[v_name] = scope_variable

    def set_value(self, v_name, position, value):
        if (variable := self.curr_scope.in_scope(v_name)) is None:
            raise NotDeclared(v_name, position)
        new_value = self.check_value_type(variable.type, value, position)
        variable.value = new_value
