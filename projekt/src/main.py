from lexer.lexer import Lexer
from lexer.reader import Source
from parser.parser import Parser
from visitor.interpreter import Interpreter
from visitor.visitor import CodeVisitor
import argparse
import sys
import io


def main(input_data):
    try:
        source = Source(io.StringIO(input_data))
        lexer = Lexer(source)
        parser = Parser(lexer)
        visitor = CodeVisitor()
        interpreter = Interpreter(parser, visitor)
        interpreter.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read a file or piped input and process its contents."
    )
    parser.add_argument(
        "file_name",
        nargs="?",
        type=str,
        help="The name of the file to read (optional if using piped input)",
    )
    args = parser.parse_args()

    if args.file_name:
        if not args.file_name.endswith(".prst"):
            print(
                f"Error: The file '{args.file_name}' does not have the required '.prst' extension."
            )
            sys.exit(1)
        try:
            with open(args.file_name, "r") as sourcefile:
                input_data = sourcefile.read()
        except FileNotFoundError:
            print(f"The file '{args.file_name}' was not found.")
            sys.exit(1)
    else:
        input_data = sys.stdin.read()

    main(input_data)
