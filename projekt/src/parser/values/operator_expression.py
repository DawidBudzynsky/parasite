from projekt.src.parser.expression import Expression


class OperatorExpression(Expression):
    def __init__(self, left_expression=None, right_expression=None):
        self.left_expression = left_expression
        self.right_expression = right_expression
