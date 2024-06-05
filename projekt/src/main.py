from lexer.lexer import Lexer
from lexer.reader import Source
from parser.parser import Parser
from visitor.interpreter import Interpreter
from visitor.visitor import CodeVisitor
import argparse


def main(file_name):
    try:
        with open(file_name, "r") as sourcefile:
            source = Source(sourcefile)
            lexer = Lexer(source)
            parser = Parser(lexer)
            visitor = CodeVisitor()
            interpreter = Interpreter(parser, visitor)
            interpreter.run()
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a file and print its contents.")
    parser.add_argument("file_name", type=str, help="The name of the file to read")
    args = parser.parse_args()
    main(args.file_name)
