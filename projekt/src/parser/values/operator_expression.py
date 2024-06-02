from parser.expression import Expression


# TODO: position
class OperatorExpression(Expression):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression
