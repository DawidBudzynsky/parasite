class Source:
    def __init__(self, source_stream):
        self.line_number = 1
        self.column = 0
        self.source_stream = source_stream
        self.character = chr(2)
        self.next()

    def get_char(self):
        return self.character

    def get_position(self):
        return self.line_number, self.column

    def next(self):
        if self.character == "":
            return
        if self.character == "\n":
            self.line_number += 1
            self.column = 0

        self.character = self.source_stream.read(1)

        if self.character == "\r":
            next_char = self.source_stream.read(1)
            if next_char == "\n":
                self.character = next_char
            else:
                self.source_stream.seek(self.source_stream.tell() - 1)

        self.column += 1
        return self.character

    def print_line(self, line_number):
        pos = self.source_stream.tell()
        self.source_stream.seek(0)

        for _ in range(0, line_number - 1):
            self.source_stream.readline()
        print(self.source_stream.readline())

        self.source_stream.seek(pos)
        return self.source_stream
