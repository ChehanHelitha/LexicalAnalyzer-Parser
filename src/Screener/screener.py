from src.Table_routines.keywords import Keywords
from src.utils.tokens import Token

class Screener:

    def _init_(self):

        self.keywords=Keywords().keywords

    
    def screener(self,tokens):
        filtered_tokens=[]

        for token in tokens:
            if token.get_type() =='DELETE':
                continue

            elif token.get_type()=='ID' and token.get_val() in self.keywords:
                filtered_tokens.append(Token(token.get_val(),"KEYWORD"))

            else:
                filtered_tokens.append(token)
            
            filtered_tokens.append(Token("EOF", "EOF"))
            
            return filtered_tokens
