# build_standard_tree.py
from utils.node import Node
# Import YStar and ETA from where they are now defined
from cse_machine import YStar, ETA

class StandardizerError(Exception):
    """Custom exception for errors during AST standardization."""
    pass

# --- extract_vars function ---
# (Content identical to the extract_vars function in the previous version)
def extract_vars(d_node):
    if not isinstance(d_node, Node): raise StandardizerError(f"Cannot extract vars from non-Node: {d_node!r}")
    if d_node.type == '=':
        vl_node = d_node.children[0]
        if vl_node.type == ',': return vl_node.children
        elif vl_node.type == 'ID': return [vl_node]
        else: raise StandardizerError(f"Unexpected LHS in '=' for var extraction: {vl_node.type}")
    elif d_node.type == 'tau':
        vars_list = []
        for child_def_node in d_node.children: vars_list.extend(extract_vars(child_def_node))
        return vars_list
    else: raise StandardizerError(f"Cannot extract vars from standardized def node '{d_node.type}'")


# --- standardize function ---
# (Content identical to the standardize function in the previous version,
#  it already uses YStar and ETA correctly, imports are now fixed)
def standardize(node):
    if not isinstance(node, Node): return node
    std_children = [standardize(child) for child in node.children]
    node_type = node.type

    if node_type == 'let':
        if len(std_children) != 2: raise StandardizerError("let needs 2 children")
        d_std, e_std = std_children; variables = extract_vars(d_std)
        if not variables: raise StandardizerError("No vars in 'let' def")
        lambda_node = Node('lambda', children=variables + [e_std])
        return Node('gamma', children=[lambda_node, d_std])
    elif node_type == 'where':
        if len(std_children) != 2: raise StandardizerError("where needs 2 children")
        e_std, dr_std = std_children; variables = extract_vars(dr_std)
        if not variables: raise StandardizerError("No vars in 'where' def")
        lambda_node = Node('lambda', children=variables + [e_std])
        return Node('gamma', children=[lambda_node, dr_std])
    elif node_type == 'function_form':
        if len(std_children) < 2: raise StandardizerError("fcn_form needs P and E")
        p_node, *vbs, e_std = std_children; flat_vbs = []
        for vb in vbs:
            if vb.type == ',': flat_vbs.extend(vb.children)
            elif vb.type == '()': pass
            elif vb.type == 'ID': flat_vbs.append(vb)
            else: raise StandardizerError(f"Unexpected node type in fcn_form params: {vb.type}")
        current_e = e_std
        for vb_id in reversed(flat_vbs): current_e = Node('lambda', children=[vb_id, current_e])
        return Node('=', children=[p_node, current_e])
    elif node_type == 'lambda':
        if len(std_children) < 1: raise StandardizerError("lambda needs body E")
        *vbs, e_std = std_children; flat_vbs = []
        for vb in vbs:
            if vb.type == ',': flat_vbs.extend(vb.children)
            elif vb.type == '()': pass
            elif vb.type == 'ID': flat_vbs.append(vb)
            else: raise StandardizerError(f"Unexpected node type in lambda params: {vb.type}")
        current_e = e_std
        for vb_id in reversed(flat_vbs): current_e = Node('lambda', children=[vb_id, current_e])
        return current_e
    elif node_type == 'within':
        if len(std_children) != 2: raise StandardizerError("within needs 2 children")
        d1_std, d2_std = std_children; vars2 = extract_vars(d2_std)
        if not vars2: raise StandardizerError("No vars in 'within' outer def (D2)")
        lambda_node = Node('lambda', children=vars2 + [d1_std])
        return Node('gamma', children=[lambda_node, d2_std])
    elif node_type == 'and': return Node('tau', children=std_children)
    elif node_type == 'rec':
        if len(std_children) != 1: raise StandardizerError("rec needs 1 child (Db)")
        db_std = std_children[0]
        if not isinstance(db_std, Node) or db_std.type != '=': raise StandardizerError(f"'rec' child must standardize to '=', got {type(db_std)}{':'+db_std.type if isinstance(db_std, Node) else ''}")
        if len(db_std.children) != 2: raise StandardizerError("'=' in 'rec' needs P and E")
        p_node, e_std = db_std.children
        if not isinstance(p_node, Node) or p_node.type != 'ID': raise StandardizerError(f"'rec' only supports single var recursion (got {p_node.type})")
        lambda_node = Node('lambda', children=[p_node, e_std])
        ystar_node = Node('Y*') # Using YStar imported from cse_machine
        gamma_node = Node('gamma', children=[ystar_node, lambda_node])
        return Node('=', children=[p_node, gamma_node])
    elif node_type == '@':
        if len(std_children) != 3: raise StandardizerError("@ needs 3 children")
        ap_std, id_node, r_std = std_children
        if not isinstance(id_node, Node) or id_node.type != 'ID': raise StandardizerError(f"Expected ID node as 2nd child of @, got {id_node.type}")
        inner_gamma = Node('gamma', children=[ap_std, id_node])
        return Node('gamma', children=[inner_gamma, r_std])
    else:
        return Node(node_type, value=node.value, children=std_children)

# (Keep the __main__ block for direct testing if desired)