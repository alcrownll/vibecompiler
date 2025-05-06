from typing import Dict, List, Optional, Set
from .parser import ASTNode

class Symbol:
    def __init__(self, name: str, type: str, scope_level: int, is_function: bool = False):
        self.name = name
        self.type = type
        self.scope_level = scope_level
        self.is_function = is_function
        self.parameters: List[str] = []  # For functions

class SemanticError(Exception):
    def __init__(self, message: str, node: ASTNode):
        super().__init__(message)
        self.node = node

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table: Dict[str, Symbol] = {}
        self.current_scope_level = 0
        self.scope_stack: List[Set[str]] = [set()]

    def analyze(self, ast: ASTNode):
        self.visit(ast)

    def enter_scope(self):
        self.current_scope_level += 1
        self.scope_stack.append(set())

    def exit_scope(self):
        # Remove symbols from the current scope
        for name in self.scope_stack.pop():
            del self.symbol_table[name]
        self.current_scope_level -= 1

    def declare_symbol(self, name: str, type: str, is_function: bool = False) -> Symbol:
        if name in self.symbol_table:
            raise SemanticError(f"Symbol '{name}' already declared in this scope", None)
        
        symbol = Symbol(name, type, self.current_scope_level, is_function)
        self.symbol_table[name] = symbol
        self.scope_stack[-1].add(name)
        return symbol

    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        return self.symbol_table.get(name)

    def visit(self, node: ASTNode):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        for child in node.children:
            self.visit(child)

    def visit_PROGRAM(self, node: ASTNode):
        self.enter_scope()
        for child in node.children:
            self.visit(child)
        self.exit_scope()

    def visit_VAR_DECL(self, node: ASTNode):
        var_type = node.value
        name_node = node.children[0]
        name = name_node.value
        
        # Declare the variable
        self.declare_symbol(name, var_type)
        
        # If there's an initial value, check its type
        if len(node.children) > 1:
            value_node = node.children[1]
            if var_type == 'ARRAY_TYPE':
                if value_node.type != 'ARRAY_LITERAL':
                    raise SemanticError(f"Type mismatch: expected array literal for array variable", node)
                element_type = self.visit_ARRAY_LITERAL(value_node)
                # Optionally, store element_type for further type checking
            else:
                value_type = self.get_expression_type(value_node)
                if not self.is_type_compatible(var_type, value_type):
                    raise SemanticError(f"Type mismatch: cannot assign {value_type} to {var_type}", node)

    def visit_FUNCTION(self, node: ASTNode):
        name = node.value
        params_node = node.children[0]
        body_node = node.children[1]
        
        # Declare the function
        func_symbol = self.declare_symbol(name, 'FUNCTION', True)
        
        # Add parameters to the symbol table
        self.enter_scope()
        for param in params_node.children:
            param_name = param.value
            param_type = 'UNKNOWN'
            if param.children and param.children[0].type == 'TYPE':
                param_type = param.children[0].value
            func_symbol.parameters.append((param_name, param_type))
            self.declare_symbol(param_name, param_type)
        
        # Analyze function body
        for statement in body_node.children:
            self.visit(statement)
        
        self.exit_scope()

    def visit_IF(self, node: ASTNode):
        condition = node.children[0]
        condition_type = self.get_expression_type(condition)
        
        if condition_type != 'BOOLEAN_TYPE':
            raise SemanticError("If condition must be a boolean expression", condition)
        
        # Analyze if body
        self.enter_scope()
        for statement in node.children[1].children:
            self.visit(statement)
        self.exit_scope()
        
        # Analyze else body if it exists
        if len(node.children) > 2:
            self.enter_scope()
            for statement in node.children[2].children:
                self.visit(statement)
            self.exit_scope()

    def visit_WHILE(self, node: ASTNode):
        condition = node.children[0]
        condition_type = self.get_expression_type(condition)
        
        if condition_type != 'BOOLEAN_TYPE':
            raise SemanticError("While condition must be a boolean expression", condition)
        
        # Analyze loop body
        self.enter_scope()
        for statement in node.children[1].children:
            self.visit(statement)
        self.exit_scope()

    def visit_FOR(self, node: ASTNode):
        # Analyze initialization
        self.enter_scope()
        self.visit(node.children[0])
        
        # Analyze condition
        condition = node.children[1]
        condition_type = self.get_expression_type(condition)
        if condition_type != 'BOOLEAN_TYPE':
            raise SemanticError("For condition must be a boolean expression", condition)
        
        # Analyze update
        self.visit(node.children[2])
        
        # Analyze body
        for statement in node.children[3].children:
            self.visit(statement)
        
        self.exit_scope()

    def visit_BINARY_OP(self, node: ASTNode):
        left_type = self.get_expression_type(node.children[0])
        right_type = self.get_expression_type(node.children[1])
        
        if not self.is_type_compatible(left_type, right_type):
            raise SemanticError(f"Type mismatch in binary operation: {left_type} {node.value} {right_type}", node)

    def visit_IDENTIFIER(self, node: ASTNode):
        name = node.value
        symbol = self.lookup_symbol(name)
        if not symbol:
            raise SemanticError(f"Undeclared variable: {name}", node)

    def get_expression_type(self, node: ASTNode) -> str:
        if node.type == 'LITERAL':
            if node.value.isdigit():
                return 'INTEGER_TYPE'
            elif '.' in node.value and node.value.replace('.', '').isdigit():
                return 'FLOAT_TYPE'
            elif node.value in ['noCap', 'cap']:
                return 'BOOLEAN_TYPE'
            elif node.value == 'ghosted':
                return 'NULL'
            else:
                return 'STRING_TYPE'
        elif node.type == 'IDENTIFIER':
            symbol = self.lookup_symbol(node.value)
            if not symbol:
                raise SemanticError(f"Undeclared variable: {node.value}", node)
            return symbol.type
        elif node.type == 'BINARY_OP':
            left_type = self.get_expression_type(node.children[0])
            right_type = self.get_expression_type(node.children[1])
            # Handle comparison operators
            if node.value in ['>', '<', '>=', '<=', '==', '!=']:
                if left_type in ['INTEGER_TYPE', 'FLOAT_TYPE'] and right_type in ['INTEGER_TYPE', 'FLOAT_TYPE']:
                    return 'BOOLEAN_TYPE'
                else:
                    raise SemanticError(f"Type mismatch in comparison: {left_type} {node.value} {right_type}", node)
            if left_type == right_type:
                return left_type
            elif left_type in ['INTEGER_TYPE', 'FLOAT_TYPE'] and right_type in ['INTEGER_TYPE', 'FLOAT_TYPE']:
                return 'FLOAT_TYPE'  # Promote to float if mixing int and float
            else:
                raise SemanticError(f"Type mismatch in binary operation: {left_type} {node.value} {right_type}", node)
        return 'UNKNOWN'

    def is_type_compatible(self, type1: str, type2: str) -> bool:
        if type1 == type2:
            return True
        if type1 in ['INTEGER_TYPE', 'FLOAT_TYPE'] and type2 in ['INTEGER_TYPE', 'FLOAT_TYPE']:
            return True
        return False

    def visit_ARRAY_LITERAL(self, node: ASTNode):
        if not node.children:
            return 'UNKNOWN'
        first_type = self.get_expression_type(node.children[0])
        for elem in node.children[1:]:
            elem_type = self.get_expression_type(elem)
            if not self.is_type_compatible(first_type, elem_type):
                raise SemanticError(f"Array literal elements must have the same type: {first_type} vs {elem_type}", node)
        return first_type 