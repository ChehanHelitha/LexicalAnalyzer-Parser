# cse_machine.py
import sys
from utils.node import Node # Base Node class

# --- CSE Value Types ---
class Closure:
    def __init__(self, env_idx, variables, body):
        self.env_idx = env_idx # Index into the environment list E
        self.variables = variables # List of formal parameter ID Nodes
        self.body = body # Node representing the function body
        self.recursive_marker = None # For Y* / eta

    def __repr__(self):
        var_names = [v.value for v in self.variables]
        marker = "*" if self.recursive_marker else ""
        return f"Closure{marker}(env={self.env_idx}, vars={var_names})"

class TupleValue:
    def __init__(self, values):
        self.values = values # List of actual CSE values

    def __repr__(self):
        return f"Tuple({self.values!r})"

# Environment marker object for CSE Control Stack
class EnvMarker:
    def __init__(self, index):
        self.index = index # index in E list (index to restore)
    def __repr__(self):
        return f"EnvMarker(restore_idx={self.index})"

# Primitive function marker for CSE Stack/Lookup
class PrimitiveFunction:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Prim({self.name})"

# Y* marker object for CSE Stack
class YStar:
    def __repr__(self):
        return "Y*"

# Special object for eta-abstractions (recursive closures marker)
ETA = object()

# --- CSE Error ---
class CseMachineError(Exception):
    """Custom exception for errors during CSE machine execution."""
    pass


