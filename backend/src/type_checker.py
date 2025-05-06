from typing import Optional, Union
from .parser import ASTNode
from .errors import SemanticError
from .symbol_table import SymbolTable

class TypeChecker:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table

    def check_type_compatibility(self, type1: str, type2: str) -> bool:
        """Check if two types are compatible for operations"""
        # Basic type compatibility rules
        if type1 == type2:
            return True
        
        # Numeric type compatibility
        if type1 in ['INTEGER_TYPE', 'FLOAT_TYPE'] and type2 in ['INTEGER_TYPE', 'FLOAT_TYPE']:
            return True
            
        # Array type compatibility
        if type1 == 'ARRAY_TYPE' and type2 == 'ARRAY_TYPE':
            return True
            
        return False

    def get_expression_type(self, node: ASTNode) -> str:
        """Determine the type of an expression"""
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
            symbol = self.symbol_table.lookup_symbol(node.value)
            if not symbol:
                raise SemanticError(f"Undeclared variable: {node.value}")
            return symbol.type
        elif node.type == 'BINARY_OP':
            left_type = self.get_expression_type(node.children[0])
            right_type = self.get_expression_type(node.children[1])
            
            if not self.check_type_compatibility(left_type, right_type):
                raise SemanticError(f"Type mismatch in binary operation: {left_type} {node.value} {right_type}")
            
            # For numeric operations, promote to float if either operand is float
            if left_type == 'FLOAT_TYPE' or right_type == 'FLOAT_TYPE':
                return 'FLOAT_TYPE'
            return left_type
        elif node.type == 'ARRAY_LITERAL':
            if not node.children:
                return 'ARRAY_TYPE'
            element_type = self.get_expression_type(node.children[0])
            for elem in node.children[1:]:
                if not self.check_type_compatibility(element_type, self.get_expression_type(elem)):
                    raise SemanticError(f"Array elements must have compatible types")
            return 'ARRAY_TYPE'
        
        return 'UNKNOWN'

    def check_assignment(self, target_type: str, value_type: str, node: ASTNode):
        """Check if an assignment is type-safe"""
        if not self.check_type_compatibility(target_type, value_type):
            raise SemanticError(f"Cannot assign {value_type} to {target_type}", node=node)

    def check_function_call(self, func_name: str, args: list[ASTNode], node: ASTNode):
        """Check if a function call is type-safe"""
        func_symbol = self.symbol_table.lookup_symbol(func_name)
        if not func_symbol or not func_symbol.is_function:
            raise SemanticError(f"'{func_name}' is not a function", node=node)
        
        if len(args) != len(func_symbol.parameters):
            raise SemanticError(f"Function '{func_name}' expects {len(func_symbol.parameters)} arguments, got {len(args)}", node=node)
        
        for arg, (param_name, param_type) in zip(args, func_symbol.parameters):
            arg_type = self.get_expression_type(arg)
            if not self.check_type_compatibility(param_type, arg_type):
                raise SemanticError(f"Type mismatch in function call: expected {param_type}, got {arg_type}", node=node) 