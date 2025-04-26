# src/utils/node.py

# Description
# This module contains the Node Class.It consists methods of binary tree data  structure


class Node:
    """
    A node in a binary tree data structure.

    A node contains a data field and a list of child nodes
    """

    def __init__(self, data):
        """
        Initialize a new node with the given data.

        Args:
             data(object):The data stored in the node.
        """

        self.data = data  # Initialize the Node object
        self.childern = []  # Initialize the children node by assigning the empty list

    def insert_child(self, child):
        """
        Insert a child node to the current node
        """

        self.childern.insert(
            0, child
        )  # insert a child to the current node's childeren list

    def remove_child(self, child):
        """
        Remove a child node from the current node.
        """

        if child in self.childern:
            self.childern.remove(
                child
            )  # If the child exists remove the child from current node's childeren list
        else:
            print("Child not found")

    def __repr__(self):
        """
        Return a string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        # String representation of the node, showing its data and the data of its children
        # print(self.children)
        children_data = ", ".join(str(child.data) for child in self.children)
        return f"Node(data={self.data}, children=[{children_data}])"
