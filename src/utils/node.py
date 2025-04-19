class Node:
    def __init__(self, data ):
        # Initialize the Node object with the provided data
        self.data = data
        # Initialize an empty list to store the children nodes
        self.children = []

    def add_child(self, child):
        # Add a child node to the current node's children list
        # The child is added at index 0 to ensure that the most recently added child appears first
        self.children.insert(0, child)

    def remove_child(self, child):
        # Check if the provided child exists in the children list
        if child in self.children:
            # If the child exists, remove it from the children list
            self.children.remove(child)
        else:
            # If the child does not exist, print a message indicating that it was not found
            print("Child not found")

    def __repr__(self):
        # String representation of the node, showing its data and the data of its children
        #print(self.children)
        """
        Helps with debugging complex structures like ASTs (Abstract Syntax Trees), parse trees, or general trees/graphs.
        Makes the object more informative when logged or printed.
        """
        children_data = ", ".join(str(child.data) for child in self.children)
        return f"Node(data={self.data}, children=[{children_data}])"