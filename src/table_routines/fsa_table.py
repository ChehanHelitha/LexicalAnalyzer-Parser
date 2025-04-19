class FSATable:
    """
    Finite State Automaton (FSA) table for parsing the required grammar.
    This class contains a table that defines the transitions between states based on input symbols.
    The table is used to determine the next state given the current state and input symbol.
        Each row = a state (starting at state 0)
        Each column = a character category index (from char_map.py)
        Each cell = next state or -1 if the transition is invalid
    The FSA is designed to recognize a specific set of patterns in the input data.
    """
    def __init__(self):
        self.fsaTable = [
            [ 1,  1,  2, -1,  3, 11, -1,  5,  6,  7,  8,  4,  4,  4,  3],
            [ 1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1,  2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  4,  4,  4, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,  4, 10],
            [11, 11, 11, 11, 11,  9, 12, 11, 11, 11, 11, 11, -1, -1, 11],
            [-1, 11, -1, -1, -1, 11, 11, -1, -1, -1, -1, -1, -1, -1, -1],
        ]