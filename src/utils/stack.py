class Stack:
    """
    A stack is an abstract data type that serves as a collection of elements, with two main operations:
    - push, which adds an element to the top of the stack, and
    - pop, which removes the element at the top of the stack.
    The order in which elements are added to the stack is known as the stack's "order of entry" or "last-in, first-out" (LIFO).
    This implementation uses a list as the underlying data structure.
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