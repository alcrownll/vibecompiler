from typing import List, Optional, Dict, Any
from .lexer import Token, Lexer
from .errors import SyntaxError as VibeSyntaxError

class ASTNode:
    def __init__(self, type: str, value: Optional[str] = None, children: Optional[List['ASTNode']] = None):
        self.type = type
        self.value = value
        self.children = children or []

    def __str__(self, level=0):
        ret = "  " * level + f"{self.type}: {self.value}\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens: List[Token] = []
        self.current_token: Optional[Token] = None
        self.token_index = 0

    def parse(self, code: str) -> ASTNode:
        self.tokens = self.lexer.tokenize(code)
        self.token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        return self.program()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def expect(self, token_type: str) -> 'Token':
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        if self.current_token:
            raise VibeSyntaxError(
                f"Expected '{token_type.lower()}' but found '{self.current_token.value}'",
                self.current_token.line,
                self.current_token.column
            )
        else:
            raise VibeSyntaxError(f"Expected '{token_type.lower()}' but found EOF", None, None)

    def program(self) -> ASTNode:
        # PROGRAM -> 'starterPack' IDENTIFIER '{' statements '}'
        self.expect('PROGRAM')
        program_name = self.expect('IDENTIFIER')
        self.expect('LBRACE')
        
        statements = []
        while self.current_token and self.current_token.type != 'RBRACE':
            statements.append(self.statement())
        
        self.expect('RBRACE')
        return ASTNode('PROGRAM', program_name.value, statements)

    def statement(self) -> ASTNode:
        if not self.current_token:
            raise VibeSyntaxError("Unexpected end of input", None, None)
            
        token_type = self.current_token.type
        
        if token_type == 'PRINT':
            return self.print_statement()
        elif token_type == 'IF':
            return self.if_statement()
        elif token_type == 'WHILE':
            return self.while_statement()
        elif token_type == 'FOR':
            return self.for_statement()
        elif token_type == 'FUNCTION':
            return self.function_declaration()
        elif token_type in ['INTEGER_TYPE', 'FLOAT_TYPE', 'STRING_TYPE', 'BOOLEAN_TYPE', 'ARRAY_TYPE', 'DICT_TYPE']:
            return self.variable_declaration()
        else:
            return self.expression_statement()

    def print_statement(self) -> ASTNode:
        self.expect('PRINT')
        self.expect('LPAREN')
        expr = self.expression()
        self.expect('RPAREN')
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.advance()
        return ASTNode('PRINT', children=[expr])

    def if_statement(self) -> ASTNode:
        self.expect('IF')
        self.expect('LPAREN')
        condition = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        if_body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if_body.append(self.statement())
        self.expect('RBRACE')

        # Collect maybe (ELSEIF) blocks
        elseif_blocks = []
        while self.current_token and self.current_token.type == 'ELSEIF':
            self.expect('ELSEIF')
            self.expect('LPAREN')
            elseif_condition = self.expression()
            self.expect('RPAREN')
            self.expect('LBRACE')
            elseif_body = []
            while self.current_token and self.current_token.type != 'RBRACE':
                elseif_body.append(self.statement())
            self.expect('RBRACE')
            elseif_blocks.append((elseif_condition, elseif_body))

        # Optional else block
        else_body = []
        if self.current_token and self.current_token.type == 'ELSE':
            self.expect('ELSE')
            self.expect('LBRACE')
            while self.current_token and self.current_token.type != 'RBRACE':
                else_body.append(self.statement())
            self.expect('RBRACE')

        # Build AST: IF node with children: [main_condition, main_body, [elseif_blocks], else_body]
        elseif_nodes = [ASTNode('ELSEIF', children=[cond, ASTNode('ELSEIF_BODY', children=body)]) for cond, body in elseif_blocks]
        return ASTNode('IF', children=[
            condition,
            ASTNode('IF_BODY', children=if_body),
            ASTNode('ELSEIF_BLOCKS', children=elseif_nodes),
            ASTNode('ELSE_BODY', children=else_body)
        ])

    def while_statement(self) -> ASTNode:
        self.expect('WHILE')
        self.expect('LPAREN')
        condition = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            body.append(self.statement())
        self.expect('RBRACE')
        
        return ASTNode('WHILE', children=[condition, ASTNode('BODY', children=body)])

    def for_statement(self) -> ASTNode:
        self.expect('FOR')
        self.expect('LPAREN')
        # Allow empty, variable declaration, or expression/assignment for init
        if self.current_token and self.current_token.type == 'SEMICOLON':
            init = None
            self.expect('SEMICOLON')
        elif self.current_token and self.current_token.type in ['INTEGER_TYPE', 'FLOAT_TYPE', 'STRING_TYPE', 'BOOLEAN_TYPE', 'ARRAY_TYPE', 'DICT_TYPE']:
            init = self.variable_declaration()
            # variable_declaration already consumes the semicolon if present
        else:
            init = self.expression_statement()
            if self.current_token and self.current_token.type == 'SEMICOLON':
                self.advance()
        # Condition (can be empty)
        if self.current_token and self.current_token.type == 'SEMICOLON':
            condition = None
            self.expect('SEMICOLON')
        else:
            condition = self.expression()
            self.expect('SEMICOLON')
        # Update (can be empty)
        if self.current_token and self.current_token.type == 'RPAREN':
            update = None
        else:
            update = self.expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            body.append(self.statement())
        self.expect('RBRACE')
        
        return ASTNode('FOR', children=[init, condition, update, ASTNode('BODY', children=body)])

    def function_declaration(self) -> ASTNode:
        self.expect('FUNCTION')
        name = self.expect('IDENTIFIER')
        self.expect('LPAREN')
        
        params = []
        if self.current_token and self.current_token.type != 'RPAREN':
            # Parse type and name
            param_type = None
            if self.current_token.type in ['INTEGER_TYPE', 'FLOAT_TYPE', 'STRING_TYPE', 'BOOLEAN_TYPE', 'ARRAY_TYPE', 'DICT_TYPE']:
                param_type = self.current_token.type
                self.advance()
            param_name = self.expect('IDENTIFIER')
            params.append(ASTNode('PARAM', param_name.value, [ASTNode('TYPE', param_type)] if param_type else []))
            while self.current_token and self.current_token.type == 'COMMA':
                self.expect('COMMA')
                param_type = None
                if self.current_token.type in ['INTEGER_TYPE', 'FLOAT_TYPE', 'STRING_TYPE', 'BOOLEAN_TYPE', 'ARRAY_TYPE', 'DICT_TYPE']:
                    param_type = self.current_token.type
                    self.advance()
                param_name = self.expect('IDENTIFIER')
                params.append(ASTNode('PARAM', param_name.value, [ASTNode('TYPE', param_type)] if param_type else []))
        
        self.expect('RPAREN')
        self.expect('LBRACE')
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            body.append(self.statement())
        self.expect('RBRACE')
        
        return ASTNode('FUNCTION', name.value, [ASTNode('PARAMS', children=params), ASTNode('BODY', children=body)])

    def variable_declaration(self) -> ASTNode:
        var_type = self.current_token.type
        self.advance()
        name = self.expect('IDENTIFIER')
        
        if self.current_token and self.current_token.type == 'OP' and self.current_token.value == '=':
            self.expect('OP')
            value = self.expression()
        else:
            value = None
        
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.advance()
        return ASTNode('VAR_DECL', var_type, [ASTNode('IDENTIFIER', name.value), value] if value else [ASTNode('IDENTIFIER', name.value)])

    def expression_statement(self) -> ASTNode:
        expr = self.expression()
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.advance()
        return expr

    def expression(self) -> ASTNode:
        return self.assignment_expression()

    def assignment_expression(self) -> ASTNode:
        # Check for assignment: IDENTIFIER = expression
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            identifier_token = self.current_token
            self.advance()
            if self.current_token and self.current_token.type == 'OP' and self.current_token.value == '=':
                self.expect('OP')
                value = self.expression()
                return ASTNode('ASSIGN', identifier_token.value, [value])
            else:
                # Not an assignment, treat as identifier
                self.token_index -= 1
                self.current_token = identifier_token
        return self.binary_expression()

    def binary_expression(self) -> ASTNode:
        left = self.primary_expression()
        
        while self.current_token and self.current_token.type == 'OP':
            op = self.current_token
            self.advance()
            right = self.primary_expression()
            left = ASTNode('BINARY_OP', op.value, [left, right])
        
        return left

    def primary_expression(self) -> ASTNode:
        if not self.current_token:
            raise VibeSyntaxError("Unexpected end of input", None, None)
            
        if self.current_token.type in ['NUMBER', 'STRING', 'TRUE', 'FALSE', 'NULL']:
            token = self.current_token
            self.advance()
            return ASTNode('LITERAL', token.value)
        elif self.current_token.type == 'IDENTIFIER':
            token = self.current_token
            self.advance()
            return ASTNode('IDENTIFIER', token.value)
        elif self.current_token.type == 'LPAREN':
            self.expect('LPAREN')
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        elif self.current_token.type == 'LBRACKET':
            return self.parse_array_literal()
        else:
            raise VibeSyntaxError(f"Unexpected token: {self.current_token.type}", self.current_token.line, self.current_token.column)

    def parse_array_literal(self) -> ASTNode:
        self.expect('LBRACKET')
        elements = []
        if self.current_token and self.current_token.type != 'RBRACKET':
            elements.append(self.expression())
            while self.current_token and self.current_token.type == 'COMMA':
                self.expect('COMMA')
                elements.append(self.expression())
        self.expect('RBRACKET')
        return ASTNode('ARRAY_LITERAL', children=elements)