import builtins
from typing import Dict
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
from parser.values.divide_expression import DivideExpression
from parser.values.equals_expression import EqualsExpression
from parser.values.float import Float
from parser.values.greater_equal_expression import GreaterEqualExpression
from parser.values.greater_expression import GreaterExpression
from parser.values.identifier_expression import Identifier
from parser.values.integer import Integer
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
from parser.values.casting_expression import CastingExpression
from parser.values.is_expression import IsExpression
from visitor.scope import Scope, ScopeObject, ScopeVariable
from visitor.stack import Stack


class EmbeddedFunction:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def accept(self, visitator):
        return visitator.visit_embedded_function(self)


embedded_functinos = {"print": EmbeddedFunction(name="print", func=print)}


class ParserVisitor:
    def __init__(self):
        self.functions = embedded_functinos
        self.aspects: Dict[str, Aspect] = {}

        self.scope_stack = Stack()
        self.curr_scope = Scope(parent=None, return_type=None, variables={})

        self.aspects_scope_map = {}
        self.curr_aspect_stack = None

        self.fun_aspect_map = {}

        self.returning_flag = False
        self.curr_aspect_fun = {}

        self.last_result = []

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
            raise ValueError("coulnt find variable in scope")
        if isinstance(scope_variable, ScopeObject):
            return scope_variable
        return scope_variable.value

    def visit_variable(self, variable: Variable):
        value = None  # NOTE: god knows
        if variable.value is not None:
            value = variable.value.accept(self)
        self.curr_scope.put_variable(
            variable.name, ScopeVariable(type=variable.type, value=value)
        )

    def visit_minus_negate_expression(self, minus_operator: MinusNegateExpression):
        ex = minus_operator.casting.accept(self)
        if not isinstance(ex, (int, float)):
            raise ValueError
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
            raise ValueError(f"couldnt use add on {lex} + {rex}")

    def visit_sub_expr(self, sub: SubtractExpression):
        rex = sub.left_expression.accept(self)
        lex = sub.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex - lex
        else:
            raise ValueError(f"couldnt use sub on {lex} - {rex}")

    def visit_multiply_expr(self, mul: MultiplyExpression):
        rex = mul.left_expression.accept(self)
        lex = mul.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex * lex
        else:
            raise ValueError(f"couldnt use multiply on {lex} * {rex}")

    def visit_divide_expression(self, div: DivideExpression):
        rex = div.left_expression.accept(self)
        lex = div.right_expression.accept(self)
        if isinstance(rex, (int, float)) and isinstance(lex, (int, float)):
            return rex / lex
        else:
            raise ValueError(f"couldnt use divide on {lex} / {rex}")

    def visit_negate_expression(self, not_operator: NegateExpression):
        obj = not_operator.casting.accept(self)
        if not isinstance(obj, bool):
            raise ValueError(f"{obj} is not of type bool")
        return not bool(obj)

    def visit_and_expression(self, and_expr: AndExpression):
        lex = and_expr.left_expression.accept(self)
        rex = and_expr.right_expression.accept(self)
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ValueError(f"couldnt use and expression on {lex} and {rex}")
        return bool(lex) and bool(rex)

    def visit_or_expression(self, or_expr: OrExpression):
        lex = or_expr.left_expression.accept(self)
        rex = or_expr.right_expression.accept(self)
        if not isinstance(lex, bool) and not isinstance(rex, bool):
            raise ValueError(f"couldnt use or expression on {lex} or {rex}")
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
            raise ValueError(f"couldnt compare {lex} >= {rex}")
        return lex >= rex

    def visit_greater_expr(self, greater: GreaterExpression):
        lex = greater.left_expression.accept(self)
        rex = greater.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ValueError(f"couldnt compare {lex} > {rex}")
        return lex > rex

    def visit_less_equal_expr(self, less_equal: LessEqualExpresion):
        lex = less_equal.left_expression.accept(self)
        rex = less_equal.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ValueError(f"couldnt compare {lex} <= {rex}")
        return lex <= rex

    def visit_less_expr(self, less: LessExpresion):
        lex = less.left_expression.accept(self)
        rex = less.right_expression.accept(self)

        if not isinstance(lex, (int, float)) and not isinstance(rex, (int, float)):
            raise ValueError(f"couldnt compare {lex} < {rex}")
        return lex < rex

    def visit_assign_statement(self, assign: AssignStatement):
        name = assign.identifier.name
        value = assign.expression.accept(self)
        self.curr_scope.set_value(name, value)

    def visit_return_statement(self, rs: ReturnStatement):
        # expression can be None
        if (expression := rs.expression) is None:
            return None
        value = expression.accept(self)
        # NOTE: może tutaj powininem sprawdzać errory
        self.curr_scope.check_return_type(value)
        self.returning_flag = True
        return value

    def visit_embedded_function(self, e_func: EmbeddedFunction):
        for arg in self.last_result:
            e_func.func(arg)

    def visit_function_declaration(self, fundef: FunctionDef):
        if len(fundef.parameters) != len(self.last_result):
            raise ValueError("invalid number of parameters")

        if (aspects_list := self.fun_aspect_map.get(fundef.identifier)) is not None:
            return self.run_function_with_aspect(aspects_list, fundef)

        values = self.last_result.copy()
        new_scope = Scope(parent=self.curr_scope, return_type=fundef.type, variables={})
        self.scope_stack.push(self.curr_scope)
        self.curr_scope = new_scope
        for value, param in zip(values, fundef.parameters):
            self.curr_scope.check_value_type(type=param.type, value=value)
            self.curr_scope.put_variable(
                param.name, ScopeVariable(value=value, type=param.type)
            )
        result = fundef.block.accept(self)
        self.last_result = result
        self.curr_scope = self.scope_stack.pop()

        if self.returning_flag:
            self.returning_flag = False
        return result

    def visit_fun_call_statement(self, fun: FunCallStatement):
        if (fundef := self.functions.get(fun.name)) is None:
            raise ValueError(f"couldnt find function declaration {fun.name}")

        values = []
        for argument in fun.arguments:
            values.append(argument.accept(self))
        self.last_result = values  # NOTE: i guess i can do that differently

        result = fundef.accept(self)

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
        self.curr_scope.put_variable(v_name=for_s.identifier.name, scope_variable=None)
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

    # NOTE: trochę zakładamy, że po kropce zawsze jest identifier
    def visit_access_expr(self, obj: ObjectAccessExpression):
        # __import__("pdb").set_trace()
        base_object = obj.left_expression.accept(self)
        if not isinstance(base_object, ScopeObject):
            raise ValueError("wyciągnięto źle, to nie ScopeObject")

        if not isinstance(obj.right_expression, Identifier):
            raise ValueError
        attribute_name = obj.right_expression.name
        if not hasattr(base_object, attribute_name):
            raise ValueError(f"objekt nie ma atrybutu: {attribute_name}")
        attribute = getattr(base_object, attribute_name)
        # NOTE: ensure that it gets the objects itself, not the value
        return attribute

    def visit_cast_expr(self, cast_expr: CastingExpression):
        # __import__("pdb").set_trace()
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
                return cast_type(value)  # should raise some kind of error here
            case builtins.bool:
                return cast_type(value)  # will return 1
            case _:
                return None

    def visit_aspect_block(self, block: AspectBlock):
        for variable_declaration in block.variables:
            if not isinstance(variable_declaration, Variable):
                raise ValueError("only variable declarations available in aspect block")
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
        # __import__("pdb").set_trace()
        after.block.accept(self)
        self.curr_scope = self.curr_aspect_stack.peek()

    def visit_is_expr(self, is_expr: IsExpression):
        lex = is_expr.left_expression.accept(self)
        if not isinstance(lex, TypeAnnotation):
            raise ValueError("left expression of  'is' statement is not a type")
        type = is_expr.right_expression
        if not isinstance(lex, TypeAnnotation):
            raise ValueError("right expression of  'is' statement is not a type")
        return lex == type

    def run_function_with_aspect(self, aspects_list, fundef):
        values = self.last_result.copy()
        # prepare args for aspect
        arguments = []
        for value, param in zip(values, fundef.parameters):
            self.curr_scope.check_value_type(type=param.type, value=value)
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
        for value, param in zip(values, fundef.parameters):
            self.curr_scope.check_value_type(type=param.type, value=value)
            self.curr_scope.put_variable(
                param.name, ScopeVariable(value=value, type=param.type)
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
