class Stack:
    """
    A simple stack implementation using a list in Python.
    This class provides basic stack operations such as push, pop, peek, and checking if the stack is empty.
    It also allows checking the size of the stack and retrieving the whole stack as a list.
    """ 

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)
    
    def whole_stack(self):
        return self.items