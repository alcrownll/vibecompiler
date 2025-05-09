import re
from typing import List, Tuple, Optional, Any, TYPE_CHECKING
from .errors import SyntaxError as VibeSyntaxError

if TYPE_CHECKING:
    from .lexer import Token

class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"

class Lexer:
    def __init__(self):
        self.tokens = [
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
            ('INTEGER_TYPE', r'clout'),
            ('FLOAT_TYPE',   r'ratio'),
            ('STRING_TYPE',  r'tea'),        
            ('BOOLEAN_TYPE', r'mood'),
            ('ARRAY_TYPE',   r'gang'),
            ('DICT_TYPE',    r'wiki'),
            
            # Constants
            ('TRUE',        r'noCap'),
            ('FALSE',       r'cap'),
            ('NULL',        r'ghosted'),
            
            # Other functions
            ('TYPEOF',      r'itsGiving'),
            ('INPUT',       r'spillTheTea'),
            ('SWITCH',      r'chooseYourFighter'),
            ('TRY',         r'tryhard'),
            ('CATCH',       r'flopped'),
            
            # Literals
            ('NUMBER',      r'\d+(\.\d+)?'),
            ('STRING',      r'"([^"\\]|\\.)*"'),
            
            # Symbols
            ('LPAREN',      r'\('),
            ('RPAREN',      r'\)'),
            ('LBRACE',      r'\{'),
            ('RBRACE',      r'\}'),
            ('LBRACKET',    r'\['),
            ('RBRACKET',    r'\]'),
            ('SEMICOLON',   r';'),
            ('COMMA',       r','),
            ('DOT',         r'\.'),
            ('COLON',       r':'),
            
            # Operators
            ('OP',          r'[+\-*/=<>!&|]+'),
            
            # Misc
            ('IDENTIFIER',  r'[a-zA-Z_]\w*'),
            ('COMMENT',     r'[ \t]*~[^\r\n]*'),
            ('BLOCK_COMMENT', r'~\*[\s\S]*?\*~'),
            ('NEWLINE',     r'\r?\n'),
            ('SKIP',        r'[ \t]+'),
            ('MISMATCH',    r'.'),
        ]
        
        # Combine all token patterns into a single regex
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.tokens)
        self.token_pattern = re.compile(self.token_regex, re.DOTALL)

    def tokenize(self, code: str) -> List[Token]:
        tokens = []
        line_num = 1
        line_start = 0
        
        for match in self.token_pattern.finditer(code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1
            
            if kind == 'NEWLINE':
                line_start = match.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'COMMENT':
                continue
            elif kind == 'BLOCK_COMMENT':
                continue
            elif kind == 'MISMATCH':
                raise VibeSyntaxError(f'Unexpected character {value}', line_num, column)
            
            tokens.append(Token(kind, value, line_num, column))
            
        for t in tokens:
            print(t)
        return tokens 