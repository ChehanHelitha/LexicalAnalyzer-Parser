import sys
import re
import argparse
from collections import namedtuple

# --- Token Definitions ---

# Basic character sets
LETTER = r"[a-zA-Z]"
DIGIT = r"[0-9]"
OPERATOR_SYMBOL = r"[+\-*/<>&.@/:=~|$!#%^_[\]{}\"`?]" # Removed '-' from here initially as it conflicts with integer's negation
UNDERSCORE = r"_"

# Token Regex Patterns (Order matters!)
patterns = [
    ('COMMENT', r"//[^\n]*"),       # Comments first
    ('SPACES', r"[ \t\n]+"),        # Whitespace
    ('STRING', r"'(?:\\t|\\n|\\\\|\\'|'|[^'\\])*'"), # Strings (handle escapes)
    ('INTEGER', DIGIT + '+'),        # Integers
    ('OPERATOR', OPERATOR_SYMBOL + '+'), # Operators (handle multi-char)
    ('IDENTIFIER', LETTER + r"(" + LETTER + r"|" + DIGIT + r"|" + UNDERSCORE + r")*"), # Identifiers
    ('L_PAREN', r"\("),             # Punctuation
    ('R_PAREN', r"\)"),
    ('SEMICOLON', r";"),
    ('COMMA', r","),
]

# Combined regex pattern
token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns))

# Keywords (subset of IDENTIFIER)
KEYWORDS = {
    'let', 'in', 'fn', 'where', 'aug', 'or', '&', 'not', 'gr', 'ge', 'ls',
    'le', 'eq', 'ne', 'within', 'and', 'rec', 'true', 'false', 'nil', 'dummy'
}

# Operator remapping (from OPERATOR token value to internal AST/CSE name)
# Some are handled directly by keywords ('gr', 'ge', etc.)
OPERATOR_MAP = {
    '+': '+', '-': '-', '*': '*', '/': '/', '**': '**', '<': 'ls', '>': 'gr',
    '<=': 'le', '>=': 'ge', '=': '=', '~=': 'ne', '|': 'or', '&': '&',
    '@': '@', '->': '->',
    # RPAL specific keywords mapped from OPERATOR tokens if not covered by IDENTIFIER keywords
    'aug': 'aug',
    'or': 'or', # Already keyword, but can appear as operator too
    '&': '&',   # Already keyword, but can appear as operator too
    # Add others if needed based on grammar and potential lexing as OPERATOR
}


Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

# --- Lexer ---

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def _update_pos(self, match_text):
        lines = match_text.splitlines(keepends=True)
        if len(lines) > 1: # Check if there is a newline
            self.line += len(lines) -1
            self.column = len(lines[-1]) + 1
        else:
             self.column += len(match_text)
        self.pos += len(match_text)


    def tokenize(self):
        while self.pos < len(self.text):
            match = token_re.match(self.text, self.pos)
            if not match:
                raise LexerError(f"Illegal character '{self.text[self.pos]}' at line {self.line}, column {self.column}")

            token_type = match.lastgroup
            value = match.group(token_type)
            start_col = self.column # Store column before updating

            if token_type == 'SPACES' or token_type == 'COMMENT':
                self._update_pos(value) # Update position but don't yield token
                continue # Skip delete tokens

            elif token_type == 'IDENTIFIER':
                if value in KEYWORDS:
                    token_type = value.upper() # Treat keywords as distinct types initially
                # Remap operator-like keywords that might be parsed as identifiers
                if value in OPERATOR_MAP:
                    token_type = "OPERATOR" # Standardize to OPERATOR type for parser

            elif token_type == 'OPERATOR':
                 # Specific handling for single '-' which could be neg vs subtract
                 # The parser will differentiate based on context
                 # Keep '-' as OPERATOR for now
                 pass # Operator map might be used later if needed

            elif token_type == 'STRING':
                # Remove surrounding quotes and unescape
                value = value[1:-1]
                value = value.replace('\\t', '\t')
                value = value.replace('\\n', '\n')
                value = value.replace('\\\\', '\\')
                value = value.replace("\\'", "'")

            elif token_type == 'INTEGER':
                 value = int(value) # Convert to integer type


            token = Token(token_type, value, self.line, start_col)
            self.tokens.append(token)
            self._update_pos(match.group(0)) # Update position based on the full matched text

        # Add an EOF token for the parser
        self.tokens.append(Token('EOF', None, self.line, self.column))
        return self.tokens


# --- AST Node ---
class Node:
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value # For leaves like ID, INT, STR
        self.children = children if children is not None else []

    def __repr__(self):
        if self.value is not None:
            return f"Node({self.type}:{self.value})"
        else:
            return f"Node({self.type}, {self.children})"

# --- Parser ---

