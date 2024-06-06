from abc import ABC, abstractmethod
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


class Visitor(ABC):
    @abstractmethod
    def visit_integer(self, element: Integer) -> None:
        pass

    @abstractmethod
    def visit_float(self, element: Float) -> None:
        pass

    @abstractmethod
    def visit_string(self, element: String) -> None:
        pass

    @abstractmethod
    def visit_bool(self, element: Bool) -> None:
        pass

    @abstractmethod
    def visit_identifier(self, element: Identifier) -> None:
        pass

    @abstractmethod
    def visit_variable(self, element: Variable) -> None:
        pass

    @abstractmethod
    def visit_minus_negate_expression(self, element: MinusNegateExpression) -> None:
        pass

    @abstractmethod
    def visit_add_expr(self, element: AddExpresion) -> None:
        pass

    @abstractmethod
    def visit_sub_expr(self, element: SubtractExpression) -> None:
        pass

    @abstractmethod
    def visit_multiply_expr(self, element: MultiplyExpression) -> None:
        pass

    @abstractmethod
    def visit_divide_expression(self, element: DivideExpression) -> None:
        pass

    @abstractmethod
    def visit_negate_expression(self, element: NegateExpression) -> None:
        pass

    @abstractmethod
    def visit_and_expression(self, element: AndExpression) -> None:
        pass

    @abstractmethod
    def visit_or_expression(self, element: OrExpression) -> None:
        pass

    @abstractmethod
    def visit_equals_expr(self, element: EqualsExpression) -> None:
        pass

    @abstractmethod
    def visit_not_equals_expr(self, element: NotEqualsExpression) -> None:
        pass

    @abstractmethod
    def visit_greater_equal_expr(self, element: GreaterEqualExpression) -> None:
        pass

    @abstractmethod
    def visit_greater_expr(self, element: GreaterExpression) -> None:
        pass

    @abstractmethod
    def visit_less_equal_expr(self, element: LessEqualExpresion) -> None:
        pass

    @abstractmethod
    def visit_less_expr(self, element: LessExpresion) -> None:
        pass

    @abstractmethod
    def visit_assign_statement(self, element: AssignStatement) -> None:
        pass

    @abstractmethod
    def visit_return_statement(self, element: ReturnStatement) -> None:
        pass

    @abstractmethod
    def visit_fun_call_statement(self, element: FunCallStatement) -> None:
        pass

    @abstractmethod
    def visit_function_declaration(self, element: FunctionDef) -> None:
        pass

    @abstractmethod
    def visit_block(self, element: Block) -> None:
        pass

    @abstractmethod
    def visit_if_statement(self, element: IfStatement) -> None:
        pass

    @abstractmethod
    def visit_loop_statement(self, element: LoopStatement) -> None:
        pass

    @abstractmethod
    def visit_for_each_statement(self, element: ForEachStatement) -> None:
        pass

    @abstractmethod
    def visit_access_expr(self, element: ObjectAccessExpression) -> None:
        pass

    @abstractmethod
    def visit_cast_expr(self, element: CastingExpression) -> None:
        pass

    @abstractmethod
    def visit_aspect_block(self, element: AspectBlock) -> None:
        pass

    @abstractmethod
    def visit_aspect_statement(self, element: Aspect) -> None:
        pass

    @abstractmethod
    def visit_before_statement(self, element: BeforeStatement) -> None:
        pass

    @abstractmethod
    def visit_after_statement(self, element: AfterStatement) -> None:
        pass

    @abstractmethod
    def visit_is_expr(self, element: IsExpression) -> None:
        pass
