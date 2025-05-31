# Import the required classes
from src.Lexical_analyzer.scanner import Scanner
from src.Screener.screener import Screener
from src.Parser.parser_module import (
    Parser,
)  # Assuming the parser class is in parser_module.py

# Example code to parse
input_code = "let x = 5 in x"


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
    
scanner = Scanner()
input_code = "let x = 5 in x"
tokens = scanner.token_scan(input_code)
for token in tokens:
    print(f"<{token.type}: {token.value}>")