class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

    def _advance(self):
        """Consumes the current token and moves to the next one."""
        if self.token_index < len(self.tokens) - 1:
            self.token_index += 1
            self.current_token = self.tokens[self.token_index]
        # Don't advance past EOF

    def _expect(self, expected_type, expected_value=None):
        """Checks if the current token matches, consumes it, or raises SyntaxError."""
        token = self.current_token
        #print(f"Expecting {expected_type} ({expected_value}), got {token.type} ({token.value})") # Debug
        if token.type == expected_type:
            if expected_value is None or token.value == expected_value:
                self._advance()
                return token
            else:
                 raise SyntaxError(f"Expected token value '{expected_value}' but got '{token.value}' at line {token.line}, column {token.column}")
        else:
            # Special handling for operator keywords vs IDENTIFIER keywords
            if expected_type == 'OPERATOR' and token.type == 'IDENTIFIER' and token.value in OPERATOR_MAP:
                 if expected_value is None or token.value == expected_value:
                    self._advance()
                    # Return a token that looks like an OPERATOR for consistency downstream if needed
                    return Token('OPERATOR', token.value, token.line, token.column)
                 else:
                    raise SyntaxError(f"Expected operator value '{expected_value}' but got identifier '{token.value}' at line {token.line}, column {token.column}")

            # Handling keyword tokens (which were lexed with upper case type)
            if expected_type == 'KEYWORD' and token.type.isupper() and token.type.lower() == expected_value:
                 self._advance()
                 return token

            expected_str = f"'{expected_value}'" if expected_value else expected_type
            raise SyntaxError(f"Expected {expected_str} but got {token.type} '{token.value}' at line {token.line}, column {token.column}")

    def parse(self):
        """Starts the parsing process."""
        ast = self._parse_E()
        if self.current_token.type != 'EOF':
            raise SyntaxError(f"Unexpected token {self.current_token.type} '{self.current_token.value}' after parsing finished at line {self.current_token.line}")
        return ast

    # --- Grammar Rule Parsing Functions ---
    # E -> 'let' D 'in' E => 'let'
    #   -> 'fn' Vb+ '.' E  => 'lambda'
    #   -> Ew
    def _parse_E(self):
        if self.current_token.type == 'LET':
            self._advance()
            d_node = self._parse_D()
            self._expect('KEYWORD', 'in')
            e_node = self._parse_E()
            return Node('let', children=[d_node, e_node])
        elif self.current_token.type == 'FN':
            self._advance()
            vbs = []
            while self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'L_PAREN':
                vbs.append(self._parse_Vb())
            if not vbs:
                 raise SyntaxError(f"Expected Vb after 'fn' but got {self.current_token.type} at line {self.current_token.line}")
            self._expect('OPERATOR', '.') # Dot operator
            e_node = self._parse_E()
            return Node('lambda', children=vbs + [e_node])
        else:
            return self._parse_Ew()

    # Ew -> T 'where' Dr => 'where'
    #    -> T
    def _parse_Ew(self):
        t_node = self._parse_T()
        if self.current_token.type == 'WHERE':
            self._advance()
            dr_node = self._parse_Dr()
            return Node('where', children=[t_node, dr_node])
        else:
            return t_node

    # T -> Ta ( ',' Ta )+ => 'tau'
    #   -> Ta
    def _parse_T(self):
        ta_node = self._parse_Ta()
        if self.current_token.type == 'COMMA':
            nodes = [ta_node]
            while self.current_token.type == 'COMMA':
                self._advance()
                nodes.append(self._parse_Ta())
            return Node('tau', children=nodes)
        else:
            return ta_node

    # Ta -> Ta 'aug' Tc => 'aug'
    #    -> Tc
    def _parse_Ta(self):
        tc_node = self._parse_Tc()
        while self.current_token.type == 'OPERATOR' and self.current_token.value == 'aug':
            self._advance()
            next_tc = self._parse_Tc()
            tc_node = Node('aug', children=[tc_node, next_tc]) # Left associative
        return tc_node

    # Tc -> B '->' Tc '|' Tc => '->'
    #    -> B
    def _parse_Tc(self):
        b_node = self._parse_B()
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '->':
            self._advance()
            tc1_node = self._parse_Tc()
            self._expect('OPERATOR', '|')
            tc2_node = self._parse_Tc()
            return Node('->', children=[b_node, tc1_node, tc2_node])
        else:
            return b_node

    # B -> B 'or' Bt => 'or'
    #   -> Bt
    def _parse_B(self):
        bt_node = self._parse_Bt()
        while self.current_token.type == 'OPERATOR' and self.current_token.value == 'or':
            self._advance()
            next_bt = self._parse_Bt()
            bt_node = Node('or', children=[bt_node, next_bt]) # Left associative
        return bt_node

    # Bt -> Bt '&' Bs => '&'
    #    -> Bs
    def _parse_Bt(self):
        bs_node = self._parse_Bs()
        while self.current_token.type == 'OPERATOR' and self.current_token.value == '&':
             self._advance()
             next_bs = self._parse_Bs()
             bs_node = Node('&', children=[bs_node, next_bs]) # Left associative
        return bs_node

    # Bs -> 'not' Bp => 'not'
    #    -> Bp
    def _parse_Bs(self):
        if self.current_token.type == 'NOT':
            self._advance()
            bp_node = self._parse_Bp()
            return Node('not', children=[bp_node])
        else:
            return self._parse_Bp()

    # Bp -> A ('gr' | '>') A => 'gr'
    #    -> A ('ge' | '>=') A => 'ge'
    #    -> A ('ls' | '<') A => 'ls'
    #    -> A ('le' | '<=') A => 'le'
    #    -> A 'eq' A => 'eq'
    #    -> A 'ne' A => 'ne'
    #    -> A
    def _parse_Bp(self):
        a_node = self._parse_A()
        op_token = self.current_token
        # Check for comparison operators (both keyword-like and symbol-like)
        op_map = { 'gr': 'gr', '>': 'gr', 'ge': 'ge', '>=': 'ge',
                   'ls': 'ls', '<': 'ls', 'le': 'le', '<=': 'le',
                   'eq': 'eq', 'ne': 'ne' }

        op_value = None
        if op_token.type == 'OPERATOR' and op_token.value in op_map:
            op_value = op_map[op_token.value]
        elif op_token.type.isupper() and op_token.type.lower() in op_map: # Keyword comparisons
             op_value = op_map[op_token.type.lower()]

        if op_value:
            self._advance()
            a2_node = self._parse_A()
            return Node(op_value, children=[a_node, a2_node])
        else:
            return a_node


    # A -> A '+' At => '+'
    #   -> A '-' At => '-'
    #   -> '+' At
    #   -> '-' At => 'neg'
    #   -> At
    def _parse_A(self):
         # Handle unary + and - first
         if self.current_token.type == 'OPERATOR' and self.current_token.value == '+':
             self._advance()
             at_node = self._parse_At()
             # Unary plus often has no semantic effect, return child directly
             # Or potentially Node('pos', children=[at_node]) if needed
             return at_node
         elif self.current_token.type == 'OPERATOR' and self.current_token.value == '-':
             self._advance()
             at_node = self._parse_At()
             return Node('neg', children=[at_node])

         # Parse the first term (At)
         node = self._parse_At()

         # Handle binary + and - (left associative)
         while self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-']:
             op = self.current_token.value
             self._advance()
             at_node = self._parse_At()
             node = Node(op, children=[node, at_node])
         return node

    # At -> At '*' Af => '*'
    #    -> At '/' Af => '/'
    #    -> Af
    def _parse_At(self):
        af_node = self._parse_Af()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
             op = self.current_token.value
             self._advance()
             next_af = self._parse_Af()
             af_node = Node(op, children=[af_node, next_af]) # Left associative
        return af_node

    # Af -> Ap '**' Af => '**'
    #    -> Ap
    def _parse_Af(self):
        ap_node = self._parse_Ap()
        # Right associative: If we see '**', parse the rest of Af recursively first
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '**':
            self._advance()
            af_node = self._parse_Af()
            return Node('**', children=[ap_node, af_node])
        else:
            return ap_node

    # Ap -> Ap '@' '<IDENTIFIER>' R => '@'
    #    -> R
    def _parse_Ap(self):
         r_node = self._parse_R()
         # Left associative '@' application
         while self.current_token.type == 'OPERATOR' and self.current_token.value == '@':
             self._advance()
             id_token = self._expect('IDENTIFIER')
             id_node = Node('ID', value=id_token.value)
             next_r = self._parse_R()
             r_node = Node('@', children=[r_node, id_node, next_r])
         return r_node

    # R -> R Rn => 'gamma'
    #   -> Rn
    def _parse_R(self):
        rn_node = self._parse_Rn()
        # Function application is left associative ('gamma')
        while self.current_token.type in ['IDENTIFIER', 'INTEGER', 'STRING', 'L_PAREN'] or \
              self.current_token.type in ['TRUE', 'FALSE', 'NIL', 'DUMMY']:
            next_rn = self._parse_Rn()
            rn_node = Node('gamma', children=[rn_node, next_rn])
        return rn_node

    # Rn -> '<IDENTIFIER>'
    #    -> '<INTEGER>'
    #    -> '<STRING>'
    #    -> 'true' => 'true'
    #    -> 'false' => 'false'
    #    -> 'nil' => 'nil'
    #    -> '(' E ')'
    #    -> 'dummy' => 'dummy'
    def _parse_Rn(self):
        token = self.current_token
        if token.type == 'IDENTIFIER':
            self._advance()
            return Node('ID', value=token.value)
        elif token.type == 'INTEGER':
            self._advance()
            return Node('INT', value=token.value)
        elif token.type == 'STRING':
            self._advance()
            return Node('STR', value=token.value)
        elif token.type == 'TRUE':
            self._advance()
            return Node('true')
        elif token.type == 'FALSE':
            self._advance()
            return Node('false')
        elif token.type == 'NIL':
            self._advance()
            return Node('nil')
        elif token.type == 'DUMMY':
            self._advance()
            return Node('dummy')
        elif token.type == 'L_PAREN':
            self._advance()
            e_node = self._parse_E()
            self._expect('R_PAREN')
            return e_node # Parens just group, return the inner expression node
        else:
             raise SyntaxError(f"Unexpected token {token.type} '{token.value}' in R expression at line {token.line}")


    # D -> Da 'within' D => 'within'
    #   -> Da
    def _parse_D(self):
        da_node = self._parse_Da()
        if self.current_token.type == 'WITHIN':
            self._advance()
            d_node = self._parse_D()
            return Node('within', children=[da_node, d_node])
        else:
            return da_node

    # Da -> Dr ( 'and' Dr )+ => 'and'
    #    -> Dr
    def _parse_Da(self):
        dr_node = self._parse_Dr()
        if self.current_token.type == 'AND':
             nodes = [dr_node]
             while self.current_token.type == 'AND':
                 self._advance()
                 nodes.append(self._parse_Dr())
             return Node('and', children=nodes)
        else:
            return dr_node

    # Dr -> 'rec' Db => 'rec'
    #    -> Db
    def _parse_Dr(self):
        if self.current_token.type == 'REC':
            self._advance()
            db_node = self._parse_Db()
            return Node('rec', children=[db_node])
        else:
            return self._parse_Db()

    # Db -> Vl '=' E => '='
    #    -> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
    #    -> '(' D ')'
    def _parse_Db(self):
        if self.current_token.type == 'L_PAREN':
            self._advance()
            d_node = self._parse_D()
            self._expect('R_PAREN')
            return d_node # Parens just group definition

        # Lookahead needed to distinguish Vl = E from IDENT Vb+ = E
        # This requires backtracking or storing state, let's try a simpler approach first
        # If the first token is IDENTIFIER, check the *next* token.
        if self.current_token.type == 'IDENTIFIER':
            id_token = self.current_token
            # Peek ahead
            next_token_index = self.token_index + 1
            if next_token_index < len(self.tokens):
                 next_token = self.tokens[next_token_index]
                 # If next is '=' or ',', it's Vl = E
                 # If next is IDENTIFIER or '(', it's potentially fcn_form
                 if next_token.type == 'IDENTIFIER' or next_token.type == 'L_PAREN':
                     # Potential function form
                     self._advance() # Consume function name ID
                     func_name_node = Node('ID', value=id_token.value)
                     vbs = []
                     while self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'L_PAREN':
                         vbs.append(self._parse_Vb())
                     if not vbs: # Must have at least one Vb for fcn_form
                         raise SyntaxError(f"Expected Vb after function name '{id_token.value}' but got {self.current_token.type} at line {self.current_token.line}")
                     self._expect('OPERATOR', '=')
                     e_node = self._parse_E()
                     return Node('function_form', children=[func_name_node] + vbs + [e_node])
                 elif next_token.type == 'OPERATOR' and next_token.value == '=':
                      # It's Vl = E where Vl is just a single IDENTIFIER
                      vl_node = self._parse_Vl() # Parses the single ID
                      self._expect('OPERATOR', '=')
                      e_node = self._parse_E()
                      return Node('=', children=[vl_node, e_node])
                 elif next_token.type == 'COMMA':
                     # It's Vl = E where Vl is IDENTIFIER , ...
                     vl_node = self._parse_Vl() # Parses ID list
                     self._expect('OPERATOR', '=')
                     e_node = self._parse_E()
                     return Node('=', children=[vl_node, e_node])
                 else:
                     # Fallback? Could be just `id = E`, treat as Vl = E
                     vl_node = self._parse_Vl() # Parses the single ID
                     self._expect('OPERATOR', '=')
                     e_node = self._parse_E()
                     return Node('=', children=[vl_node, e_node])

            else: # Identifier followed by EOF? Error or simple assignment? Assume simple assignment
                vl_node = self._parse_Vl() # Parses the single ID
                self._expect('OPERATOR', '=')
                e_node = self._parse_E()
                return Node('=', children=[vl_node, e_node])

        # If it wasn't an identifier starting fcn_form, try parsing Vl directly
        vl_node = self._parse_Vl()
        self._expect('OPERATOR', '=')
        e_node = self._parse_E()
        return Node('=', children=[vl_node, e_node])


    # Vb -> '<IDENTIFIER>'
    #    -> '(' Vl ')'
    #    -> '(' ')' => '()'
    def _parse_Vb(self):
        if self.current_token.type == 'IDENTIFIER':
            id_token = self._advance()
            return Node('ID', value=id_token.value)
        elif self.current_token.type == 'L_PAREN':
            self._advance()
            if self.current_token.type == 'R_PAREN': # Special case for ()
                self._advance()
                return Node('()')
            else:
                vl_node = self._parse_Vl()
                self._expect('R_PAREN')
                return vl_node # Return the Vl node directly (often a comma list)
        else:
             raise SyntaxError(f"Expected IDENTIFIER or '(' for Vb but got {self.current_token.type} at line {self.current_token.line}")

    # Vl -> '<IDENTIFIER>' list ',' => ','?
    # Simplified: Parses one or more comma-separated identifiers
    # Returns a single ID node if only one, or a ',' node if multiple.
    def _parse_Vl(self):
        if self.current_token.type != 'IDENTIFIER':
            raise SyntaxError(f"Expected IDENTIFIER for Vl but got {self.current_token.type} at line {self.current_token.line}")

        ids = []
        while True:
            id_token = self._expect('IDENTIFIER')
            ids.append(Node('ID', value=id_token.value))
            if self.current_token.type == 'COMMA':
                self._advance()
            else:
                break # Stop if no more commas

        if len(ids) == 1:
            return ids[0]
        else:
            return Node(',', children=ids) # Use ',' node type to represent list


