class CharMap:
    def __init__(self):
        """
        This class groups all possible characters into category indexes (0 to 14), each representing a type of character the scanner understands.

       """
        self.charMap = {
            # Uppercase letters
            'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
            'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0,
            # Lowercase letters
            'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
            'n': 1, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 1, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0,
            # digits
            '0': 2, '1': 2, '2': 2, '3': 2, '4': 2, '5': 2, '6': 2, '7': 2, '8': 2, '9': 2,
            # underscore
            '_': 3,
            # Special characters
            '|': 4, '+': 4, '-': 4, '*': 4, '<': 4, '>': 4, '&': 4, '.': 4, '@': 4, ':': 4, '=': 4, '˜': 4, ',': 4,
            '$': 4, '!': 4, '#': 4, '%': 4, 'ˆ': 4, '[': 4, ']': 4, '{': 4, '}': 4, '"': 4, '‘': 4, '?': 4,

            '\'': 5, '\\': 6, '(': 7, ')': 8, ';': 9, ',': 10, ' ': 11, '\t': 12, '\n': 13, '/': 14
        }

    def get_category(self, char):
        """        
           Returns the group number for a character, or -1 if not found.

        """
        return self.charMap.get(char, -1)