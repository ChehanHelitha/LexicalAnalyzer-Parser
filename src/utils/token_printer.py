from typing import List, Optional
from src.utils.tokens import Token


def print_tokens(tokens: Optional[List[Token]]) -> None:
    if tokens is not None:
        for token in tokens:
            print(token)
