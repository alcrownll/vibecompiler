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
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '', 0, 0)
    
    def peek(self, offset=1):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return ('EOF', '', 0, 0)
    
    def match(self, expected_type):
        tok_type, tok_value, line, col = self.current_token()
        if tok_type == expected_type:
            self.pos += 1
            return tok_value
        else:
            raise SyntaxError(f"Expected {expected_type} but found {tok_type} at line {line}, column {col}")
    
    def parse(self):
        return self.program()
    
    def program(self):
        # Program starts with 'starterPack'
        self.match('PROGRAM')
        statements = []
        
        while self.current_token()[0] != 'EOF':
            statement = self.statement()
            if statement:  # Skip empty statements (like extra semicolons)
                statements.append(statement)
                
        return ASTNode('Program', children=statements)
    
    def statement(self):
        tok_type, tok_value, line, col = self.current_token()
        
        if tok_type == 'SEMICOLON':
            self.pos += 1  # Skip semicolon
            return None
            
        if tok_type == 'PRINT':
            return self.print_statement()
        elif tok_type == 'IF':
            return self.if_statement()
        elif tok_type == 'WHILE':
            return self.while_statement()
        elif tok_type == 'FOR':
            return self.for_statement()
        elif tok_type == 'FUNCTION':
            return self.function_declaration()
        elif tok_type == 'IDENTIFIER':
            # Check if this is an assignment (next token is '=')
            if self.peek()[0] == 'ASSIGN':
                return self.assignment_statement()
            # Otherwise, it's a function call or variable reference
            return self.expression_statement()
        elif tok_type == 'RETURN':
            return self.return_statement()
        elif tok_type == 'BREAK':
            self.pos += 1  # Consume 'staph'
            self.match('SEMICOLON')
            return ASTNode('Break')
        elif tok_type == 'LBRACE':
            return self.block()
        else:
            raise SyntaxError(f"Unexpected token {tok_type} at line {line}, column {col}")
    
    def print_statement(self):
        self.match('PRINT')
        expr = self.expression()
        self.match('SEMICOLON')
        return ASTNode('Print', children=[expr])
    
    def if_statement(self):
        self.match('IF')
        condition = self.expression()
        then_block = self.block()
        else_block = None
        
        tok_type = self.current_token()[0]
        if tok_type == 'ELSEIF':
            elseif_statements = []
            while tok_type == 'ELSEIF':
                self.pos += 1  # Consume 'maybe'
                elseif_condition = self.expression()
                elseif_block = self.block()
                elseif_statements.append(ASTNode('ElseIf', children=[elseif_condition, elseif_block]))
                tok_type = self.current_token()[0]
            
            if tok_type == 'ELSE':
                self.pos += 1  # Consume 'pass'
                else_block = self.block()
                
            return ASTNode('If', children=[condition, then_block, *elseif_statements, else_block])
        elif tok_type == 'ELSE':
            self.pos += 1  # Consume 'pass'
            else_block = self.block()
            
        return ASTNode('If', children=[condition, then_block, else_block])
    
    def while_statement(self):
        self.match('WHILE')
        condition = self.expression()
        body = self.block()
        return ASTNode('While', children=[condition, body])
    
    def for_statement(self):
        self.match('FOR')
        self.match('LPAREN')
        
        # Initialization
        init = None
        if self.current_token()[0] != 'SEMICOLON':
            init = self.assignment_statement()
        else:
            self.match('SEMICOLON')
        
        # Condition
        condition = None
        if self.current_token()[0] != 'SEMICOLON':
            condition = self.expression()
        self.match('SEMICOLON')
        
        # Increment
        increment = None
        if self.current_token()[0] != 'RPAREN':
            increment = self.assignment_statement()
        self.match('RPAREN')
        
        body = self.block()
        return ASTNode('For', children=[init, condition, increment, body])
    
    def block(self):
        self.match('LBRACE')
        statements = []
        
        while self.current_token()[0] != 'RBRACE':
            statement = self.statement()
            if statement:  # Skip empty statements
                statements.append(statement)
                
        self.match('RBRACE')
        return ASTNode('Block', children=statements)
    
    def function_declaration(self):
        self.match('FUNCTION')
        function_name = self.match('IDENTIFIER')
        
        self.match('LPAREN')
        parameters = []
        
        if self.current_token()[0] != 'RPAREN':
            parameters.append(self.match('IDENTIFIER'))
            while self.current_token()[0] == 'COMMA':
                self.pos += 1  # Consume comma
                parameters.append(self.match('IDENTIFIER'))
                
        self.match('RPAREN')
        body = self.block()
        
        return ASTNode('FunctionDeclaration', value=function_name, 
                      children=[ASTNode('Parameters', value=parameters), body])
    
    def assignment_statement(self):
        identifier = self.match('IDENTIFIER')
        self.match('ASSIGN')
        expr = self.expression()
        self.match('SEMICOLON')
        return ASTNode('Assignment', value=identifier, children=[expr])
    
    def expression_statement(self):
        expr = self.expression()
        self.match('SEMICOLON')
        return expr
    
    def return_statement(self):
        self.match('RETURN')
        expr = self.expression()
        self.match('SEMICOLON')
        return ASTNode('Return', children=[expr])
    
    def expression(self):
        return self.logical_expression()
    
    def logical_expression(self):
        expr = self.comparison_expression()
        
        while self.current_token()[0] == 'OP' and self.current_token()[1] in ['&&', '||']:
            op = self.current_token()[1]
            self.pos += 1  # Consume operator
            right = self.comparison_expression()
            expr = ASTNode('BinaryOp', value=op, children=[expr, right])
            
        return expr
    
    def comparison_expression(self):
        expr = self.additive_expression()
        
        while (self.current_token()[0] == 'OP' and 
               self.current_token()[1] in ['==', '!=', '<', '>', '<=', '>=']):
            op = self.current_token()[1]
            self.pos += 1  # Consume operator
            right = self.additive_expression()
            expr = ASTNode('BinaryOp', value=op, children=[expr, right])
            
        return expr
    
    def additive_expression(self):
        expr = self.multiplicative_expression()
        
        while self.current_token()[0] == 'OP' and self.current_token()[1] in ['+', '-']:
            op = self.current_token()[1]
            self.pos += 1  # Consume operator
            right = self.multiplicative_expression()
            expr = ASTNode('BinaryOp', value=op, children=[expr, right])
            
        return expr
    
    def multiplicative_expression(self):
        expr = self.primary_expression()
        
        while self.current_token()[0] == 'OP' and self.current_token()[1] in ['*', '/']:
            op = self.current_token()[1]
            self.pos += 1  # Consume operator
            right = self.primary_expression()
            expr = ASTNode('BinaryOp', value=op, children=[expr, right])
            
        return expr
    
    def primary_expression(self):
        tok_type, tok_value, line, col = self.current_token()
        
        if tok_type == 'LPAREN':
            self.pos += 1  # Consume '('
            expr = self.expression()
            self.match('RPAREN')
            return expr
        elif tok_type == 'IDENTIFIER':
            self.pos += 1  # Consume identifier
            
            # Check if this is a function call
            if self.current_token()[0] == 'LPAREN':
                self.pos += 1  # Consume '('
                arguments = []
                
                if self.current_token()[0] != 'RPAREN':
                    arguments.append(self.expression())
                    while self.current_token()[0] == 'COMMA':
                        self.pos += 1  # Consume comma
                        arguments.append(self.expression())
                        
                self.match('RPAREN')
                return ASTNode('FunctionCall', value=tok_value, children=arguments)
                
            # Otherwise, it's a variable reference
            return ASTNode('Identifier', value=tok_value)
        elif tok_type == 'NUMBER':
            self.pos += 1  # Consume number
            return ASTNode('Number', value=tok_value)
        elif tok_type == 'STRING':
            self.pos += 1  # Consume string
            return ASTNode('String', value=tok_value)
        elif tok_type == 'TRUE':
            self.pos += 1  # Consume 'noCap'
            return ASTNode('Boolean', value=True)
        elif tok_type == 'FALSE':
            self.pos += 1  # Consume 'cap'
            return ASTNode('Boolean', value=False)
        elif tok_type == 'NULL':
            self.pos += 1  # Consume 'ghosted'
            return ASTNode('Null')
        else:
            raise SyntaxError(f"Unexpected token {tok_type} at line {line}, column {col}")

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
        print("Syntax analysis completed successfully.")
    except SyntaxError as e:
        print("Syntax error:", e)
    except RuntimeError as e:
        print("Runtime error:", e)