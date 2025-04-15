from .node import Node # Use relative import within the package

def print_tree(node, depth=0):
    """Recursively prints the AST or ST in the specified dot-indented format."""
    if not isinstance(node, Node):
        print(f"{'.' * depth}<INVALID NODE: {type(node)} {node!r}>")
        return

    indent = '.' * depth
    node_type = node.type

    # Handle leaf nodes with values
    if node_type in ['ID', 'INT', 'STR']:
        # Format value appropriately
        if node_type == 'STR':
            # Escape special characters for printing if needed, or just show raw
            val_str = node.value # repr(node.value)[1:-1] # Raw string value
        else:
            val_str = str(node.value)
        print(f"{indent}<{node_type}:{val_str}>")
    # Handle simple leaf nodes without explicit values in the grammar output
    elif node_type in ['true', 'false', 'nil', 'dummy', '()']:
         print(f"{indent}<{node_type}>")
    # Handle internal nodes
    else:
        print(f"{indent}{node_type}")
        for child in node.children:
            if child: # Ensure child is not None
                print_tree(child, depth + 1)
            else:
                 print(f"{indent}.<ERROR: None child in {node_type}>")