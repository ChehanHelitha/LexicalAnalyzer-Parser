import re
# Make sure these imports point to the correct location of your utility files
from utils.tokens import Token, OPERATOR_MAP, LETTER, DIGIT, OPERATOR_SYMBOL, UNDERSCORE
from table_routines.keywords import KEYWORDS

# --- Token Regex Patterns (Order matters!) ---
# Defined using constants from utils.tokens
patterns = [
    ('COMMENT', r"//[^\n]*"),       # Comments first
    ('SPACES', r"[ \t\n]+"),        # Whitespace
    # RPAL String: Handles escapes \t, \n, \\, \', and allows other chars except ' \ unless escaped.
    ('STRING', r"'(?:\\t|\\n|\\\\|\\'|'|[^'\\])*'"),
    ('INTEGER', DIGIT + '+'),        # Integers
    # RPAL Operator: Handles multi-char operators like ->, >=, <=, **, etc.
    # Need to be careful with single chars like '-', '+', '/', '*' which are common.
    # Place generic OPERATOR_SYMBOL+ after more specific multi-char ops if needed,
    # but the current pattern covers them. Let parser resolve ambiguity (e.g., neg vs sub).
    ('OPERATOR', OPERATOR_SYMBOL + '+'), # General operator pattern
    ('IDENTIFIER', LETTER + r"(" + LETTER + r"|" + DIGIT + r"|" + UNDERSCORE + r")*"), # Identifiers
    ('L_PAREN', r"\("),             # Punctuation
    ('R_PAREN', r"\)"),
    ('SEMICOLON', r";"),
    ('COMMA', r","),
]

# Combined regex pattern
token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns))

class LexerError(Exception):
    """Custom exception for errors during lexing."""
    pass

class Lexer:
    """Scans the input text and produces a stream of tokens."""
    def __init__(self, text):
        if text is None:
             raise ValueError("Input text cannot be None")
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def _update_pos(self, match_text):
        """Updates line and column based on the matched text."""
        newline_chars = match_text.count('\n')
        self.line += newline_chars
        if newline_chars > 0:
            # Column resets to 1 + length after the last newline
            self.column = len(match_text) - match_text.rfind('\n')
        else:
            # No newlines, just add length to current column
            self.column += len(match_text)
        # Advance position in the text
        self.pos += len(match_text)

    def tokenize(self):
        """Performs the tokenization process."""
        while self.pos < len(self.text):
            match = token_re.match(self.text, self.pos)
            if not match:
                # Find the actual illegal character for a better error message
                illegal_char = self.text[self.pos]
                # Handle potential EOF edge case if pos is exactly len(text)
                if self.pos == len(self.text):
                     break # Reached end cleanly after last token
                raise LexerError(f"Illegal character '{illegal_char}' at line {self.line}, column {self.column}")

            token_type = match.lastgroup
            original_value_str = match.group(token_type) # <<< Store original matched string
            start_line = self.line                       # <<< Capture starting line
            start_col = self.column                      # <<< Capture starting column

            # Update position *after* capturing start line/col, using the original string length
            self._update_pos(original_value_str)

            # --- Now process the token type (skip spaces/comments) ---

            if token_type == 'SPACES' or token_type == 'COMMENT':
                continue # Skip delete tokens

            # --- Process value for non-skipped tokens ---
            processed_value = original_value_str # Default to original string

            if token_type == 'IDENTIFIER':
                if original_value_str in KEYWORDS:
                    token_type = original_value_str.upper() # Use uppercase keyword as type
                # processed_value remains original_value_str for identifiers

            elif token_type == 'OPERATOR':
                 processed_value = original_value_str # Keep the operator string

            elif token_type == 'STRING':
                try:
                    # Remove quotes and unescape standard Python escapes
                    temp_val = original_value_str[1:-1]
                    # Use 'unicode_escape' for standard escapes, then handle RPAL specifics if any
                    processed_value = bytes(temp_val, "utf-8").decode("unicode_escape")
                    # Example: If RPAL had `\z` as a special escape not covered by Python:
                    # processed_value = processed_value.replace('\z', 'some_replacement')
                except Exception as e:
                     # Use start_line for error reporting as self.line might be updated
                     raise LexerError(f"Error decoding string literal '{original_value_str}' near line {start_line}: {e}")

            elif token_type == 'INTEGER':
                 try:
                    processed_value = int(original_value_str) # <<< Convert to int HERE
                 except ValueError:
                     # Use start_line, start_col for error reporting
                     raise LexerError(f"Invalid integer format '{original_value_str}' at line {start_line}, column {start_col}")

            # --- Create the token ---
            # Use the captured start_line/start_col and the potentially processed_value
            # The complex line calculation is removed as start_line is now accurate.
            token = Token(token_type, processed_value, start_line, start_col)
            self.tokens.append(token)


        # Add an EOF token for the parser
        # Use the final lexer position's line and column
        self.tokens.append(Token('EOF', None, self.line, self.column))
        return self.tokens

# Example Usage (for testing screener.py directly)
# Ensure utils/token_printer.py exists and works
try:
    from utils.token_printer import print_tokens
except ImportError:
    # Provide a basic fallback if the printer isn't found during direct testing
    def print_tokens(tokens):
        print("--- Tokens (Basic Print) ---")
        for t in tokens: print(t)
        print("--------------------------")


if __name__ == '__main__':
    # sample_code = "let x = 10 in x + //comment\n 'hello\\tworld'"
    # sample_code = "'test\\nline'\n123 // C\nmy_var"
    sample_code = "let Sum(A) = Psum (A,Order A )\nwhere rec Psum (T,N) = N eq 0 -> 0 \n| Psum(T,N-1)+T N \nin Print ( Sum (1,2,3,4,5) )"
    print(f"--- Input Code ---\n{sample_code}\n------------------")
    lexer = Lexer(sample_code)
    try:
        tokens = lexer.tokenize()
        print_tokens(tokens)
    except LexerError as e:
        print(f"Lexer Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        import traceback
        traceback.print_exc()