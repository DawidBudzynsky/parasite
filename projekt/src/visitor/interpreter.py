from parser.values.string import String
import re


class Interpreter:
    def __init__(self, parser, visitor):
        self.parser = parser
        self.visitor = visitor

    def is_valid_regex(self, regex):
        try:
            re.compile(regex)
            return True
        except re.error:
            return False

    def get_matching_function_names(self, regex, functions):
        pattern = re.compile(regex)
        return [fun_name for fun_name in functions if pattern.match(fun_name)]

    def run(self):
        program = self.parser.parse_program()

        functions = program.functions
        if functions.get("main") is None:
            raise ValueError("Error: Missing main function")

        aspects = program.aspects

        fun_aspect_dict = {}

        for _, aspect in aspects.items():
            for fun in aspect.aspect_args:
                if isinstance(fun, String):
                    if self.is_valid_regex(fun.value):
                        matching_functions = self.get_matching_function_names(
                            fun.value, functions.keys()
                        )
                        for match in matching_functions:
                            if match not in fun_aspect_dict:
                                fun_aspect_dict[match] = []
                            if aspect not in fun_aspect_dict[match]:
                                fun_aspect_dict[match].append(aspect)
                else:
                    if fun_aspect_dict.get(fun.name) is None:
                        fun_aspect_dict[fun.name] = []
                    if aspect not in fun_aspect_dict[fun.name]:
                        fun_aspect_dict[fun.name].append(aspect)

        self.visitor.set_functions(functions)
        self.visitor.set_aspects(aspects)
        self.visitor.set_function_to_aspect_map(fun_aspect_dict)

        for fname, function in functions.items():
            if fname == "main":
                function.accept(self.visitor)