# --- CSE Machine Class ---
class CSEMachine:
    """Implements the Control-Stack-Environment (CSE) execution model."""
    def __init__(self):
        self.control = []
        self.stack = []
        self.environments = [[]]
        self.current_env_idx = 0
        self._populate_builtins()

    def _populate_builtins(self):
        # (Content identical to the _populate_builtins method in the previous version)
        builtins = {
            # IO
            "Print": PrimitiveFunction("Print"),
            # Type checking
            "Isinteger": PrimitiveFunction("Isinteger"), "Istruthvalue": PrimitiveFunction("Istruthvalue"),
            "Isstring": PrimitiveFunction("Isstring"), "Istuple": PrimitiveFunction("Istuple"),
            "Isdummy": PrimitiveFunction("Isdummy"), "Isfunction": PrimitiveFunction("Isfunction"),
            # String
            "Stem": PrimitiveFunction("Stem"), "Stern": PrimitiveFunction("Stern"), "Conc": PrimitiveFunction("Conc"),
            # Tuple
            "Order": PrimitiveFunction("Order"),
            # System
            "stop": PrimitiveFunction("stop"),
            # Operators / Other built-ins
            "+": PrimitiveFunction("+"), "-": PrimitiveFunction("-"), "*": PrimitiveFunction("*"),
            "/": PrimitiveFunction("/"), "**": PrimitiveFunction("**"), "or": PrimitiveFunction("or"),
            "&": PrimitiveFunction("&"), "not": PrimitiveFunction("not"), "eq": PrimitiveFunction("eq"),
            "ne": PrimitiveFunction("ne"), "ls": PrimitiveFunction("ls"), "le": PrimitiveFunction("le"),
            "gr": PrimitiveFunction("gr"), "ge": PrimitiveFunction("ge"), "neg": PrimitiveFunction("neg"),
            "aug": PrimitiveFunction("aug"),
        }
        for name, func in builtins.items():
             self.environments[0].append((name, func))

    def _lookup(self, name, env_idx):
        # (Content identical to the _lookup method in the previous version)
        current_lookup_idx = env_idx
        visited_indices = set()
        while current_lookup_idx is not None:
            if current_lookup_idx in visited_indices: raise CseMachineError(f"Env loop for '{name}'")
            visited_indices.add(current_lookup_idx)
            if not (0 <= current_lookup_idx < len(self.environments)): raise CseMachineError(f"Invalid env index {current_lookup_idx}")

            env_frame = self.environments[current_lookup_idx]
            for var_name, value in reversed(env_frame):
                if var_name == name:
                    if isinstance(value, Closure) and value.recursive_marker is ETA: return value # Return marked closure
                    else: return value

            parent_idx = None
            if current_lookup_idx > 0:
                 if env_frame and isinstance(env_frame[0], int): parent_idx = env_frame[0]
                 else: raise CseMachineError(f"Env {current_lookup_idx} missing parent index.")
            current_lookup_idx = parent_idx
        raise CseMachineError(f"Unbound variable '{name}' from env {env_idx}")


    def _apply_primitive(self, prim_func, actual_param):
        # (Content identical to the _apply_primitive method in the previous version)
        name = prim_func.name
        try:
            # Unary Ops
            if name == "Isinteger": self.stack.append(isinstance(actual_param, int))
            elif name == "Istruthvalue": self.stack.append(isinstance(actual_param, bool))
            elif name == "Isstring": self.stack.append(isinstance(actual_param, str))
            elif name == "Istuple": self.stack.append(isinstance(actual_param, TupleValue))
            elif name == "Isdummy": self.stack.append(isinstance(actual_param, str) and actual_param == 'dummy')
            elif name == "Isfunction": self.stack.append(isinstance(actual_param, Closure))
            elif name == "Stem": self.stack.append(actual_param[0] if isinstance(actual_param, str) and actual_param else "")
            elif name == "Stern": self.stack.append(actual_param[1:] if isinstance(actual_param, str) and len(actual_param)>0 else "")
            elif name == "Order": self.stack.append(len(actual_param.values) if isinstance(actual_param, TupleValue) else (_ for _ in ()).throw(CseMachineError("TypeError: Order expects tuple")))
            elif name == "Print": print(self._format_value(actual_param), end=''); self.stack.append('dummy')
            elif name == "stop": self.control = []
            elif name == 'neg': self.stack.append(-actual_param if isinstance(actual_param, int) else (_ for _ in ()).throw(CseMachineError("TypeError: neg expects integer")))
            elif name == 'not': self.stack.append(not actual_param if isinstance(actual_param, bool) else (_ for _ in ()).throw(CseMachineError("TypeError: not expects boolean")))
            # Binary Ops
            elif name in ['+', '-', '*', '/', '**', 'eq', 'ne', 'ls', 'le', 'gr', 'ge', 'or', '&', 'Conc', 'aug']:
                 val2 = actual_param
                 if not self.stack: raise CseMachineError(f"Stack underflow for '{name}'")
                 val1 = self.stack.pop()
                 result = None
                 if name == '+': result = val1 + val2 if isinstance(val1, int) and isinstance(val2, int) else (_ for _ in ()).throw(CseMachineError("TypeError: '+' requires integers"))
                 elif name == '-': result = val1 - val2 if isinstance(val1, int) and isinstance(val2, int) else (_ for _ in ()).throw(CseMachineError("TypeError: '-' requires integers"))
                 elif name == '*': result = val1 * val2 if isinstance(val1, int) and isinstance(val2, int) else (_ for _ in ()).throw(CseMachineError("TypeError: '*' requires integers"))
                 elif name == '/':
                     if not isinstance(val1, int) or not isinstance(val2, int): raise CseMachineError("TypeError: '/' requires integers")
                     if val2 == 0: raise CseMachineError("RuntimeError: Division by zero")
                     result = val1 // val2
                 elif name == '**': result = val1 ** val2 if isinstance(val1, int) and isinstance(val2, int) else (_ for _ in ()).throw(CseMachineError("TypeError: '**' requires integers"))
                 elif name == 'eq': result = val1 == val2
                 elif name == 'ne': result = val1 != val2
                 elif name == 'ls': result = val1 < val2
                 elif name == 'le': result = val1 <= val2
                 elif name == 'gr': result = val1 > val2
                 elif name == 'ge': result = val1 >= val2
                 elif name == 'or': result = val1 or val2 if isinstance(val1, bool) and isinstance(val2, bool) else (_ for _ in ()).throw(CseMachineError("TypeError: 'or' requires booleans"))
                 elif name == '&': result = val1 and val2 if isinstance(val1, bool) and isinstance(val2, bool) else (_ for _ in ()).throw(CseMachineError("TypeError: '&' requires booleans"))
                 elif name == 'Conc': result = val1 + val2 if isinstance(val1, str) and isinstance(val2, str) else (_ for _ in ()).throw(CseMachineError("TypeError: Conc requires strings"))
                 elif name == 'aug':
                    if not isinstance(val1, TupleValue) or not isinstance(val2, TupleValue): raise CseMachineError(f"TypeError: aug expects two tuples, got {type(val1)} and {type(val2)}")
                    result = TupleValue(val1.values + val2.values)
                 self.stack.append(result)
            else: raise CseMachineError(f"Unimplemented primitive '{name}'")
        except TypeError as e: raise CseMachineError(f"RuntimeError applying '{name}': {e}") from e
        except CseMachineError: raise # Re-raise specific CSE errors
        except Exception as e: raise CseMachineError(f"Unexpected error applying '{name}': {e}") from e


    def _format_value(self, value):
        # (Content identical to the _format_value method in the previous version)
        if isinstance(value, str): return value.replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n').replace("'", "\\'")
        elif isinstance(value, bool): return str(value).lower()
        elif isinstance(value, Closure):
             vars_str = ", ".join(v.value for v in value.variables); marker = "*" if value.recursive_marker else ""
             return f"[closure{marker}: env={value.env_idx}, vars=({vars_str})]"
        elif isinstance(value, TupleValue): return "(" + ", ".join(self._format_value(v) for v in value.values) + ")"
        elif value is None: return "nil"
        elif value == 'dummy': return "dummy"
        elif isinstance(value, int): return str(value)
        elif isinstance(value, PrimitiveFunction): return f"[primitive:{value.name}]"
        elif isinstance(value, YStar): return "[Y*]"
        else: return repr(value)


    def evaluate(self, st_root):
        # (Content identical to the evaluate method in the previous version,
        # using the classes/methods defined within this file/class)
        if not isinstance(st_root, Node): return None

        self.control = [st_root]
        self.stack = []
        self.environments = [list(self.environments[0])] # Reset with copy of global
        self.current_env_idx = 0
        MAX_STEPS = 10000
        steps = 0

        while self.control and steps < MAX_STEPS:
            steps += 1
            # DEBUG: print(f"S{steps} C:{self.control[-1] if self.control else '[]'} S:{self.stack}")
            ctrl_item = self.control.pop()

            # Process Node
            if isinstance(ctrl_item, Node):
                node = ctrl_item; node_type = node.type
                if node_type == 'INT': self.stack.append(node.value)
                elif node_type == 'STR': self.stack.append(node.value)
                elif node_type == 'true': self.stack.append(True)
                elif node_type == 'false': self.stack.append(False)
                elif node_type == 'nil': self.stack.append(None)
                elif node_type == 'dummy': self.stack.append('dummy')
                elif node_type == '()': self.stack.append(TupleValue([]))
                elif node_type == 'ID': self.stack.append(self._lookup(node.value, self.current_env_idx))
                elif node_type == 'lambda':
                    if not node.children: raise CseMachineError("Lambda node has no children")
                    vars = node.children[:-1]; body = node.children[-1]
                    for v in vars:
                        if not isinstance(v, Node) or v.type != 'ID': raise CseMachineError(f"Invalid lambda param: {v}")
                    self.stack.append(Closure(self.current_env_idx, vars, body))
                elif node_type == '->':
                    if len(node.children)!=3: raise CseMachineError("Conditional needs 3 children")
                    cond,then,els = node.children; self.control.extend(['beta',els,then,cond])
                elif node_type == 'gamma':
                    if len(node.children)!=2: raise CseMachineError("Gamma needs 2 children")
                    rator,rand = node.children; self.control.extend(['gamma',rand,rator])
                elif node_type == 'tau':
                    n=len(node.children); self.control.append(('tau',n)); self.control.extend(reversed(node.children))
                elif node_type == 'Y*': self.stack.append(YStar())
                else: raise CseMachineError(f"Unexpected Node '{node_type}' on control stack.")

            # Process String Marker
            elif isinstance(ctrl_item, str):
                marker = ctrl_item
                if marker == 'gamma':
                    if not self.stack: raise CseMachineError("Stack empty: missing Rand for gamma")
                    rand = self.stack.pop();
                    if not self.stack: raise CseMachineError("Stack empty: missing Rator for gamma")
                    rator = self.stack.pop()

                    if isinstance(rator, Closure): # Rule 5
                        closure = rator
                        if closure.recursive_marker is ETA: # Handle Y* result
                           if len(closure.variables) != 1: raise CseMachineError("Y* closure needs 1 var")
                           rec_name = closure.variables[0].value; eta_env_idx = closure.env_idx
                           if not (0 <= eta_env_idx < len(self.environments)): raise CseMachineError(f"Invalid ETA env index {eta_env_idx}")
                           # Bind name to closure itself in captured env
                           self.environments[eta_env_idx].append((rec_name, closure))
                           closure.recursive_marker = None # Bound now

                        new_env_idx = len(self.environments); parent_env_idx = closure.env_idx
                        new_env_frame = [parent_env_idx] # Link to parent
                        self.environments.append(new_env_frame)

                        if len(closure.variables) == 1: new_env_frame.append((closure.variables[0].value, rand))
                        elif len(closure.variables) > 1:
                            if not isinstance(rand, TupleValue): raise CseMachineError(f"Func expected tuple arg, got {type(rand)}")
                            if len(rand.values) != len(closure.variables): raise CseMachineError(f"Arg count mismatch: got {len(rand.values)}, expected {len(closure.variables)}")
                            for i, var in enumerate(closure.variables): new_env_frame.append((var.value, rand.values[i]))
                        elif len(closure.variables) == 0:
                            if not isinstance(rand, TupleValue) or rand.values: raise CseMachineError("Func with no params called with args")

                        self.control.append(EnvMarker(self.current_env_idx)) # Save caller env index
                        self.control.append(closure.body)
                        self.current_env_idx = new_env_idx # Switch to new env

                    elif isinstance(rator, PrimitiveFunction): self._apply_primitive(rator, rand) # Rule 6
                    elif isinstance(rator, TupleValue): # Rule 12
                        if not isinstance(rand, int): raise CseMachineError("Tuple index must be integer")
                        idx = rand
                        if not (1 <= idx <= len(rator.values)): raise CseMachineError(f"Tuple index {idx} out of bounds (size {len(rator.values)})")
                        self.stack.append(rator.values[idx-1])
                    elif isinstance(rator, YStar): # Y* application
                        if not isinstance(rand, Closure): raise CseMachineError("Y* expects a closure")
                        rand.recursive_marker = ETA; self.stack.append(rand) # Mark and push back
                    else: raise CseMachineError(f"Cannot apply non-callable type: {type(rator)}")

                elif marker == 'beta': # Rule 10 cont.
                    if not self.stack: raise CseMachineError("Stack empty for beta cond")
                    cond_val = self.stack.pop();
                    if not isinstance(cond_val, bool): raise CseMachineError(f"Cond expected bool, got {type(cond_val)}")
                    if not self.control or not self.control: raise CseMachineError("Control stack missing branches for beta")
                    els = self.control.pop(); thn = self.control.pop();
                    self.control.append(thn if cond_val else els)

            # Process Tuple Marker
            elif isinstance(ctrl_item, tuple) and ctrl_item[0] == 'tau': # Rule 13 cont.
                _, arity = ctrl_item
                if len(self.stack) < arity: raise CseMachineError(f"Stack underflow for tau (need {arity})")
                vals = [self.stack.pop() for _ in range(arity)]
                self.stack.append(TupleValue(list(reversed(vals))))

            # Process Env Marker
            elif isinstance(ctrl_item, EnvMarker): # Rule 5 cont.
                self.current_env_idx = ctrl_item.index # Restore caller env

            else: raise CseMachineError(f"Unknown control item type: {type(ctrl_item)}")

        # Final result handling
        if steps >= MAX_STEPS:
             print(f"\nError: CSE Max steps ({MAX_STEPS}) exceeded.", file=sys.stderr)
             return None
        if len(self.stack) == 1: return self.stack[0]
        elif len(self.stack) == 0:
             if self.control == []: print("\nWarning: CSE finished with empty stack.", file=sys.stderr) # Empty stack ok if stop was used
             return None
        else:
             print(f"\nWarning: CSE finished with multiple values on stack: {self.stack}", file=sys.stderr)
             return self.stack[-1] # Return top value?