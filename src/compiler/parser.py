import sys
from lexer import tokenize

class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children else []

    def __repr__(self):
        return f"ASTNode({self.node_type}, {self.value}, {self.children})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def match(self, expected_type):
        tok_type, tok_value = self.current_token()
        if tok_type == expected_type:
            self.pos += 1
            return tok_value
        else:
            raise SyntaxError(f"Expected {expected_type} but found {tok_type} at position {self.pos}")

    def parse(self):
        return self.program()

    def program(self):
        self.match('STARTERPACK')  # matches 'starterPack'
        statements = []
        while self.current_token()[0] != 'EOF':
            statements.append(self.statement())
        return ASTNode('Program', children=statements)

    def statement(self):
        tok_type, _ = self.current_token()
        if tok_type == 'IDENTIFIER':
            return self.assignment()
        elif tok_type == 'SHOUTOUT':
            return self.print_statement()
        else:
            raise SyntaxError(f"Unexpected token {tok_type} at position {self.pos}")

    def assignment(self):
        identifier = self.match('IDENTIFIER')
        self.match('ASSIGN')
        expr = self.expression()
        return ASTNode('Assignment', value=identifier, children=[expr])

    def print_statement(self):
        self.match('SHOUTOUT')
        self.match('LPAREN')
        expr = self.expression()
        self.match('RPAREN')
        return ASTNode('Print', children=[expr])

    def expression(self):
        tok_type, tok_value = self.current_token()
        if tok_type in ['INTEGER', 'FLOAT', 'STRING', 'BOOLEAN', 'IDENTIFIER']:
            self.pos += 1
            return ASTNode('Literal', value=tok_value)
        else:
            raise SyntaxError(f"Invalid expression starting with {tok_type} at position {self.pos}")

# Function for external imports
def parse_program(tokens):
    parser = Parser(tokens)
    return parser.parse()

# CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <filename>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    try:
        tokens = list(tokenize(code))
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST:", ast)
    except SyntaxError as e:
        print("Syntax error:", e)
    except RuntimeError as e:
        print("Runtime error:", e)
