# utils/node.py
class Node:
    """Represents a node in the Abstract Syntax Tree (AST) or Standardized Tree (ST)."""
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value # For leaves like ID, INT, STR
        self.children = children if children is not None else []

    def __repr__(self):
        if self.value is not None:
            if isinstance(self.value, str):
                 val_repr = f"'{self.value}'"
            else:
                 val_repr = self.value
            return f"Node({self.type}:{val_repr})"
        else:
            child_repr = ', '.join(repr(c) for c in self.children)
            return f"Node({self.type}, [{child_repr}])"

# CSE specific value types (Closure, TupleValue, etc.) are moved to cse_machine.py