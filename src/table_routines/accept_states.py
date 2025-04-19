class AcceptStates:
    """
    This class defines the accept states for the lexical analyzer(Screener.py).
    Each accept state corresponds to a specific token type that the analyzer can recognize.
    The accept states are used to determine if a sequence of characters forms a valid token.
    The mapping of accept states to token types is defined in the `acceptStates` dictionary.
    """
    def __init__(self):
        # Initialize the accept states dictionary with mappings of state numbers to token types
        self.acceptStates = {
            1: 'ID',          # Identifier
            2: 'INT',         # Integer
            3: 'OPERATOR',    # Operator
            4: 'DELETE',      # Delete keyword
            5: '(',           # Left parenthesis
            6: ')',           # Right parenthesis
            7: ';',           # Semicolon
            8: ',',           # Comma
            9: 'STR'          # String
        }