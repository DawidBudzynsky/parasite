from types import new_class
from typing import Dict
from typing_extensions import ValuesView

from _pytest.python import FunctionDefinition
from pytest import Function
from projekt.src.parser.function import FunctionDef
from projekt.src.parser.statements.after_statement import AfterStatement
from projekt.src.parser.statements.aspect_block_statement import AspectBlock
from projekt.src.parser.statements.aspect_statement import Aspect
from projekt.src.parser.statements.assign_statement import AssignStatement
from projekt.src.parser.statements.before_statement import BeforeStatement
from projekt.src.parser.statements.block import Block
from projekt.src.parser.statements.for_each_statement import ForEachStatement
from projekt.src.parser.statements.fun_call_statement import FunCallStatement
from projekt.src.parser.statements.loop_statement import LoopStatement
from projekt.src.parser.statements.return_statement import ReturnStatement
from projekt.src.parser.type_annotations import TypeAnnotation
from projekt.src.parser.values.and_expression import AndExpression
from projekt.src.parser.values.bool import Bool
from projekt.src.parser.values.divide_expression import DivideExpression
from projekt.src.parser.values.equals_expression import EqualsExpression
from projekt.src.parser.values.float import Float
from projekt.src.parser.values.greater_equal_expression import GreaterEqualExpression
from projekt.src.parser.values.greater_expression import GreaterExpression
from projekt.src.parser.values.identifier_expression import Identifier
from projekt.src.parser.values.integer import Integer
from projekt.src.parser.values.less_equal_expression import LessEqualExpresion
from projekt.src.parser.values.less_expression import LessExpresion
from projekt.src.parser.values.minus_expression import SubtractExpression
from projekt.src.parser.values.minus_negate_expression import MinusNegateExpression
from projekt.src.parser.values.multiply_expression import MultiplyExpression
from projekt.src.parser.values.negate_expression import NegateExpression
from projekt.src.parser.values.not_equals_expression import NotEqualsExpression
from projekt.src.parser.values.object_access_expression import ObjectAccessExpression
from projekt.src.parser.values.or_expression import OrExpression
from projekt.src.parser.values.plus_expression import AddExpresion
from projekt.src.parser.values.string import String
from projekt.src.parser.variable import Variable
from projekt.src.visitor.scope import Scope, ScopeVariable
from projekt.src.visitor.stack import Stack


