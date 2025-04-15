from utils.tokens import Token, OPERATOR_MAP # Need Token type and potentially OPERATOR_MAP
from utils.node import Node

class SyntaxError(Exception):
    """Custom exception for parsing errors."""
    pass

class Parser:
    """Parses a stream of tokens into an Abstract Syntax Tree (AST)."""
    def __init__(self, tokens):
        if not tokens:
            raise ValueError("Token stream cannot be empty (must include EOF)")
        self.tokens = tokens
        self.token_index = 0
        # Ensure we don't go past EOF immediately if tokens is just [EOF]
        self.current_token = self.tokens[self.token_index] if self.tokens else None

    def _advance(self):
        """Consumes the current token and moves to the next one."""
        if self.token_index < len(self.tokens) - 1: # Stop at EOF
            self.token_index += 1
            self.current_token = self.tokens[self.token_index]
        elif self.current_token.type != 'EOF':
             # If already at the last token, make sure it's EOF
             self.current_token = self.tokens[-1] # Should be EOF

    def _expect(self, expected_type, expected_value=None):
        """Checks if the current token matches, consumes it, or raises SyntaxError."""
        token = self.current_token
        if not token: # Should not happen if EOF is present
             raise SyntaxError("Unexpected end of input (missing EOF?)")

        # print(f"Expecting {expected_type} ({expected_value}), got {token.type} ({token.value})") # Debug

        match = False
        actual_type = token.type
        actual_value = token.value

        if actual_type == expected_type:
            if expected_value is None or actual_value == expected_value:
                match = True
        # Handle Keywords (lexed as uppercase type) matching lowercase expected value
        elif expected_type == 'KEYWORD' and actual_type.isupper() and actual_type.lower() == expected_value:
            match = True
        # Handle cases where grammar expects OPERATOR but keyword token matches value
        elif expected_type == 'OPERATOR' and actual_type.isupper() and actual_type.lower() in OPERATOR_MAP:
             if expected_value is None or actual_type.lower() == expected_value:
                match = True
                # Return a synthesized OPERATOR token if needed downstream? No, just match.
        # Handle cases where grammar expects OPERATOR but IDENTIFIER matches value (e.g. 'aug')
        elif expected_type == 'OPERATOR' and actual_type == 'IDENTIFIER' and actual_value in OPERATOR_MAP:
             if expected_value is None or actual_value == expected_value:
                 match = True
                 # Return a synthesized OPERATOR token? No, just match.

        if match:
            self._advance()
            return token # Return the consumed token
        else:
            expected_str = f"'{expected_value}'" if expected_value else expected_type
            got_str = f"{token.type}" + (f" '{token.value}'" if token.value is not None else "")
            raise SyntaxError(f"Expected {expected_str} but got {got_str} at line {token.line}, column {token.column}")


    def parse(self):
        """Starts the parsing process."""
        ast = self._parse_E()
        if self.current_token.type != 'EOF':
            # Provide more context if possible
            context_tokens = self.tokens[max(0, self.token_index-2):self.token_index+2]
            context_str = " ".join([f"{t.type}({t.value})" for t in context_tokens])
            raise SyntaxError(f"Unexpected token {self.current_token.type} '{self.current_token.value}' after parsing finished at line {self.current_token.line}. Near: {context_str}")
        return ast

    # --- Grammar Rule Parsing Functions ---
    # E -> 'let' D 'in' E => 'let'
    #   -> 'fn' Vb+ '.' E  => 'lambda'
    #   -> Ew
    def _parse_E(self):
        if self.current_token.type == 'LET': # Keyword type is uppercase
            self._advance()
            d_node = self._parse_D()
            self._expect('KEYWORD', 'in') # Match keyword 'in'
            e_node = self._parse_E()
            return Node('let', children=[d_node, e_node])
        elif self.current_token.type == 'FN':
            self._advance()
            vbs = []
            # Vb starts with IDENTIFIER or L_PAREN
            while self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'L_PAREN':
                vbs.append(self._parse_Vb())
            if not vbs:
                 raise SyntaxError(f"Expected Vb (Identifier or '(') after 'fn' but got {self.current_token.type} at line {self.current_token.line}")
            self._expect('OPERATOR', '.') # Expect the dot operator
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
        nodes = [ta_node] # Start with the first Ta
        while self.current_token.type == 'COMMA':
            self._advance()
            nodes.append(self._parse_Ta())

        if len(nodes) > 1:
             return Node('tau', children=nodes)
        else:
            return ta_node # Return the single Ta node directly

    # Ta -> Ta 'aug' Tc => 'aug'
    #    -> Tc
    def _parse_Ta(self):
        # Left associative: parse Tc first, then loop for 'aug' Tc
        node = self._parse_Tc()
        while self.current_token.type == 'AUG' or \
              (self.current_token.type == 'OPERATOR' and self.current_token.value == 'aug'): # Accept keyword or operator 'aug'
            op_token = self._advance()
            tc_node = self._parse_Tc()
            node = Node('aug', children=[node, tc_node])
        return node

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
        # Left associative
        node = self._parse_Bt()
        while self.current_token.type == 'OR' or \
              (self.current_token.type == 'OPERATOR' and self.current_token.value == 'or'):
             self._advance()
             bt_node = self._parse_Bt()
             node = Node('or', children=[node, bt_node])
        return node


    # Bt -> Bt '&' Bs => '&'
    #    -> Bs
    def _parse_Bt(self):
        # Left associative
        node = self._parse_Bs()
        while self.current_token.type == 'OPERATOR' and self.current_token.value == '&':
             self._advance()
             bs_node = self._parse_Bs()
             node = Node('&', children=[node, bs_node])
        return node

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
        # Map recognized comparison tokens to standard node types
        op_map = {
            'gr': 'gr', '>': 'gr', 'GR': 'gr', # Keyword GR or operator >
            'ge': 'ge', '>=': 'ge', 'GE': 'ge',
            'ls': 'ls', '<': 'ls', 'LS': 'ls',
            'le': 'le', '<=': 'le', 'LE': 'le',
            'eq': 'eq', 'EQ': 'eq', # Keyword EQ or operator = (handled separately?)
            'ne': 'ne', 'NE': 'ne', # Keyword NE or operator ~=
        }
        # Special case for '=' which is assignment in Db, but equality check here?
        # The grammar uses 'eq' explicitly for equality. Let's assume '=' is not used for comparison here.
        # RPAL uses 'eq' and 'ne'. Operators like '>', '<', '>=', '<=' are also valid.

        op_node_type = None
        token_val_or_type = op_token.value if op_token.type == 'OPERATOR' else op_token.type

        if op_token.type == 'OPERATOR' and op_token.value in op_map:
             op_node_type = op_map[op_token.value]
        elif op_token.type.isupper() and op_token.type in op_map: # Check uppercase type
             op_node_type = op_map[op_token.type]


        if op_node_type:
            self._advance() # Consume the operator/keyword
            a2_node = self._parse_A()
            return Node(op_node_type, children=[a_node, a2_node])
        else:
            # Handle 'eq' and 'ne' explicitly if they weren't matched above
            # (They might be keywords EQ, NE)
            if op_token.type == 'EQ':
                 self._advance()
                 a2_node = self._parse_A()
                 return Node('eq', children=[a_node, a2_node])
            elif op_token.type == 'NE':
                 self._advance()
                 a2_node = self._parse_A()
                 return Node('ne', children=[a_node, a2_node])
            else:
                return a_node # No comparison operator found


    # A -> A '+' At => '+'
    #   -> A '-' At => '-'
    #   -> '+' At       => '+' (unary handled implicitly?) or specific node? Grammar unclear. Assume handled by context.
    #   -> '-' At       => 'neg'
    #   -> At
    def _parse_A(self):
         # Handle unary + and - first
         op_type = None
         if self.current_token.type == 'OPERATOR':
              if self.current_token.value == '+':
                   op_type = '+' # Or maybe 'pos' if we need distinct unary plus node
                   self._advance()
              elif self.current_token.value == '-':
                   op_type = 'neg'
                   self._advance()

         # If unary operator was found, parse the operand
         if op_type:
              at_node = self._parse_At()
              if op_type == '+':
                  # Standard practice: unary plus often optimized away unless needed for type coercion
                  return at_node
              else: # op_type == 'neg'
                  return Node(op_type, children=[at_node])

         # No unary operator, parse the first term (At)
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
        # Left associative
        node = self._parse_Af()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ['*', '/']:
             op = self.current_token.value
             self._advance()
             af_node = self._parse_Af()
             node = Node(op, children=[node, af_node])
        return node

    # Af -> Ap '**' Af => '**'
    #    -> Ap
    def _parse_Af(self):
        # Right associative: If we see '**', parse the rest of Af recursively first
        ap_node = self._parse_Ap()
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '**':
            self._advance()
            af_node = self._parse_Af() # Recursive call for right operand
            return Node('**', children=[ap_node, af_node])
        else:
            return ap_node

    # Ap -> Ap '@' '<IDENTIFIER>' R => '@'
    #    -> R
    def _parse_Ap(self):
         # Left associative
         node = self._parse_R()
         while self.current_token.type == 'OPERATOR' and self.current_token.value == '@':
             self._advance()
             id_token = self._expect('IDENTIFIER') # Expect the specific ID token
             id_node = Node('ID', value=id_token.value)
             r_node = self._parse_R()
             node = Node('@', children=[node, id_node, r_node])
         return node

    # R -> R Rn => 'gamma' (Function application)
    #   -> Rn
    def _parse_R(self):
        # Left associative function application ('gamma')
        node = self._parse_Rn()
        # Check if the *next* token can start an Rn (operand)
        while self.current_token.type in ['IDENTIFIER', 'INTEGER', 'STRING', 'L_PAREN'] or \
              self.current_token.type in ['TRUE', 'FALSE', 'NIL', 'DUMMY']: # Check uppercase keyword types
            rn_node = self._parse_Rn()
            node = Node('gamma', children=[node, rn_node])
        return node

    # Rn -> '<IDENTIFIER>' | '<INTEGER>' | '<STRING>'
    #    -> 'true' | 'false' | 'nil' | 'dummy'
    #    -> '(' E ')'
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
            return Node('true') # Node type matches the keyword
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
            # Parentheses just group, return the inner expression node directly
            # No separate 'paren' node needed in AST typically
            return e_node
        else:
             # Provide helpful error message
             expected_options = "Identifier, Integer, String, Keyword (true, false, nil, dummy), or '('"
             raise SyntaxError(f"Unexpected token {token.type} '{token.value}' in expression operand (Rn). Expected {expected_options} at line {token.line}")


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
        nodes = [dr_node]
        while self.current_token.type == 'AND':
             self._advance()
             nodes.append(self._parse_Dr())

        if len(nodes) > 1:
            return Node('and', children=nodes)
        else:
            return dr_node # Return single Dr node

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
            return d_node # Parentheses group definitions

        # Need to distinguish between Vl=E and ID Vb+=E
        # If it starts with ID, peek ahead.
        if self.current_token.type == 'IDENTIFIER':
            # Peek at the next token without consuming
            if self.token_index + 1 < len(self.tokens):
                next_token = self.tokens[self.token_index + 1]
                # If next token starts a Vb (ID or '(') or is '=', it *could* be fcn_form or Vl=E.
                # If next token starts a Vb, it MUST be fcn_form.
                if next_token.type == 'IDENTIFIER' or next_token.type == 'L_PAREN':
                     # Definitely function form
                     id_token = self._expect('IDENTIFIER') # Consume ID
                     func_name_node = Node('ID', value=id_token.value)
                     vbs = []
                     while self.current_token.type == 'IDENTIFIER' or self.current_token.type == 'L_PAREN':
                         vbs.append(self._parse_Vb())
                     if not vbs: # Grammar says Vb+ (at least one)
                         raise SyntaxError(f"Expected parameters (Vb) after function name '{id_token.value}' in function definition at line {id_token.line}")
                     self._expect('OPERATOR', '=')
                     e_node = self._parse_E()
                     return Node('function_form', children=[func_name_node] + vbs + [e_node])
                # If next token is '=', it's Vl = E where Vl is a single identifier
                elif next_token.type == 'OPERATOR' and next_token.value == '=':
                     vl_node = self._parse_Vl() # Parses the single ID
                     self._expect('OPERATOR', '=')
                     e_node = self._parse_E()
                     return Node('=', children=[vl_node, e_node])
                # If next token is ',', it's Vl starting with ID, ... = E
                elif next_token.type == 'COMMA':
                     vl_node = self._parse_Vl() # Parses ID list
                     self._expect('OPERATOR', '=')
                     e_node = self._parse_E()
                     return Node('=', children=[vl_node, e_node])
                else:
                      # If ID is followed by something else then '=', it must be Vl=E with Vl=ID
                      vl_node = self._parse_Vl() # Parses the single ID
                      self._expect('OPERATOR', '=')
                      e_node = self._parse_E()
                      return Node('=', children=[vl_node, e_node])
            else: # Identifier followed by EOF? Should be handled by EOF check later. Treat as Vl=E.
                 vl_node = self._parse_Vl()
                 self._expect('OPERATOR', '=')
                 e_node = self._parse_E()
                 return Node('=', children=[vl_node, e_node])
        else:
            # Does not start with ID, must be '(' D ')' which was handled,
            # or potentially an error if Vl must start with ID?
            # Grammar for Vl implies it starts with ID. If we get here, it's likely an error.
            # Let's assume Vl must start with ID or '('. The '(' case for Vl is handled in _parse_Vb.
            # So, if not L_PAREN and not IDENTIFIER, what could Db be?
            # Re-check Db: -> Vl = E | ID Vb+ = E | ( D )
            # It seems Db *must* start with L_PAREN or IDENTIFIER.
            # Let's try parsing Vl directly if it wasn't function form.
            try:
                 vl_node = self._parse_Vl()
                 self._expect('OPERATOR', '=')
                 e_node = self._parse_E()
                 return Node('=', children=[vl_node, e_node])
            except SyntaxError as e:
                 # Raise a more specific error if parsing Vl failed here
                 raise SyntaxError(f"Invalid definition (Db). Expected identifier, function form, or parenthesized definition. Got {self.current_token.type} near line {self.current_token.line}. Original error: {e}") from e


    # Vb -> '<IDENTIFIER>'
    #    -> '(' Vl ')'
    #    -> '(' ')' => '()'
    def _parse_Vb(self):
        if self.current_token.type == 'IDENTIFIER':
            id_token = self._advance()
            return Node('ID', value=id_token.value)
        elif self.current_token.type == 'L_PAREN':
            self._advance()
            if self.current_token.type == 'R_PAREN': # Special case for () parameter list
                self._advance()
                return Node('()') # Specific node type for empty tuple pattern
            else:
                # If not empty parens, it must contain Vl
                vl_node = self._parse_Vl()
                self._expect('R_PAREN')
                # Vl could be a single ID or a ',' node. Return it directly.
                return vl_node # Return the Vl node (ID or , list)
        else:
             raise SyntaxError(f"Expected IDENTIFIER or '(' for variable binding (Vb) but got {self.current_token.type} at line {self.current_token.line}")

    # Vl -> '<IDENTIFIER>' list ',' => ','?
    # Simplified: Parses one or more comma-separated identifiers.
    # Returns a single ID node if only one, or a ',' node if multiple.
    def _parse_Vl(self):
        # Vl must start with an identifier according to the simplified view
        # based on Db rules analysis.
        if self.current_token.type != 'IDENTIFIER':
            raise SyntaxError(f"Expected IDENTIFIER for variable list (Vl) but got {self.current_token.type} at line {self.current_token.line}")

        ids = []
        # Loop to parse 'ID , ID , ... , ID'
        while True:
            id_token = self._expect('IDENTIFIER')
            ids.append(Node('ID', value=id_token.value))
            # Check for a following comma
            if self.current_token.type == 'COMMA':
                self._advance() # Consume comma, expect another ID
                if self.current_token.type != 'IDENTIFIER':
                     raise SyntaxError(f"Expected IDENTIFIER after ',' in variable list (Vl) but got {self.current_token.type} at line {self.current_token.line}")
            else:
                break # No more commas, list ends

        if len(ids) == 1:
            return ids[0] # Return the single ID node
        else:
            # Use ',' node type to represent the list/tuple pattern
            return Node(',', children=ids)