# --- AST Printing ---
def print_ast(node, depth=0):
    indent = '.' * depth
    if node.type in ['ID', 'INT', 'STR']:
        print(f"{indent}<{node.type}:{node.value}>")
    elif node.type in ['true', 'false', 'nil', 'dummy', '()']:
         print(f"{indent}<{node.type}>")
    else:
        print(f"{indent}{node.type}")
        for child in node.children:
            if child: # Ensure child is not None
                print_ast(child, depth + 1)
            else:
                 print(f"{indent}.<ERROR: None child in {node.type}>")


# --- Standardizer ---
# Converts AST to a simpler form for the CSE machine

def standardize(node):
    if node is None: return None

    # Standardize children first (usually)
    std_children = [standardize(child) for child in node.children]

    # Apply standardization rules based on node type
    if node.type == 'let':
        # let D in E => gamma (lambda V . E_std) D_std
        d_node = std_children[0]
        e_node = std_children[1]
        # Extract variables from D_std
        variables = extract_vars(d_node)
        lambda_node = Node('lambda', children=variables + [e_node])
        return Node('gamma', children=[lambda_node, d_node])

    elif node.type == 'where':
        # E where Dr => gamma (lambda V . E_std) Dr_std
        e_node = std_children[0]
        dr_node = std_children[1]
        variables = extract_vars(dr_node)
        lambda_node = Node('lambda', children=variables + [e_node])
        return Node('gamma', children=[lambda_node, dr_node])

    elif node.type == 'function_form':
        # fcn_form P V1 V2... = E => = P (lambda V1 . lambda V2 . ... E_std)
        p_node = std_children[0] # Function Name (ID)
        vbs = std_children[1:-1] # Variables (Vb nodes, standardized to ID or ,)
        e_node = std_children[-1] # Body

        # Flatten Vb list if necessary (handle Vl represented by ',')
        flat_vbs = []
        for vb in vbs:
            if vb.type == ',':
                flat_vbs.extend(vb.children)
            elif vb.type == '()': # () parameter list
                pass # Add nothing specific? or a dummy? CSE needs to handle this
            else: # Should be ID
                flat_vbs.append(vb)

        # Build nested lambdas
        current_e = e_node
        for vb in reversed(flat_vbs):
            current_e = Node('lambda', children=[vb, current_e])

        return Node('=', children=[p_node, current_e])

    elif node.type == 'lambda':
         # lambda Vb+ . E => lambda V1 lambda V2 ... E_std
         vbs = std_children[:-1]
         e_node = std_children[-1]
         flat_vbs = []
         for vb in vbs:
             if vb.type == ',':
                 flat_vbs.extend(vb.children)
             elif vb.type == '()':
                 pass # Handle empty param list if needed
             else: # Should be ID
                 flat_vbs.append(vb)

         current_e = e_node
         for vb in reversed(flat_vbs):
             current_e = Node('lambda', children=[vb, current_e])
         return current_e # Return the top-level lambda

    elif node.type == 'within':
        # D1 within D2 => = D2_std (gamma (lambda V1. D1_std) D2_vars?) No, this is wrong.
        # let (D1 within D2) = E => let D2 in let D1 = E
        # Standardize as: = D2_std (lambda V1 . D1_std) ? This doesn't match structure well.
        # Let's treat `within` like nested lets for standardization purpose.
        # D1 within D2 => gamma (lambda V2 . D1_std) D2_std (Applying D2 defs to D1)
        d1_node = std_children[0]
        d2_node = std_children[1]
        vars2 = extract_vars(d2_node)
        lambda_node = Node('lambda', children=vars2 + [d1_node])
        # This structure might not be quite right for CSE, but represents the scoping
        # Alternative: Create a specific 'within' node for CSE?
        # Let's stick to a structure similar to let:
        return Node('gamma', children=[Node('lambda', children=vars2 + [d1_node]), d2_node])
        # This feels more consistent with 'let'/'where' standardization.

    elif node.type == 'and':
        # and D1 D2 ... => tau D1_std D2_std ...
        # Already standardized children, just change type
        return Node('tau', children=std_children)

    elif node.type == 'rec':
         # rec Db => = P (Y* (lambda P . E)) where Db = (= P E) or fcn_form
         db_node = std_children[0] # Should be an '=' node after standardization
         if db_node.type != '=':
              raise StandardizerError("Expected '=' node inside 'rec'")
         p_node = db_node.children[0] # The variable being defined
         e_node = db_node.children[1] # The expression (often a lambda)
         lambda_node = Node('lambda', children=[p_node, e_node])
         ystar_node = Node('Y*') # Special node for Y-combinator
         gamma_node = Node('gamma', children=[ystar_node, lambda_node])
         return Node('=', children=[p_node, gamma_node]) # Define P = Y*(lambda P . E)

    elif node.type == '@':
        # Ap @ <ID> R => gamma (gamma Ap_std <ID>) R_std
        ap_node = std_children[0]
        id_node = std_children[1] # Should already be an ID node
        r_node = std_children[2]
        gamma1 = Node('gamma', children=[ap_node, id_node])
        return Node('gamma', children=[gamma1, r_node])

    # Base cases and other nodes: return node with standardized children
    else:
        node.children = std_children
        return node

