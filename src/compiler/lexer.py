import re

# Token specification
token_specification = [
    ('PROGRAM',     r'starterPack'),
    ('PRINT',       r'shoutout'),
    ('IF',          r'smash-pass'),
    ('ELSEIF',      r'maybe'),
    ('ELSE',        r'pass'),
    ('WHILE',       r'grind'),
    ('FOR',         r'yeet'),
    ('FUNCTION',    r'serve'),
    ('TRUE',        r'noCap'),
    ('FALSE',       r'cap'),
    ('NULL',        r'ghosted'),
    ('BREAK',       r'staph'),
    ('COMMENT',     r'~.*'),
    ('NUMBER',      r'\d+(\.\d+)?'),
    ('STRING',      r'"[^"]*"'),
    ('BOOLEAN',     r'(noCap|cap)'),
    ('LPAREN',      r'\('),
    ('RPAREN',      r'\)'),
    ('LBRACE',      r'\{'),
    ('RBRACE',      r'\}'),
    ('SEMICOLON',   r';'),
    ('COMMA',       r','),
    ('IDENTIFIER',  r'[a-zA-Z_]\w*'),
    ('OP',          r'[+\-*/=<>!]+'),
    ('NEWLINE',     r'\n'),
    ('SKIP',        r'[ \t]+'),
    ('MISMATCH',    r'.'),
]


tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        else:
            tokens.append((kind, value, line_num, column))
    return tokens

# Example usage
if __name__ == '__main__':
    code = '''
    starterPack
    shoutout "Hello, Vibe!"
    ~ this is a comment
    serve yeet(x)
    grind noCap
    '''
    for token in tokenize(code):
        print(token)
