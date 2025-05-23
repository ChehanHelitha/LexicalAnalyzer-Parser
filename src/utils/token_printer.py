def print_tokens(tokens):
    """Prints a list of tokens, one per line (for debugging)."""
    print("--- Tokens ---")
    if not tokens:
        print("(No tokens)")
        return
    max_type_len = max(len(t.type) for t in tokens)
    for token in tokens:
        val_str = f"'{token.value}'" if isinstance(token.value, str) else str(token.value)
        print(f"L{token.line:<3} C{token.column:<3} {token.type:<{max_type_len}} : {val_str}")
    print("--------------")