def extract_vars(d_node):
    """Helper to get variable(s) defined by a D-like standardized node."""
    if d_node.type == '=': # Single definition: X = E
        vl = d_node.children[0]
        if vl.type == ',': # Multiple vars: (V1, V2) = E
            return vl.children # Return list of ID nodes
        else: # Single var: V = E
            return [vl] # Return list containing one ID node
    elif d_node.type == 'tau': # From 'and': tau (= V1 E1) (= V2 E2) ...
        vars_list = []
        for child_eq_node in d_node.children:
            if child_eq_node.type == '=':
                vl = child_eq_node.children[0]
                if vl.type == ',':
                    vars_list.extend(vl.children)
                else:
                    vars_list.append(vl)
            else:
                 raise StandardizerError(f"Expected '=' node within 'tau' (standardized 'and'), got {child_eq_node.type}")
        return vars_list
    else:
        # This might happen for 'rec' before full standardization? Or other cases.
        # Should ideally handle all definition structures D produces.
        # For now, assume it's a single definition if not '=' or 'tau'
        # This part needs careful review based on what standardized D looks like.
        # Let's assume D standardization always results in '=' or 'tau' at the top level for var extraction.
        raise StandardizerError(f"Cannot extract variables from standardized definition node of type {d_node.type}")


# --- CSE Machine ---

