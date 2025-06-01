class Token:
    """A class representing a token with a type and value.
    This class provides methods to get and set the type and value of the token,
    as well as methods for string representation, equality checks, and hashing.
    """
    def __init__(self, value: str, type_: str):
        self.type = type_
        self.value = value

    def get_type(self) -> str:
        return self.type

    def get_value(self) -> str:
        return self.value

    def set_type(self, type_: str):
        self.type = type_

    def set_value(self, value: str):
        self.value = value

    def __str__(self):
        
        return f"<{self.type}: {self.value}>"

    def __repr__(self):
        return f"<{self.type}: {self.value}>"

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.type, self.value))