class Interpreter:
    def __init__(self, parser, visitor):
        self.parser = parser
        self.visitor = visitor

    def run(self):
        program = self.parser.parse_program()

        functions = program.functions
        aspects = program.aspects

        fun_aspect_dict = {}
        for _, aspect in aspects.items():
            for fun in aspect.aspect_args:
                if fun_aspect_dict.get(fun.name) is None:
                    fun_aspect_dict[fun.name] = []
                fun_aspect_dict[fun.name].append(aspect)

        self.visitor.set_functions(functions)
        self.visitor.set_aspects(aspects)
        self.visitor.set_function_to_aspect_map(fun_aspect_dict)

        for fname, function in functions.items():
            if fname == "main":
                function.accept(self.visitor)
