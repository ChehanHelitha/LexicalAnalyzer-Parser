from Table_routines.char_map import CharMap
from Table_routines.fsa_table import FSATable
from Table_routines.accept_states import AcceptStates
from utils.tokens import Token

class Scanner:
    def __init__(self):
        self.charMap = CharMap().charMap
        self.fsaTable = FSATable().fsaTable
        self.acceptStates = AcceptStates().acceptStates
        self.status = False

        # Initialize the scanner state variables and output list variables
        self.current_token = str()
        self.current_state = 0
        self.output_tokens = list()
        self.index = 0
        self.line_number = 1


    def token_scan(self, input_string):
        self.input_string = input_string

        while self.index < len(input_string):
            character = input_string[self.index]
            input_index = self.charMap.get(character, -1)

            # Track line number
            if character == "\n":
                self.line_number += 1

            # If the character is not in the charMap, throw an error
            if input_index == -1:
                raise ValueError(f"SCANNER : {character} at line {self.line_number} is not a valid character.")

            next_state = self.fsaTable[self.current_state][input_index]

            # If the next state is unacceptable and the current state is an accept state,
            # add the token to the output and go back to the start state
            if next_state == -1 and self.current_state in self.acceptStates:
                self.output_tokens.append(Token(self.current_token, self.acceptStates[self.current_state]))
                self.current_token = ''
                self.current_state = 0

                if character == '\n':
                    self.line_number -= 1

            # If the next state is unacceptable and the current state is not an accept state, throw an error
            elif next_state == -1 and self.current_state not in self.acceptStates:
                raise Exception(f"SCANNER : {self.current_token + character} at line {self.line_number} is not a valid token.")
            else:
                self.current_token += character
                self.index += 1
                self.current_state = next_state

        if self.current_state in self.acceptStates:
            self.output_tokens.append(Token(self.current_token, self.acceptStates[self.current_state]))

        # If a comment is at the end of the file without EoL, it will not be considered as an error
        elif self.current_token[0:2] == '//':
            self.output_tokens.append(Token(self.current_token, 'DELETE'))

        else:
            raise Exception("SCANNER : {self.current_token} at line {self.line_number} is not a valid token.")

        self.status = True
        return self.output_tokens
