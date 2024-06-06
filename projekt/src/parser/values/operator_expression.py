from parser.expression import Expression


class OperatorExpression(Expression):
    def __init__(self, left_expression, right_expression, position):
        self.left_expression = left_expression
        self.right_expression = right_expression
        self.position = position