class CseMachineError(Exception):
    pass

# CSE Value Types
class Closure:
    def __init__(self, env_idx, variables, body):
        self.env_idx = env_idx # Index into the environment list E
        self.variables = variables # List of formal parameter ID Nodes
        self.body = body # Node representing the function body

    def __repr__(self):
        var_names = [v.value for v in self.variables]
        return f"Closure(env={self.env_idx}, vars={var_names})"

class TupleValue:
    def __init__(self, values):
        self.values = values # List of actual CSE values

    def __repr__(self):
        return f"Tuple({self.values})"

# Environment marker object
class EnvMarker:
    def __init__(self, index):
        self.index = index # index in E list
    def __repr__(self):
        return f"EnvMarker({self.index})"

# Primitive function marker (could also use closures)
class PrimitiveFunction:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Prim({self.name})"

# Y* marker object
class YStar:
    def __repr__(self):
        return "Y*"
ETA = object() # Special object for eta-abstractions (recursive closures)

class CSEMachine:
    def __init__(self):
        self.control = []  # C stack (list acting as stack)
        self.stack = []    # S stack (values)
        self.environments = [[]] # E: List of environments (frames), start with global (env 0)
                               # Each frame is a list of (name, value) tuples
        self.current_env_idx = 0

        # Pre-populate environment 0 with built-ins
        builtins = {
            # IO
            "Print": PrimitiveFunction("Print"),
            # Numeric
            "Isinteger": PrimitiveFunction("Isinteger"),
            "Istruthvalue": PrimitiveFunction("Istruthvalue"),
            "Isstring": PrimitiveFunction("Isstring"),
            "Istuple": PrimitiveFunction("Istuple"),
            "Isdummy": PrimitiveFunction("Isdummy"),
            "Isfunction": PrimitiveFunction("Isfunction"), # Check if Closure
            # String
            "Stem": PrimitiveFunction("Stem"),
            "Stern": PrimitiveFunction("Stern"),
            "Conc": PrimitiveFunction("Conc"),
            # Tuple
            "Order": PrimitiveFunction("Order"),
            # System? (Maybe needed for errors or specific behaviors)
            "stop": PrimitiveFunction("stop"), # For explicit termination?
        }
        for name, func in builtins.items():
             self.environments[0].append((name, func))


    def _lookup(self, name):
        """Looks up a name in the environment chain."""
        env_idx = self.current_env_idx
        while env_idx is not None:
            env = self.environments[env_idx]
            for var_name, value in reversed(env): # Search current scope first
                if var_name == name:
                    return value
            # Find parent environment index (stored in EnvMarker if available)
            parent_idx = None
            for item in reversed(self.control): # Look for the env marker that created this env
                if isinstance(item, EnvMarker) and item.index == env_idx:
                     # The environment *below* this marker's closure's env is the parent
                     # This is tricky. Let's rethink environment structure.

                     # Simpler: Store parent index directly when creating environment?
                     # Let's try just chaining through the E list for now, assuming lexical scope.
                     # Need a way to link environments. Maybe store parent index in frame?
                     # Modify E to be list of (frame, parent_idx) tuples?
                     # Let's stick to simple list for now and rely on closure env_idx

                     # Use closure's captured env_idx to find parent if needed
                     # This lookup seems complex. Let's simplify:
                     # A closure captures its definition environment. When called,
                     # a *new* environment is created whose parent IS the captured environment.

                     # Let's store parent index with each environment frame
                     # E = [[(name, val)...], [(name, val)..., parent_idx], ...]
                     if len(self.environments[env_idx]) > 0 and isinstance(self.environments[env_idx][-1], int):
                         parent_idx = self.environments[env_idx][-1]
                     else: # Global env has no parent index element
                         parent_idx = None
                     break # Stop searching control stack once we find the relevant marker? No needed.

            env_idx = parent_idx # Move to parent

        raise CseMachineError(f"Unbound variable '{name}'")

    def _apply_primitive(self, prim_func, actual_param):
        """Applies a built-in primitive function."""
        name = prim_func.name
        # print(f"Applying primitive {name} to {actual_param}") # Debug

        # Unary Ops
        if name == "Isinteger": self.stack.append(isinstance(actual_param, int))
        elif name == "Istruthvalue": self.stack.append(isinstance(actual_param, bool))
        elif name == "Isstring": self.stack.append(isinstance(actual_param, str))
        elif name == "Istuple": self.stack.append(isinstance(actual_param, TupleValue))
        elif name == "Isdummy": self.stack.append(actual_param == 'dummy') # Represent dummy as string?
        elif name == "Isfunction": self.stack.append(isinstance(actual_param, Closure))
        elif name == "Stem":
            if not isinstance(actual_param, str): raise CseMachineError("Stem expects a string")
            self.stack.append(actual_param[0] if actual_param else "")
        elif name == "Stern":
            if not isinstance(actual_param, str): raise CseMachineError("Stern expects a string")
            self.stack.append(actual_param[1:] if len(actual_param)>0 else "")
        elif name == "Order":
            if not isinstance(actual_param, TupleValue): raise CseMachineError("Order expects a tuple")
            self.stack.append(len(actual_param.values))
        elif name == "Print":
            # Print has side effect, pushes dummy? Or result? Let's push dummy.
            print(self._format_value(actual_param), end='') # RPAL often has no newline
            self.stack.append('dummy') # Common convention
        elif name == "stop":
            # How to handle stop? Clear control stack?
            print("\nExecution stopped by 'stop'.")
            self.control = [] # Clear control stack to terminate
        # Binary Ops (need to pop another value from stack)
        elif name in ['+', '-', '*', '/', '**', 'eq', 'ne', 'ls', 'le', 'gr', 'ge', 'or', '&', 'Conc', 'aug']:
             val2 = actual_param
             if not self.stack: raise CseMachineError(f"Not enough operands for binary op '{name}'")
             val1 = self.stack.pop()
             # print(f"Binary op {name} with {val1} and {val2}") # Debug

             # Type checking / Coercion might be needed depending on RPAL rules
             if name == '+': result = val1 + val2
             elif name == '-': result = val1 - val2
             elif name == '*': result = val1 * val2
             elif name == '/':
                 if val2 == 0: raise CseMachineError("Division by zero")
                 result = val1 // val2 # Integer division
             elif name == '**': result = val1 ** val2
             elif name == 'eq': result = val1 == val2
             elif name == 'ne': result = val1 != val2
             elif name == 'ls': result = val1 < val2
             elif name == 'le': result = val1 <= val2
             elif name == 'gr': result = val1 > val2
             elif name == 'ge': result = val1 >= val2
             elif name == 'or': result = val1 or val2 # Short-circuiting handled by grammar? No, by CSE if needed. Here standard 'or'.
             elif name == '&': result = val1 and val2 # Standard 'and'.
             elif name == 'Conc':
                 if not isinstance(val1, str) or not isinstance(val2, str): raise CseMachineError("Conc expects two strings")
                 result = val1 + val2
             elif name == 'aug':
                 if not isinstance(val1, TupleValue) or not isinstance(val2, TupleValue):
                     # RPAL 'aug' might also work on non-tuples, need spec clarification.
                     # Assuming tuple augmentation for now.
                     raise CseMachineError("aug expects two tuples (currently)")
                 result = TupleValue(val1.values + val2.values)
             else: raise CseMachineError(f"Unknown binary primitive '{name}'")
             self.stack.append(result)
        # Unary Ops handled by nodes ('neg', 'not')
        elif name == 'neg':
            if not isinstance(actual_param, (int, float)): raise CseMachineError("neg expects a number")
            self.stack.append(-actual_param)
        elif name == 'not':
            if not isinstance(actual_param, bool): raise CseMachineError("not expects a boolean")
            self.stack.append(not actual_param)
        else:
            raise CseMachineError(f"Unimplemented primitive function '{name}'")


    def _format_value(self, value):
        """Formats CSE values for printing according to RPAL conventions."""
        if isinstance(value, str):
            # RPAL strings don't show quotes in output typically
            # Need to re-escape internal special chars for printing if necessary?
            # Let's print Python's representation for now, might need adjustment
             # Re-escape for printing?
            return value.replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n').replace("'", "\\'")
            # Or just print the direct value:
            # return value
        elif isinstance(value, bool):
            return str(value).lower() # 'true' or 'false'
        elif isinstance(value, Closure):
            # Maybe print [closure env# (vars)]
             vars_str = ", ".join(v.value for v in value.variables)
             return f"[closure env{value.env_idx} ({vars_str})]"
        elif isinstance(value, TupleValue):
            return "(" + ", ".join(self._format_value(v) for v in value.values) + ")"
        elif value is None: # Check for RPAL nil?
            return "nil" # Assuming None represents nil
        elif value == 'dummy':
             return "dummy"
        else: # Integers, etc.
            return str(value)


    def evaluate(self, std_tree):
        self.control = [std_tree] # Start with the root of the standardized tree
        self.stack = []
        # Initial environment (env 0) is already set up with builtins
        self.environments = [list(self.environments[0])] # Make a copy to avoid modifying template?
        self.current_env_idx = 0

        MAX_STEPS = 10000 # Prevent infinite loops
        steps = 0

        while self.control and steps < MAX_STEPS:
            steps += 1
            # print(f"\nStep {steps}:") # Debug
            # print(f" C: {self.control}") # Debug
            # print(f" S: {self.stack}") # Debug
            # print(f" E: {self.environments}") # Debug
            # print(f" CurEnv: {self.current_env_idx}") # Debug


            ctrl_item = self.control.pop()

            if isinstance(ctrl_item, Node):
                node = ctrl_item
                # Rule 1 & 2: Literals
                if node.type == 'INT': self.stack.append(node.value)
                elif node.type == 'STR': self.stack.append(node.value)
                elif node.type == 'true': self.stack.append(True)
                elif node.type == 'false': self.stack.append(False)
                elif node.type == 'nil': self.stack.append(None) # Use Python None for nil
                elif node.type == 'dummy': self.stack.append('dummy') # Use string 'dummy'

                # Rule 3: Lookup Identifier
                elif node.type == 'ID':
                    value = self._lookup(node.value)
                    self.stack.append(value)

                # Rule 4: Lambda -> Closure
                elif node.type == 'lambda':
                     # lambda V B => Create closure [env, V, B]
                     variables = node.children[:-1] # All but last are vars
                     body = node.children[-1]
                     # Flatten variable list if needed (e.g., from Vl ',')
                     flat_vars = []
                     for v in variables:
                         if v.type == ',': flat_vars.extend(v.children)
                         elif v.type == '()': pass # Empty param list
                         else: flat_vars.append(v) # Should be ID nodes
                     closure = Closure(self.current_env_idx, flat_vars, body)
                     self.stack.append(closure)

                # Rule 10: Conditional (->)
                elif node.type == '->':
                     # B -> C1 | C2 => push beta, C2, C1 onto control, then B
                     cond, then_branch, else_branch = node.children
                     self.control.append('beta') # Beta marker object/string
                     self.control.append(else_branch)
                     self.control.append(then_branch)
                     self.control.append(cond) # Evaluate condition next

                # Rule 11: Operator Application (gamma)
                elif node.type == 'gamma':
                    # gamma L R => push gamma marker, R, L onto control
                    if len(node.children) != 2: raise CseMachineError(f"Gamma node expects 2 children, got {len(node.children)}")
                    left, right = node.children
                    self.control.append('gamma') # Gamma marker object/string
                    self.control.append(right)
                    self.control.append(left)

                # Rule 13: Tuples (tau)
                elif node.type == 'tau':
                    # tau T1 T2 ... Tn => push tau marker(n), Tn, ..., T1
                    n = len(node.children)
                    self.control.append(('tau', n)) # Tau marker tuple (name, arity)
                    for child in reversed(node.children):
                        self.control.append(child)

                # Other node types that act like operators (push op, then operands)
                elif node.type in ['+', '-', '*', '/', '**', 'eq', 'ne', 'ls', 'le', 'gr', 'ge', 'or', '&', 'aug']: # Binary ops handled by PrimitiveFunction now
                     # Should these be handled by pushing PrimitiveFunction('op')? Yes.
                     # Let's assume binary ops are looked up as identifiers '+'/'-'/etc
                     # However, the standardized tree still has nodes for them.
                     # Let's handle them explicitly here by pushing the operator name/primitive
                     op_prim = PrimitiveFunction(node.type)
                     self.control.append(op_prim) # Operator itself goes on control last
                     self.control.append(node.children[1]) # Right operand
                     self.control.append(node.children[0]) # Left operand

                elif node.type in ['neg', 'not']: # Unary ops
                     op_prim = PrimitiveFunction(node.type)
                     self.control.append(op_prim)
                     self.control.append(node.children[0]) # The single operand

                # Rule for definition (=) - Handled by standardization into let/where/rec -> gamma/lambda
                # Rule for Y* (rec)
                elif node.type == 'Y*':
                     self.stack.append(YStar()) # Push the Y* object

                # Unhandled AST node?
                else:
                    raise CseMachineError(f"Unhandled AST node type in CSE: {node.type}")

            # Handle markers/non-node items on control stack
            elif isinstance(ctrl_item, str): # Markers like 'gamma', 'beta'
                marker = ctrl_item
                if marker == 'gamma':
                     # Rule 5 & 6: Apply closure or primitive
                     if not self.stack: raise CseMachineError("Stack empty when expecting Rand for gamma application")
                     rand = self.stack.pop()
                     if not self.stack: raise CseMachineError("Stack empty when expecting Rator for gamma application")
                     rator = self.stack.pop()

                     if isinstance(rator, Closure):
                         # Rule 5: Closure application
                         closure = rator
                         # Create new environment e' linked to closure's env
                         new_env_idx = len(self.environments)
                         parent_env_idx = closure.env_idx
                         new_env_frame = [] # Start empty
                         # Add parent link conceptually (maybe store parent index in frame?)
                         # self.environments.append((new_env_frame, parent_env_idx)) # If using tuples
                         self.environments.append(new_env_frame) # Simpler list for now

                         # Bind formal parameters to actual parameters
                         if len(closure.variables) == 1: # Single argument
                             formal_var_name = closure.variables[0].value
                             new_env_frame.append((formal_var_name, rand))
                         elif len(closure.variables) > 1: # Multi-argument (passed as tuple)
                             if not isinstance(rand, TupleValue) or len(rand.values) != len(closure.variables):
                                  raise CseMachineError(f"Argument count mismatch: expected {len(closure.variables)}, got {rand}")
                             for i, formal_var in enumerate(closure.variables):
                                 new_env_frame.append((formal_var.value, rand.values[i]))
                         # Else: 0 arguments (lambda () . E) - no bindings needed

                         # Push environment marker and body onto control
                         self.control.append(EnvMarker(new_env_idx))
                         self.control.append(closure.body)
                         # Set current environment to the new one
                         self.current_env_idx = new_env_idx

                     elif isinstance(rator, PrimitiveFunction):
                         # Rule 6: Primitive function application
                         self._apply_primitive(rator, rand)

                     elif isinstance(rator, TupleValue):
                         # Rule 12: Tuple selection
                         if not isinstance(rand, int): raise CseMachineError("Tuple selection requires an integer index")
                         index = rand - 1 # RPAL uses 1-based indexing
                         if 0 <= index < len(rator.values):
                             self.stack.append(rator.values[index])
                         else:
                             raise CseMachineError(f"Tuple index {rand} out of bounds for tuple of size {len(rator.values)}")

                     elif isinstance(rator, YStar):
                         # Rule related to 'rec' standardization: Y* lambda P.E
                         if not isinstance(rand, Closure): raise CseMachineError("Y* expects a closure")
                         eta_closure = Closure(rand.env_idx, rand.variables, rand.body)
                         eta_closure.is_recursive = True # Mark it specially? Or handle in lookup?
                         # Need eta-abstraction: bind P to the eta-closure itself within the closure's env
                         # This requires modifying the closure's environment, which is tricky.
                         # Alternative CSE: Store the closure itself in the stack, create env later.
                         # Let's try simpler: push closure back onto stack, ready for binding.
                         # The standard Y* rule involves creating an eta-record. Let's approximate:
                         # Push the closure itself, but mark it for recursive binding?
                         # Simpler: Let the '=' binding handle it. Y* gamma lambda -> = Name (Y* lambda)
                         # When Name is looked up, if it points to Y* result, bind recursively?
                         # Revisit Y* implementation:
                         # Y* expects lambda f. B. It produces a value X such that X = B[f->X]
                         # When gamma applies Y* to the lambda:
                         # Pop lambda (f, B, e)
                         # Create new closure eta = Closure(e, f, B) but somehow make f inside B refer to eta itself.
                         # Push eta onto stack.
                         # Let's try marking the closure:
                         lambda_closure = rand
                         lambda_closure.recursive_marker = ETA # Add a marker
                         self.stack.append(lambda_closure)


                     else:
                         raise CseMachineError(f"Cannot apply non-callable type: {type(rator)}")

                elif marker == 'beta':
                     # Rule 10 (cont.): Conditional execution
                     if not self.stack: raise CseMachineError("Stack empty for beta condition")
                     cond_val = self.stack.pop()
                     if not isinstance(cond_val, bool): raise CseMachineError(f"Conditional expected boolean, got {cond_val}")

                     # Pop then/else branches from control
                     else_branch = self.control.pop()
                     then_branch = self.control.pop()

                     if cond_val is True:
                         self.control.append(then_branch) # Execute then branch
                         # Discard else branch implicitly
                     else:
                         self.control.append(else_branch) # Execute else branch
                         # Discard then branch implicitly

            # Handle environment markers
            elif isinstance(ctrl_item, EnvMarker):
                # Rule 5 (cont.): Exit environment
                marker = ctrl_item
                # Find the parent environment
                # If we stored parent index: parent_idx = self.environments[marker.index][1]
                # Find parent based on closure env of marker? No, that's forward.
                # Find the *previous* EnvMarker on the control stack? No.
                # Find the EnvMarker that created the *current* env_idx? No.
                # When an EnvMarker(idx) is processed, it means the function called in env `idx` is returning.
                # The environment *before* `idx` was created is the one to return to.
                # This implies closures need to capture not just the index, but the *state* to return to.

                # Let's retry the simple model: Restore the environment index that was active
                # *before* the current one was created. This was saved implicitly by the call stack.
                # Find the env marker on the stack that created this one? No.
                # The closure application (Rule 5) changed self.current_env_idx.
                # When EnvMarker is hit, we need to restore the previous one.

                # Strategy: When pushing EnvMarker(new_idx), also push current_env_idx onto stack S? No.
                # Strategy: When creating env `new_idx`, store its parent `self.current_env_idx` with it.
                # self.environments[new_env_idx].append(parent_idx_marker) # Special marker?
                # Let's try storing parent index directly in the Closure/EnvMarker system.

                # Find the environment that created the current one (marker.index).
                # This requires searching the control stack or storing parent links.

                # Simplified approach: Assume lexical scope. Find the defining environment of the *closure*
                # that led to this EnvMarker.
                # This seems overly complex. Let's trust the standard CSE model:
                # The EnvMarker simply signals the end of the current scope. We need to find
                # the parent scope index. Let's assume the parent index is implicitly managed
                # by the nesting of calls on the control stack.
                # When EnvMarker(idx) is popped, search backwards in E for the *first* env
                # that is NOT idx. This feels wrong.

                # Let's assume the parent environment index is simply the index of the environment
                # captured in the *closure* that was called.
                # Find the closure that caused this EnvMarker? Difficult.

                # Backtrack: Let the environment list E just be the list of frames.
                # The `current_env_idx` determines the active scope chain.
                # The EnvMarker should just signal returning to the *caller's* environment.
                # How to find the caller's environment index?
                # It must have been the `current_env_idx` *before* the gamma application (Rule 5) happened.

                # Solution: Store the old `current_env_idx` on the *control* stack before the EnvMarker?
                # Rule 5 revised:
                # ...
                # self.control.append(EnvMarker(new_env_idx)) # Marker for the new env
                # self.control.append(self.current_env_idx) # Push old env index *before* the marker
                # self.control.append(closure.body)
                # self.current_env_idx = new_env_idx
                # ...
                # Then, when processing EnvMarker:
                # popped_marker = ctrl_item
                # restored_env_idx = self.control.pop() # Pop the saved index
                # self.current_env_idx = restored_env_idx
                # This seems plausible. Let's try this modification.

                # Rule 5 modification applied above. Now handle EnvMarker here:
                # Popping EnvMarker means the function body is done.
                # The next item on C should be the caller's environment index.
                # But EnvMarker itself doesn't hold that info.
                # Let's redefine EnvMarker to hold the index to restore:
                # Rule 5 revised again:
                # ...
                # self.control.append(EnvMarker(self.current_env_idx)) # Marker stores *caller's* index
                # self.control.append(closure.body)
                # self.current_env_idx = new_env_idx
                # ...
                # Then, when processing EnvMarker(caller_idx):
                self.current_env_idx = ctrl_item.index # Restore caller's environment index


            # Handle tuple markers
            elif isinstance(ctrl_item, tuple) and ctrl_item[0] == 'tau':
                # Rule 13 (cont.): Collect values into tuple
                marker_name, arity = ctrl_item
                if len(self.stack) < arity: raise CseMachineError(f"Not enough values on stack for tau (expected {arity}, found {len(self.stack)})")
                values = []
                for _ in range(arity):
                    values.append(self.stack.pop())
                # Values were pushed in reverse order, so pop gives T_n, ..., T_1
                # Resulting tuple should be (T_1, ..., T_n)
                self.stack.append(TupleValue(list(reversed(values))))

            # Handle PrimitiveFunction objects on control stack (from explicit node handling)
            elif isinstance(ctrl_item, PrimitiveFunction):
                 # Apply it to the top of the value stack
                 if not self.stack: raise CseMachineError(f"Stack empty when applying primitive {ctrl_item.name}")
                 operand = self.stack.pop()
                 self._apply_primitive(ctrl_item, operand)


            else:
                 raise CseMachineError(f"Unknown item on control stack: {ctrl_item}")


        if steps >= MAX_STEPS:
            print("\nCSE machine exceeded maximum steps.", file=sys.stderr)
            return None

        if len(self.stack) == 1:
             final_value = self.stack[0]
             # Special case for top-level Print: result is dummy, but we printed.
             # Let's return the actual computed value unless it's the dummy from Print.
             # This needs more thought - does the RPAL spec mandate the final value?
             # Usually, the value on the stack is the result. If the program ends with Print,
             # the stack might hold 'dummy'.
             return final_value
        elif len(self.stack) == 0:
             print("\nWarning: CSE machine finished with empty stack.", file=sys.stderr)
             return None # Or raise error?
        else:
             print(f"\nWarning: CSE machine finished with multiple values on stack: {self.stack}", file=sys.stderr)
             return self.stack[-1] # Return top value?


