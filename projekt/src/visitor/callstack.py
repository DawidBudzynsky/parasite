class CallStack:
    def __init__(self) -> None:
        self.call_stack_map = {}

    def push(self, fun_name):
        if (count := self.call_stack_map.get(fun_name)) is not None:
            self.call_stack_map[fun_name] = count + 1
        else:
            self.call_stack_map[fun_name] = 1

    def pop(self, fun_name):
        if (count := self.call_stack_map.get(fun_name)) is None:
            raise ValueError("no such function on callstack")
        if count > 1:
            self.call_stack_map[fun_name] = count - 1
        else:
            self.call_stack_map.pop(fun_name)

    def recursion_count(self, fun_name):
        if (count := self.call_stack_map.get(fun_name)) is None:
            return 0
        return count
