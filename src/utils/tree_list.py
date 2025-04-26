def list_tree(tree):
    ast = []

    def dfs(root, depth):
        ast.append("." * depth + root.data + " ")

        for child in root.children:
            dfs(child, depth + 1)

    dfs(tree, 0)

    return ast
