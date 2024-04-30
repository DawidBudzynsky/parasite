from projekt.src.parser.values.operator_expression import OperatorExpression


class AddExpresion(OperatorExpression):
    def __init__(self, left_expression, right_expression):
        super().__init__(left_expression, right_expression)

    def __eq__(self, other):
        return (
            isinstance(other, AddExpresion)
            and self.left_expression == other.left_expression
            and self.right_expression == other.right_expression
        )

    def accept(self, visitator):
        return visitator.visit_add_expr(self)
