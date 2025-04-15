# Set of reserved keywords in RPAL
KEYWORDS = {
    'let', 'in', 'fn', 'where', 'aug', 'or', '&', 'not', 'gr', 'ge', 'ls',
    'le', 'eq', 'ne', 'within', 'and', 'rec', 'true', 'false', 'nil', 'dummy'
}

# Keywords that can also be lexed as operators (for reference)
OPERATOR_KEYWORDS = {'aug', 'or', '&', 'gr', 'ge', 'ls', 'le', 'eq', 'ne'}