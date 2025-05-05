import re

# Token specification
token_specification = [
    # Core keywords
    ('PROGRAM',     r'starterPack'),
    ('PRINT',       r'shoutout'),
    ('IF',          r'smash'),        
    ('ELSEIF',      r'maybe'),
    ('ELSE',        r'pass'),
    ('WHILE',       r'grind'),
    ('FOR',         r'yeet'),
    ('FUNCTION',    r'serve'),
    ('BREAK',       r'staph'),
    
    # Data types
    ('INTEGER_TYPE', r'clout'),      # Integer type
    ('FLOAT_TYPE',   r'ratio'),      # Float type
    ('STRING_TYPE',  r'tea'),        # String type
    ('BOOLEAN_TYPE', r'mood'),       # Boolean type
    ('ARRAY_TYPE',   r'gang'),       # Array/List type
    ('DICT_TYPE',    r'wiki'),       # Dictionary type
    
    # Constants
    ('TRUE',        r'noCap'),
    ('FALSE',       r'cap'),
    ('NULL',        r'ghosted'),
    
    # Other functions
    ('TYPEOF',      r'itsGiving'),
    ('INPUT',       r'spillTheTea'),
    ('SWITCH',      r'chooseYourFighter'),
    ('TRY',         r'tryhard-flopped'),
    ('CATCH',       r'flopped'),
    
    # Literals
    ('NUMBER',      r'\d+(\.\d+)?'),
    ('STRING',      r'"([^"\\]|\\.)*"'),  # Updated to handle escaped quotes
    
    # Symbols
    ('LPAREN',      r'\('),
    ('RPAREN',      r'\)'),
    ('LBRACE',      r'\{'),
    ('RBRACE',      r'\}'),
    ('LBRACKET',    r'\['),          # Added for array literals
    ('RBRACKET',    r'\]'),          # Added for array literals
    ('SEMICOLON',   r';'),
    ('COMMA',       r','),
    ('DOT',         r'\.'),          # Added for object property access
    ('COLON',       r':'),           # Added for dictionary key-value pairs
    
    # Operators
    ('OP',          r'[+\-*/=<>!&|]+'),
    
    # Misc
    ('IDENTIFIER',  r'[a-zA-Z_]\w*'),
    ('COMMENT',     r'~.*'),
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
    starterPack {
        shoutout("Hello, Vibe!")
        ~ This is a comment
        
        ~ Data type examples
        clout myInt = 42
        ratio myFloat = 3.14
        tea myString = "This is a string"
        mood myBool = noCap
        gang myArray = [1, 2, 3]
        
        ~ Control structure examples
        smash(myBool) {
            shoutout("This is true!")
        } pass {
            shoutout("This is false!")
        }
        
        grind(myInt > 0) {
            myInt = myInt - 1
            shoutout("Counting down: " + myInt)
        }
        
        yeet(let i = 0; i < 5; i++) {
            shoutout("Loop index: " + i)
        }
        
        serve addNumbers(a, b) {
            return a + b
        }
    }
    '''
    for token in tokenize(code):
        print(token)