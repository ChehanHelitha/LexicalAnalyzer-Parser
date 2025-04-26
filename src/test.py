# Import the required classes
from src.Lexical_analyzer.scanner import Scanner
from src.Screener.screener import Screener
from src.Parser.parser_module import (
    Parser,
)  # Assuming the parser class is in parser_module.py

# Example code to parse
input_code = """
let  
    x = -15
in  
    Print(x > 0 -> 'Positive' | x < 0 -> 'Negative' | 'Zero')
"""

# Initialize the Scanner and Screener
scanner = Scanner()
screener = Screener()

# Tokenize the input code
tokens = scanner.token_scan(input_code)

# Screen the tokens (remove unnecessary ones like comments, etc.)
filtered_tokens = screener.screener(tokens)

# Initialize the Parser
parser = Parser()

# Parse the filtered tokens to create the AST
parser.parse(filtered_tokens)

# Check if parsing was successful and get the AST
if parser.status:
    ast = parser.get_ast_tree()  # Retrieve the Abstract Syntax Tree (AST)
    print("AST: ", ast)  # Print the AST structure
else:
    print("Parsing failed.")
