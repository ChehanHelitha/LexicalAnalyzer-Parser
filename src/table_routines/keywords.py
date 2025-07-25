# Set of reserved keywords in RPAL
class Keywords:
    """
    The Keywords class defines a set of reserved keywords in the RPAL language
    
    """
    def __init__(self):
        # Define a set containing all the keywords in the RPAL language
        self.keywords = {
            "let",   # Used for variable declaration
            "in",    # Used for scoping
            "fn",    # Used for function definition
            "where", # Used for local definitions
            "aug",   # Augmentation operator
            "or",    # Logical OR operator
            "not",   # Logical NOT operator
            "gr",    # Greater than operator
            "ge",    # Greater than or equal to operator
            "ls",    # Less than operator
            "le",    # Less than or equal to operator
            "eq",    # Equality operator
            "ne",    # Not equal to operator
            "true",  # Boolean value for true
            "false", # Boolean value for false
            "nil",   # Empty list value
            "dummy", # Dummy value
            "within",# Used for scoping
            "and",   # Logical AND operator
            "rec"    # Used for recursive function definition
        }