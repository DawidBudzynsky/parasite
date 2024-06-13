from lexer.lexer import Lexer
from lexer.reader import Source
from parser.parser import Parser
from visitor.interpreter import Interpreter
import argparse
import sys
import io


def main(input_data):
    try:
        source = Source(io.StringIO(input_data))
        lexer = Lexer(source)
        parser = Parser(lexer)
        interpreter = Interpreter()
        interpreter.run(parser.parse_program())
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
                try:
                    source = Source(sourcefile)
                    lexer = Lexer(source)
                    parser = Parser(lexer)
                    interpreter = Interpreter()
                    interpreter.run(parser.parse_program())
                except Exception as e:
                    print(e)

        except FileNotFoundError:
            print(f"The file '{args.file_name}' was not found.")
            sys.exit(1)
    else:
        input_data = sys.stdin.read()
