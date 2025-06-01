
"""
Description: This module defines the ControlStructure class, which represents a control structure in the CSE machine.
# This module defines a control structure class for the CSE (Compiler, Symbolic, Expression) machine.

Usage: This module can be imported and used to create control structures in the CSE machine.

"""


from cse_machine.stack import Stack

class ControlStructure(Stack):
    """
    Represents a control structure in the CSE (Compiler, Symbolic, Expression) machine.
    Inherits from Stack class.

    Attributes:
        elements (list): List of elements in the control structure.
        index (int): Index of the control structure.
    """

    def __init__(self, index):
        """
        Initializes a new control structure.

        Args:
            index (int): Index of the control structure.
        """
        # Initialize the control structure
        super().__init__()
        self.elements = self.items  # Alias for the items attribute inherited from Stack
        self.index = index