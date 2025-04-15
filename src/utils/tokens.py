from collections import namedtuple

# Token Definition
Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

# Operator remapping (subset, others handled by keywords/grammar)
OPERATOR_MAP = {
    '+': '+', '-': '-', '*': '*', '/': '/', '**': '**', '<': 'ls', '>': 'gr',
    '<=': 'le', '>=': 'ge', '=': '=', '~=': 'ne', '|': 'or', '&': '&',
    '@': '@', '->': '->',
    'aug': 'aug',
    # Note: 'eq', 'ne', 'or', 'and', 'not', 'gr', 'ge', 'ls', 'le' are primarily handled as keywords
    # but can sometimes appear as operators depending on context/lexing.
}

# Basic character sets (used by screener) - Keep definitions close to where used
LETTER = r"[a-zA-Z]"
DIGIT = r"[0-9]"
OPERATOR_SYMBOL = r"[+\-*/<>&.@/:=~|$!#%^_[\]{}\"`?]"
UNDERSCORE = r"_"