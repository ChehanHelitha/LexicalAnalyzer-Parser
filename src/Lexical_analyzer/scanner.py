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
        
        # Define all language keywords
        KEYWORDS = {
            'let', 'in', 'where', 'fn', 'if', 'then', 'else',
            'true', 'false', 'nil', 'dummy', 'rec', 'and'
        }
        
        while self.index < len(input_string):
            character = input_string[self.index]
            
            # Skip whitespace but track newlines
            if character.isspace():
                if character == "\n":
                    self.line_number += 1
                self.index += 1
                continue
                
            input_index = self.charMap.get(character, -1)
            
            if input_index == -1:
                self.error(f"Invalid character: '{character}' at line {self.line_number}")
                return

            next_state = self.fsaTable[self.current_state][input_index]
            
            # When we hit a potential token boundary
            if next_state == -1:
                if self.current_state in self.acceptStates:
                    token_value = self.current_token
                    token_type = self.acceptStates[self.current_state]
                    
                    # Special handling for keywords
                    if token_value.lower() in KEYWORDS:
                        token_type = token_value.upper()
                    
                    if token_type != "DELETE":
                        self.output_tokens.append(Token(token_value, token_type))
                    
                    # Reset for next token
                    self.current_token = ""
                    self.current_state = 0
                    continue  # Reprocess current character with fresh state
                else:
                    self.error(f"Invalid token: '{self.current_token}' at line {self.line_number}")
                    return

            self.current_token += character
            self.index += 1
            self.current_state = next_state

        # Handle any remaining token at end of input
        if self.current_state in self.acceptStates and self.current_token:
            token_value = self.current_token
            token_type = self.acceptStates[self.current_state]
            if token_value.lower() in KEYWORDS:
                token_type = token_value.upper()
            self.output_tokens.append(Token(token_value, token_type))
        
        self.status = True
        return self.output_tokens

def check_ending_newline(input_string):
    if input_string[-1] != "\n":
        line = len(input_string.split("\n"))
        print("Potential parse problem -- tokens remain.")
        print(f"Remaining tokens begin at line {line}.")