class ParserVisitor:
    def __init__(self):
        self.functions: Dict[str, FunctionDef] = {}
        self.aspects: Dict[str, Aspect] = {}

        self.scope_stack = Stack()
        self.curr_scope = Scope(parent=None, return_type=None, variables={})

        self.aspects_scope_map = {}
        self.curr_aspect_stack = None

        self.fun_aspect_map = {}

        self.returning_flag = False
        self.curr_aspect_fun = None

        self.last_result = None

    def set_function_to_aspect_map(self, fun_aspect_map):
        self.fun_aspect_map = fun_aspect_map

    def set_functions(self, functions):
        self.functions = functions

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
        return self.curr_scope.in_scope(identifier.name).value

    def visit_variable(self, variable: Variable):
        value = None
        if variable.value is not None:
            value = variable.value.accept(self)
        self.curr_scope.put_variable(
            variable.name,
            ScopeVariable(type=variable.type, value=value),
        )

    def visit_minus_negate_expression(self, minus_operator: MinusNegateExpression):
        ex = minus_operator.casting.accept(self)
        if not isinstance(ex, (int, float)):
            raise ValueError
        return -1 * ex

    def visit_add_expr(self, sum: AddExpresion):
        rex = sum.left_expression.accept(self)
        lex = sum.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex + lex
        # string concatenation
        if isinstance(rex, str) and isinstance(lex, str):
            return str(rex + lex)
        else:
            raise ValueError

    def visit_sub_expr(self, sub: SubtractExpression):
        rex = sub.left_expression.accept(self)
        lex = sub.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex - lex
        else:
            raise ValueError

    def visit_multiply_expr(self, mul: MultiplyExpression):
        rex = mul.left_expression.accept(self)
        lex = mul.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex * lex
        else:
            raise ValueError

    def visit_divide_expression(self, div: DivideExpression):
        rex = div.left_expression.accept(self)
        lex = div.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex / lex
        else:
            raise ValueError

    def visit_negate_expression(self, not_operator: NegateExpression):
        obj = not_operator.casting.accept(self)
        if not isinstance(obj, bool):
            raise ValueError
        return not bool(obj)

    def visit_and_expression(self, and_expr: AndExpression):
        lex = and_expr.left_expression.accept(self)
        rex = and_expr.right_expression.accept(self)
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ValueError
        return bool(lex) and bool(rex)

    def visit_or_expression(self, or_expr: OrExpression):
        lex = or_expr.left_expression.accept(self)
        rex = or_expr.right_expression.accept(self)
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ValueError
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
            raise ValueError
        return lex >= rex

    def visit_greater_expr(self, greater: GreaterExpression):
        lex = greater.left_expression.accept(self)
        rex = greater.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ValueError
        return lex > rex

    def visit_less_equal_expr(self, less_equal: LessEqualExpresion):
        lex = less_equal.left_expression.accept(self)
        rex = less_equal.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ValueError
        return lex <= rex

    def visit_less_expr(self, less: LessExpresion):
        lex = less.left_expression.accept(self)
        rex = less.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ValueError
        return lex < rex

    def visit_assign_statement(self, assign: AssignStatement):
        name = assign.identifier.name
        value = assign.expression.accept(self)
        # TODO: inaczje, to wprowadza w błąd jakbyśmy ustawiali wartość w tym SCOPE a nie zawsze tak jest
        self.curr_scope.set_value(name, value)

    def visit_return_statement(self, rs: ReturnStatement):
        expression = rs.expression
        if expression is None:
            return None
        value = expression.accept(self)
        # NOTE: może tutaj powininem sprawdzać errory
        self.curr_scope.check_return_type(value)
        self.returning_flag = True
        return value

    def visit_function_declaration(self, fundef: FunctionDef):
        new_scope = Scope(parent=self.curr_scope, return_type=fundef.type)
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope
        # check if given parameter has right type defined in fundef
        # if len(self.last_result) == 0:
        #     raise ValueError
        for value, param in zip(self.last_result, fundef.parameters):
            new_scope.check_value_type(type=param.type, value=value)
            self.curr_scope.put_variable(
                param.name, ScopeVariable(value=value, type=param.type)
            )
        result = fundef.block.accept(self)
        self.curr_scope = self.scope_stack.pop()
        return result

    def visit_fun_call_statement(self, fun: FunCallStatement):
        if (fundef := self.functions.get(fun.name)) is None:
            raise ValueError("couldnt find function declaration")
        if len(fundef.parameters) != len(fun.arguments):
            raise ValueError("invalid number of parameters")

        values = []
        for argument in fun.arguments:
            values.append(argument.accept(self))
        self.last_result = values

        self.curr_aspect_fun = fun
        self.scope_stack.push(self.curr_scope)
        if (aspects_list := self.fun_aspect_map.get(fun.name)) is not None:
            for aspect_name in aspects_list:
                aspect = self.aspects.get(aspect_name)
                aspect.accept(self)
                if aspect.aspect_block.before_statement is not None:
                    aspect.aspect_block.before_statement.accept(self)

        self.curr_scope = self.scope_stack.pop()
        result = fundef.accept(self)

        self.scope_stack.push(self.curr_scope)
        if (aspects_list := self.fun_aspect_map.get(fun.name)) is not None:
            for aspect in aspects_list:
                aspect = self.aspects.get(aspect_name)
                if aspect.aspect_block.after_statement is not None:
                    aspect.aspect_block.after_statement.accept(self)

        return result

    def visit_block(self, block: Block):
        for statement in block.statements:
            if isinstance(statement, ReturnStatement):
                return statement.accept(self)
            statement.accept(self)  # TODO: return here???

    def visit_loop_statement(self, loop: LoopStatement):
        new_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope
        while loop.expression.accept(self):
            if (result := self.visit_block(loop.block)) is not None:
                # NOTE: consider if{ while {...}}
                self.curr_scope = self.scope_stack.pop()
                return result
        self.curr_scope = self.scope_stack.pop()
        return None

    def visit_for_each_statement(self, for_s: ForEachStatement):
        new_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope

        # initialize "arg" in scope
        self.curr_scope.put_variable(v_name="arg", scope_variable=None)
        arg_list = for_s.expression.accept()  # visiting object_access
        for arg in arg_list:
            # set currently iterating arg
            self.curr_scope.variables["arg"] = arg

            if (result := self.visit_block(for_s.block)) is not None:
                self.curr_scope = self.scope_stack.pop()
                return result
        self.curr_scope = self.scope_stack.pop()
        return None

    # NOTE: trochę zakładamy, że po kropce zawsze jest int
    def visit_access_expr(self, obj: ObjectAccessExpression):
        base_object = obj.left_expression.accept(self)
        if not isinstance(obj.right_expression, Identifier):
            raise ValueError
        attribute_name = obj.right_expression.name
        attribute = base_object.get(attribute_name)
        # NOTE: ensure that it gets the objects itself, not the value
        return attribute

    def visit_aspect_block(self, block: AspectBlock):
        for variable_declaration in block.variables:
            if not isinstance(variable_declaration, Variable):
                raise ValueError("only variable declarations available in aspect block")
            variable_declaration.accept(self)

    def visit_aspect_statement(self, aspect: Aspect):
        if (stack := self.aspects_scope_map.get(aspect.identifier)) is None:
            stack = Stack()
            stack.push(
                Scope(
                    parent=None,
                    return_type=None,
                    variables={
                        "function": ScopeVariable(
                            type=FunctionDef,
                            value={
                                "name": self.curr_aspect_fun.name,
                                "args": self.curr_aspect_fun.arguments,
                            },
                        )
                    },
                )
            )
            self.aspects_scope_map[aspect.identifier] = stack

        self.curr_aspect_stack = self.aspects_scope_map.get(aspect.identifier)
        self.curr_scope = self.curr_aspect_stack.peek()
        if len(self.curr_scope.variables) == 1:
            aspect.aspect_block.accept(self)

    def visit_before_statement(self, before: BeforeStatement):
        new_aspect_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.curr_scope = new_aspect_scope

        before.block.accept(self)

        self.curr_scope = self.curr_aspect_stack.peek()

    def visit_after_statement(self, after: AfterStatement):
        new_aspect_scope = Scope(parent=self.curr_scope, return_type=None, variables={})
        self.curr_scope = new_aspect_scope

        after.block.accept(self)

        self.curr_scope = self.curr_aspect_stack.peek()
