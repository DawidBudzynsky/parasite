from parser.values.string import String
import re

from visitor.visitor import CodeVisitor


class Interpreter:
    def __init__(self):
        pass

    def is_valid_regex(self, regex):
        try:
            re.compile(regex)
            return True
        except re.error:
            return False

    def get_matching_function_names(self, regex, functions):
        pattern = re.compile(regex)
        return [fun_name for fun_name in functions if pattern.match(fun_name)]

    def run(self, program):
        visitor = CodeVisitor()
        program.accept(visitor)
