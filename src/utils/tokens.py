<<<<<<< HEAD
# src/utils/tokens.py

# Description:
# This module contains the Token class, which represents a token in a program.

#Usage:
# This module provides the Token class, which can be used to represent tokens in a program.   
class Token :
  

    def __init__(self, value: str, type_: str):
        """
        Initialize a new Token instance.

        Args:
            value (str): The value of the token.
            type_ (str): The type of the token.

        """
        self.type = type_
        self.value = value

    def get_type(self) -> str:
        """
        Get the type of the token.

        Returns:
            str: The type of the token.

        """
        return self.type

    def get_value(self) -> str:
        """
        Get the value of the token.

        Returns:
            str: The value of the token.

        """
        return self.value

    def set_type(self, type_: str):
        """
        Set the type of the token.

        Args:
            type_ (str): The new type of the token.

        """
        self.type = type_

    def set_value(self, value: str):
        """
        Set the value of the token.

        Args:
            value (str): The new value of the token.

        """
        self.value = value

    def __str__(self):
        """
        Return a string representation of the token.

        Returns:
            str: A string representation of the token, in the form "<type: value>".

        """
        return f"<{self.type}: {self.value}>"

    def __repr__(self):
        """
        Return an unambiguous string representation of the token.

        Returns:
            str: An unambiguous string representation of the token, in the form "<type: value>".

        """
        return f"<{self.type}: {self.value}>"

    def __eq__(self, other):
        """
        Define equality comparison between two tokens.

        Args:
            other (Token): The other token to compare with.

        Returns:
            bool: True if the two tokens are equal, False otherwise.

        """
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        """
        Define inequality comparison between two tokens.

        Args:
            other (Token): The other token to compare with.

        Returns:
            bool: True if the two tokens are not equal, False otherwise.

        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Return a hash value for the token.

        Returns:
            int: A hash value for the token.

        """
        return hash((self.type, self.value))

   
=======
class Token:
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
>>>>>>> origin/HEAD
