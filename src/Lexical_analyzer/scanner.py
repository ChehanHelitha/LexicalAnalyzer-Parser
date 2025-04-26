from src.Errors_handling.Error_handler import ErrorHandler
from src.Table_routines.char_map import CharMap
from src.Table_routines.fsa_table import FSATable
from src.Table_routines.accept_states import AcceptStates
from src.utils.tokens import Token


class Scanner:
    def __init__(self):
        self.error = ErrorHandler().handle_error
        self.charMap = CharMap().charMap
        self.fsaTable = FSATable().fsaTable
        self.acceptStates = AcceptStates().acceptStates
        self.status = False

        self.current_token = ""  # Always initialize as a string
        self.current_state = 0
        self.output_tokens = list()
        self.index = 0
        self.line_number = 1

    def token_scan(self, input_string):
        self.input_string = input_string
        check_ending_newline(self.input_string)

        while self.index < len(input_string):
            character = input_string[self.index]
            input_index = self.charMap.get(character, -1)

            if character == "\n":
                self.line_number += 1

            if input_index == -1:
                self.error(
                    f"SCANNER:{character} at line {self.line_number} is not a valid character."
                )
                return

            next_state = self.fsaTable[self.current_state][input_index]

            # Handle when we've hit a valid token
            if next_state == -1 and self.current_state in self.acceptStates:
                self.output_tokens.append(
                    Token(self.current_token, self.acceptStates[self.current_state])
                )
                self.current_token = ""  # Reset current_token to an empty string

                if character == "\n":
                    self.line_number -= 1

            # Invalid token
            elif next_state == -1 and self.current_state not in self.acceptStates:
                self.error(
                    f"SCANNER:{self.current_token + character} at line {self.line_number} is not a valid token."
                )
                return

            # Continue tokenizing
            else:
                self.current_token += character
                self.index += 1
                self.current_state = next_state

        # End of string handling
        if self.current_state in self.acceptStates:
            print(f"Current token: {self.current_token}, Type: {self.acceptStates[self.current_state]}")

            self.output_tokens.append(
                Token(self.current_token, self.acceptStates[self.current_state])
            )

        # Handle comments (assuming "DELETE" is the token type for comments)
        elif self.current_token[0:2] == "//":
            self.output_tokens.append(Token(self.current_token, "DELETE"))

        else:
            self.error(
                f"SCANNER : {self.current_token} at line {self.line_number} is not a valid token."
            )
            return

        self.status = True
        return self.output_tokens


def check_ending_newline(input_string):
    if input_string[-1] != "\n":
        line = len(input_string.split("\n"))
        print("Potential parse problem -- tokens remain.")
        print(f"Remaining tokens begin at line {line}.")
