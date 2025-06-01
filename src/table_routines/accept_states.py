class AcceptStates:
    """
      Defines accept states for the lexical analyzer, mapping each to a token type in acceptStates.
      
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