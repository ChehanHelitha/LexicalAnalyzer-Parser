class Node:
    """
    A class representing a node in a tree structure.
    Each node can have multiple children, and it stores data associated with it.
    Attributes:
        data (any): The data stored in the node.
        children (list): A list of child nodes.
    """
    def __init__(self, data ):
        """
        Initialize a new node with the given data.
        Args:
            data (any): The data to be stored in the node.
        """
        
        self.data = data
        
        self.children = []

    def add_child(self, child):
        """
        Add a child node to the current node.
        Args:
            child (Node): The child node to be added.
        """
    
        self.children.insert(0, child)

    def remove_child(self, child):
        """
        Remove a child node from the current node.
        Args:
            child (Node): The child node to be removed.
        """
   
        if child in self.children:
            
            self.children.remove(child)
        else:

            print("Child not found")

    def __repr__(self):
        """Return a string representation of the node."""
        children_data = ", ".join(str(child.data) for child in self.children)
        return f"Node(data={self.data}, children=[{children_data}])"