from table_routines.keywords import Keywords
from utils.tokens import Token

class Screener:
    def __init__(self):
        # Retrieve keywords from the Keywords class
        self.keywords = Keywords().keywords

    # Method to filter unwanted tokens from the input list of tokens
    def screener(self, tokens):
        # Iterate through the tokens
        filtered_tokens = []
        for token in tokens:
            # Remove tokens marked for deletion or EOF tokens
            if token.get_type() == 'DELETE':
                continue
            # Remove IDENTIFIER tokens if they match any keywords
            elif token.get_type() == 'ID' and token.get_value() in self.keywords:
                filtered_tokens.append(Token(token.get_value(), "KEYWORD"))
            # Add the token to the filtered list if it passes all checks
            else:
                filtered_tokens.append(token)
        # Add an EOF token to the end of the filtered list
        filtered_tokens.append(Token("EOF", "EOF"))
        # Return the filtered list of tokens
        return filtered_tokens