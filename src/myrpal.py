# myrpal.py
import sys
import argparse
import traceback

# Import pipeline components
from screener import Lexer, LexerError
from parser_module import Parser, SyntaxError
from build_standard_tree import standardize, StandardizerError
# Import the interpreter driver function and CSE error
from execution_engine import interpret, format_result, CseMachineError # CseMachineError now raised by interpret
# Import utilities
from utils.tree_printer import print_tree
# from utils.token_printer import print_tokens # Optional

def main():
    """Main function to parse arguments and run the interpreter pipeline."""
    parser = argparse.ArgumentParser(description="RPAL Interpreter")
    parser.add_argument("file_name", help="Path to the RPAL input file")
    parser.add_argument("-ast", action="store_true", help="Print the Abstract Syntax Tree only")
    # Add other flags as needed

    args = parser.parse_args()

    try:
        # 1. Read Input File
        try:
            with open(args.file_name, 'r', encoding='utf-8') as f:
                program_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found '{args.file_name}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
             print(f"Error reading file '{args.file_name}': {e}", file=sys.stderr)
             sys.exit(1)

        # 2. Lexing (Screening)
        lexer = Lexer(program_text)
        tokens = lexer.tokenize()

        # 3. Parsing
        parser = Parser(tokens)
        ast_root = parser.parse()

        # 4. Optional: Print AST
        if args.ast:
            print_tree(ast_root)
            sys.exit(0)

        # 5. Standardization
        st_root = standardize(ast_root)

        # 6. Interpretation (Execution)
        # The interpret function now handles creating/running the CSE machine
        final_value = interpret(st_root) # This might raise CseMachineError

        # 7. Output Result
        formatted_output = format_result(final_value)
        if formatted_output is not None:
             print(formatted_output) # Print the formatted result


    # Error Handling (Catch errors from each phase)
    except LexerError as e:
        print(f"Lexical Error: {e}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except StandardizerError as e:
        print(f"Standardization Error: {e}", file=sys.stderr)
        sys.exit(1)
    except CseMachineError as e: # Catch error raised by interpret()
        print(f"Runtime Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RecursionError as e:
        print(f"Runtime Error: Maximum recursion depth exceeded. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()