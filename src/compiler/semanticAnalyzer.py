import sys
from lexer import tokenize
from parser import parse_program

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        
    def declare(self, name, var_type=None, is_function=False, is_parameter=False):
        if name in self.symbols:
            raise RuntimeError(f"Semantic Error: Variable '{name}' already declared in this scope.")
        self.symbols[name] = {
            'type': var_type,
            'is_function': is_function,
            'is_parameter': is_parameter
        }
        
    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise RuntimeError(f"Semantic Error: Identifier '{name}' not declared.")
    
    def is_declared_in_current_scope(self, name):
        return name in self.symbols

class SemanticAnalyzer:
    def __init__(self):
        self.global_symbol_table = SymbolTable()
        self.current_symbol_table = self.global_symbol_table
        self.in_loop = False  # Track if we're inside a loop for 'staph' (break) statements
        
    def analyze(self, ast):
        if ast is None:
            return None
            
        method_name = f"visit_{ast.node_type}"
        method = getattr(self, method_name, self.generic_visit)
        return method(ast)
        
    def generic_visit(self, node):
        raise RuntimeError(f"No visit method for {node.node_type}")
    
    def visit_Program(self, node):
        for child in node.children:
            self.analyze(child)
        return None  # Programs don't have a type
    
    def visit_Block(self, node):
        # Create a new scope for the block
        old_symbol_table = self.current_symbol_table
        self.current_symbol_table = SymbolTable(parent=old_symbol_table)
        
        for child in node.children:
            self.analyze(child)
            
        # Restore the previous scope
        self.current_symbol_table = old_symbol_table
        return None
    
    def visit_Assignment(self, node):
        var_name = node.value
        expr_type = self.analyze(node.children[0])
        
        # If variable doesn't exist, declare it
        if not self.is_variable_declared(var_name):
            self.current_symbol_table.declare(var_name, expr_type)
        else:
            # Check if types match for already declared variables
            var_info = self.current_symbol_table.lookup(var_name)
            if var_info['is_function']:
                raise RuntimeError(f"Semantic Error: Cannot assign to function '{var_name}'")
                
            if var_info['type'] is not None and expr_type is not None and var_info['type'] != expr_type:
                raise RuntimeError(f"Semantic Error: Cannot assign value of type '{expr_type}' to variable '{var_name}' of type '{var_info['type']}'")
                
        return expr_type
    
    def visit_Identifier(self, node):
        var_name = node.value
        var_info = self.current_symbol_table.lookup(var_name)
        return var_info['type']
    
    def visit_Number(self, node):
        # Determine if it's an int or float
        if isinstance(node.value, int):
            return 'int'
        else:
            return 'float'
    
    def visit_String(self, node):
        return 'string'
    
    def visit_Boolean(self, node):
        return 'boolean'
    
    def visit_Null(self, node):
        return 'null'
    
    def visit_BinaryOp(self, node):
        left_type = self.analyze(node.children[0])
        right_type = self.analyze(node.children[1])
        operator = node.value
        
        # Type checking for binary operations
        if operator in ['+', '-', '*', '/']:
            if left_type in ['int', 'float'] and right_type in ['int', 'float']:
                # For numeric operations, return float if either operand is float
                return 'float' if 'float' in [left_type, right_type] else 'int'
            elif operator == '+' and (left_type == 'string' or right_type == 'string'):
                # String concatenation
                return 'string'
            else:
                raise RuntimeError(f"Semantic Error: Operator '{operator}' cannot be applied to types '{left_type}' and '{right_type}'")
        elif operator in ['==', '!=', '<', '>', '<=', '>=']:
            # Comparison operators return boolean
            # Check if types are comparable
            if (left_type in ['int', 'float'] and right_type in ['int', 'float']) or \
               (left_type == right_type):
                return 'boolean'
            else:
                raise RuntimeError(f"Semantic Error: Cannot compare types '{left_type}' and '{right_type}'")
        elif operator in ['&&', '||']:
            # Logical operators require boolean operands
            if left_type == 'boolean' and right_type == 'boolean':
                return 'boolean'
            else:
                raise RuntimeError(f"Semantic Error: Logical operator '{operator}' requires boolean operands, got '{left_type}' and '{right_type}'")
        
        return None
    
    def visit_Print(self, node):
        # Any type can be printed
        self.analyze(node.children[0])
        return None
    
    def visit_If(self, node):
        # Check that condition is a boolean
        condition_type = self.analyze(node.children[0])
        if condition_type != 'boolean':
            raise RuntimeError(f"Semantic Error: Condition must be a boolean, got '{condition_type}'")
        
        # Analyze then-block
        self.analyze(node.children[1])
        
        # Analyze else-if and else blocks if they exist
        for i in range(2, len(node.children)):
            child = node.children[i]
            
            if child is None:  # Skip None (for missing else block)
                continue
                
            if child.node_type == 'ElseIf':
                # ElseIf should have a condition and a block
                elseif_condition_type = self.analyze(child.children[0])
                if elseif_condition_type != 'boolean':
                    raise RuntimeError(f"Semantic Error: ElseIf condition must be a boolean, got '{elseif_condition_type}'")
                self.analyze(child.children[1])
            else:
                # This is the else block
                self.analyze(child)
        
        return None
    
    def visit_While(self, node):
        # Check that condition is a boolean
        condition_type = self.analyze(node.children[0])
        if condition_type != 'boolean':
            raise RuntimeError(f"Semantic Error: While condition must be a boolean, got '{condition_type}'")
        
        # Mark that we're inside a loop
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Analyze loop body
        self.analyze(node.children[1])
        
        # Restore previous loop status
        self.in_loop = old_in_loop
        
        return None
    
    def visit_For(self, node):
        # For has initialization, condition, increment, and body
        init = node.children[0]
        condition = node.children[1]
        increment = node.children[2]
        body = node.children[3]
        
        # Create a new scope for the for loop variables
        old_symbol_table = self.current_symbol_table
        self.current_symbol_table = SymbolTable(parent=old_symbol_table)
        
        # Analyze initialization if provided
        if init:
            self.analyze(init)
        
        # Check that condition is a boolean if provided
        if condition:
            condition_type = self.analyze(condition)
            if condition_type != 'boolean':
                raise RuntimeError(f"Semantic Error: For condition must be a boolean, got '{condition_type}'")
        
        # Mark that we're inside a loop
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Analyze loop body
        self.analyze(body)
        
        # Analyze increment if provided
        if increment:
            self.analyze(increment)
        
        # Restore previous loop status and symbol table
        self.in_loop = old_in_loop
        self.current_symbol_table = old_symbol_table
        
        return None
    
    def visit_Break(self, node):
        if not self.in_loop:
            raise RuntimeError("Semantic Error: 'staph' (break) statement outside of loop")
        return None
    
    def visit_FunctionDeclaration(self, node):
        function_name = node.value
        parameters_node = node.children[0]
        body_node = node.children[1]
        
        # Make sure the function isn't already declared in this scope
        if self.current_symbol_table.is_declared_in_current_scope(function_name):
            raise RuntimeError(f"Semantic Error: Function '{function_name}' already declared")
        
        # Add function to symbol table
        self.current_symbol_table.declare(function_name, is_function=True)
        
        # Create a new scope for the function body
        old_symbol_table = self.current_symbol_table
        self.current_symbol_table = SymbolTable(parent=old_symbol_table)
        
        # Add parameters to the function's scope
        parameters = parameters_node.value  # List of parameter names
        for param in parameters:
            self.current_symbol_table.declare(param, is_parameter=True)
        
        # Analyze function body
        self.analyze(body_node)
        
        # Restore the previous scope
        self.current_symbol_table = old_symbol_table
        
        return None
    
    def visit_FunctionCall(self, node):
        function_name = node.value
        arguments = node.children
        
        # Check if the function exists
        try:
            func_info = self.current_symbol_table.lookup(function_name)
            if not func_info['is_function']:
                raise RuntimeError(f"Semantic Error: '{function_name}' is not a function")
        except RuntimeError:
            # Allow undefined functions for this simplified analyzer
            # In a full compiler, you'd check that function exists and argument types match parameters
            pass
        
        # Analyze all arguments
        for arg in arguments:
            self.analyze(arg)
        
        # For simplicity, we don't do parameter count or type checking here
        # Returning 'any' as function call's return type
        return 'any'
    
    def visit_Return(self, node):
        # Analyze the return expression
        return_type = self.analyze(node.children[0])
        
        # In a full compiler, you'd check that return type matches function's declared type
        return None
    
    def is_variable_declared(self, name):
        try:
            self.current_symbol_table.lookup(name)
            return True
        except RuntimeError:
            return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python semantic_analyzer.py <source_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    
    try:
        tokens = tokenize(code)
        ast = parse_program(tokens)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("Semantic analysis completed successfully.")
    except RuntimeError as e:
        print(e)
    except SyntaxError as e:
        print(f"Syntax error: {e}")