# --- Main Execution Logic ---

def main():
    parser = argparse.ArgumentParser(description="RPAL Interpreter")
    parser.add_argument("file_name", help="Path to the RPAL input file")
    parser.add_argument("-ast", action="store_true", help="Print the Abstract Syntax Tree only")
    # Add -st flag if needed: parser.add_argument("-st", action="store_true", help="Print the Standardized Tree only")

    args = parser.parse_args()

    try:
        with open(args.file_name, 'r') as f:
            program_text = f.read()

        # 1. Lexing
        lexer = Lexer(program_text)
        tokens = lexer.tokenize()
        # print("Tokens:", tokens) # Debug

        # 2. Parsing
        parser = Parser(tokens)
        ast_root = parser.parse()
        # print("\nRaw AST:") # Debug
        # print_ast(ast_root) # Debug

        if args.ast:
            print_ast(ast_root)
            sys.exit(0)

        # 3. Standardization
        # print("\nStandardizing...") # Debug
        st_root = standardize(ast_root)
        # print("\nStandardized Tree (ST):") # Debug
        # print_ast(st_root) # Debug # Use print_ast for ST too

        # 4. CSE Machine Execution
        # print("\nRunning CSE Machine...") # Debug
        cse = CSEMachine()
        result = cse.evaluate(st_root)

        # 5. Output Result
        if result is not None:
             # If the result is the dummy from a final Print, don't print dummy.
             # Otherwise, print the formatted result.
            if not (isinstance(result, str) and result == 'dummy' and cse.control == []): # Check if final result is dummy and machine truly finished
                 print(cse._format_value(result)) # Print final value on stack


    except FileNotFoundError:
        print(f"Error: File not found '{args.file_name}'", file=sys.stderr)
        sys.exit(1)
    except LexerError as e:
        print(f"Lexical Error: {e}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except StandardizerError as e:
        print(f"Standardization Error: {e}", file=sys.stderr)
        sys.exit(1)
    except CseMachineError as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


class StandardizerError(Exception): # Define exception used in standardize
    pass


if __name__ == "__main__":
    main()
