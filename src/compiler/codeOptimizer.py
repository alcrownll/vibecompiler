"""
Code optimization module for VibeScript compiler.
Contains various optimization techniques to improve generated code.
"""

from error_handler import Warning


class CodeOptimizer:
    """Base class for code optimization passes"""
    
    def __init__(self, ast):
        self.ast = ast
        self.optimized = False
    
    def optimize(self):
        """Implement optimization logic in subclasses"""
        raise NotImplementedError
    
    def was_optimized(self):
        return self.optimized


class ConstantFolding(CodeOptimizer):
    """Evaluate constant expressions at compile time"""
    
    def optimize(self):
        self.optimized = False
        self._fold_constants(self.ast)
        return self.ast
    
    def _fold_constants(self, node):
        if node is None:
            return None
        
        # Process children first (bottom-up traversal)
        if hasattr(node, 'children'):
            for i, child in enumerate(node.children):
                node.children[i] = self._fold_constants(child)
        
        # Handle binary operations on constants
        if node.node_type == 'BinaryOp':
            left, right = node.children
            
            # Check if both operands are constants
            if (left.node_type in ('Number', 'Boolean', 'String') and 
                right.node_type in ('Number', 'Boolean', 'String')):
                
                result = self._evaluate_constant_expression(left, right, node.value)
                if result is not None:
                    self.optimized = True
                    return result
        
        return node
    
    def _evaluate_constant_expression(self, left, right, operator):
        """Calculate result of constant binary operation"""
        from ast_nodes import ASTNode  # Import locally to avoid circular imports
        
        # Extract values based on node types
        left_val = self._get_node_value(left)
        right_val = self._get_node_value(right)
        
        # Handle different operators
        result = None
        
        try:
            if operator == '+':
                result = left_val + right_val
            elif operator == '-':
                result = left_val - right_val
            elif operator == '*':
                result = left_val * right_val
            elif operator == '/':
                if right_val == 0:
                    # Don't optimize division by zero
                    return None
                result = left_val / right_val
            elif operator == '==':
                result = left_val == right_val
            elif operator == '!=':
                result = left_val != right_val
            elif operator == '<':
                result = left_val < right_val
            elif operator == '>':
                result = left_val > right_val
            elif operator == '<=':
                result = left_val <= right_val
            elif operator == '>=':
                result = left_val >= right_val
            elif operator == '&&':
                result = left_val and right_val
            elif operator == '||':
                result = left_val or right_val
        except (TypeError, ValueError):
            # If operation is not valid for the types, don't optimize
            return None
            
        # Create appropriate node type based on result
        if isinstance(result, bool):
            return ASTNode('Boolean', value=result)
        elif isinstance(result, (int, float)):
            return ASTNode('Number', value=result)
        elif isinstance(result, str):
            return ASTNode('String', value=result)
        
        return None
    
    def _get_node_value(self, node):
        """Extract actual value from AST node"""
        if node.node_type == 'Number':
            # Handle int vs float
            if isinstance(node.value, str) and '.' in node.value:
                return float(node.value)
            else:
                try:
                    return int(node.value)
                except ValueError:
                    return float(node.value)
        elif node.node_type == 'Boolean':
            return node.value
        elif node.node_type == 'String':
            # Remove quotes and handle escape sequences
            raw = node.value[1:-1]
            return raw.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
        return None


class DeadCodeElimination(CodeOptimizer):
    """Remove unreachable code"""
    
    def optimize(self):
        self.optimized = False
        self._eliminate_dead_code(self.ast)
        return self.ast
    
    def _eliminate_dead_code(self, node):
        if node is None:
            return None
        
        # Process children first
        if hasattr(node, 'children'):
            for i, child in enumerate(node.children):
                node.children[i] = self._eliminate_dead_code(child)
        
        # Handle if statements with constant conditions
        if node.node_type == 'If':
            condition = node.children[0]
            then_block = node.children[1]
            else_block = node.children[2] if len(node.children) > 2 else None
            
            # Check if condition is a constant
            if condition.node_type == 'Boolean':
                self.optimized = True
                
                if condition.value:  # True condition
                    return then_block
                elif else_block:     # False condition with else
                    return else_block
                else:                # False with no else
                    # Return an empty block
                    from ast_nodes import ASTNode  # Import locally
                    return ASTNode('Block', children=[])
        
        # Handle while loops with constant false conditions
        if node.node_type == 'While':
            condition = node.children[0]
            
            if condition.node_type == 'Boolean' and condition.value is False:
                self.optimized = True
                # Return an empty block instead of the loop
                from ast_nodes import ASTNode
                return ASTNode('Block', children=[])
        
        return node


class StrengthReduction(CodeOptimizer):
    """Replace expensive operations with cheaper equivalents"""
    
    def optimize(self):
        self.optimized = False
        self._reduce_strength(self.ast)
        return self.ast
    
    def _reduce_strength(self, node):
        if node is None:
            return None
        
        # Process children first
        if hasattr(node, 'children'):
            for i, child in enumerate(node.children):
                node.children[i] = self._reduce_strength(child)
        
        # Handle multiplication by powers of 2 -> left shift
        if node.node_type == 'BinaryOp' and node.value == '*':
            left, right = node.children
            
            # Convert x * 2^n to x << n
            if self._is_power_of_two(right):
                from ast_nodes import ASTNode
                power = self._log2(self._get_number_value(right))
                if power > 0:
                    self.optimized = True
                    shift_node = ASTNode('BinaryOp', value='<<')
                    shift_node.add_child(left)
                    shift_node.add_child(ASTNode('Number', value=power))
                    return shift_node
            
            # Same for right operand
            if self._is_power_of_two(left):
                from ast_nodes import ASTNode
                power = self._log2(self._get_number_value(left))
                if power > 0:
                    self.optimized = True
                    shift_node = ASTNode('BinaryOp', value='<<')
                    shift_node.add_child(right)
                    shift_node.add_child(ASTNode('Number', value=power))
                    return shift_node
        
        # Handle division by powers of 2 -> right shift
        if node.node_type == 'BinaryOp' and node.value == '/':
            left, right = node.children
            
            # Convert x / 2^n to x >> n
            if self._is_power_of_two(right):
                from ast_nodes import ASTNode
                power = self._log2(self._get_number_value(right))
                if power > 0:
                    self.optimized = True
                    shift_node = ASTNode('BinaryOp', value='>>')
                    shift_node.add_child(left)
                    shift_node.add_child(ASTNode('Number', value=power))
                    return shift_node
        
        # Convert x * 1 to x and other algebraic identities
        if node.node_type == 'BinaryOp':
            left, right = node.children
            op = node.value
            
            # Multiplicative identities
            if op == '*':
                # x * 1 = x
                if self._is_value(right, 1):
                    self.optimized = True
                    return left
                # 1 * x = x
                if self._is_value(left, 1):
                    self.optimized = True
                    return right
                # x * 0 = 0 (if no side effects)
                if self._is_value(right, 0) and self._has_no_side_effects(left):
                    self.optimized = True
                    from ast_nodes import ASTNode
                    return ASTNode('Number', value=0)
                # 0 * x = 0 (if no side effects)
                if self._is_value(left, 0) and self._has_no_side_effects(right):
                    self.optimized = True
                    from ast_nodes import ASTNode
                    return ASTNode('Number', value=0)
            
            # Additive identities
            elif op == '+':
                # x + 0 = x
                if self._is_value(right, 0):
                    self.optimized = True
                    return left
                # 0 + x = x
                if self._is_value(left, 0):
                    self.optimized = True
                    return right
            
            # Subtractive identities
            elif op == '-':
                # x - 0 = x
                if self._is_value(right, 0):
                    self.optimized = True
                    return left
                # x - x = 0 (if no side effects and same variable)
                if (left.node_type == 'Identifier' and right.node_type == 'Identifier' and
                    left.value == right.value):
                    self.optimized = True
                    from ast_nodes import ASTNode
                    return ASTNode('Number', value=0)
            
            # Division identities
            elif op == '/':
                # x / 1 = x
                if self._is_value(right, 1):
                    self.optimized = True
                    return left
                # 0 / x = 0 (if no side effects and x != 0)
                if self._is_value(left, 0) and self._has_no_side_effects(right):
                    self.optimized = True
                    from ast_nodes import ASTNode
                    return ASTNode('Number', value=0)
        
        return node
    
    def _is_power_of_two(self, node):
        """Check if node is a power of 2"""
        if node.node_type != 'Number':
            return False
        
        value = self._get_number_value(node)
        if not isinstance(value, (int, float)):
            return False
        
        # Check if integer and power of 2
        return value > 0 and (value & (value - 1)) == 0
    
    def _log2(self, n):
        """Calculate log base 2 (position of the highest bit)"""
        result = 0
        while n > 1:
            n >>= 1
            result += 1
        return result
    
    def _get_number_value(self, node):
        """Extract numerical value from a number node"""
        if node.node_type != 'Number':
            return None
        
        value = node.value
        if isinstance(value, (int, float)):
            return value
        
        try:
            if isinstance(value, str) and '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return None
    
    def _is_value(self, node, value):
        """Check if node is a specific numerical value"""
        if node.node_type != 'Number':
            return False
        
        node_val = self._get_number_value(node)
        return node_val == value
    
    def _has_no_side_effects(self, node):
        """Check if evaluating a node has no side effects"""
        if node is None:
            return True
        
        # Simple literals have no side effects
        if node.node_type in ('Number', 'Boolean', 'String', 'Identifier'):
            return True
        
        # Function calls have potential side effects
        if node.node_type == 'FunctionCall':
            return False
        
        # Assignments have side effects
        if node.node_type == 'Assignment':
            return False
        
        # Check children recursively
        if hasattr(node, 'children'):
            for child in node.children:
                if not self._has_no_side_effects(child):
                    return False
        
        return True


class UnusedCodeAnalyzer(CodeOptimizer):
    """Identify unused variables and functions"""
    
    def optimize(self):
        self.unused_vars = set()
        self.declared_vars = set()
        self.used_vars = set()
        
        self.unused_funcs = set()
        self.declared_funcs = set()
        self.used_funcs = set()
        
        # First pass: collect declarations
        self._collect_declarations(self.ast)
        
        # Second pass: collect usages
        self._collect_usages(self.ast)
        
        # Find unused variables and functions
        self.unused_vars = self.declared_vars - self.used_vars
        self.unused_funcs = self.declared_funcs - self.used_funcs
        
        return self.ast
    
    def get_warnings(self):
        warnings = []
        
        for var in self.unused_vars:
            name, line, col = var
            warnings.append(Warning(
                line, col, 
                f"Unused variable '{name}'",
                "UNUSED_VAR"
            ))
        
        for func in self.unused_funcs:
            name, line, col = func
            # Don't warn about main function as it's implicitly used
            if name != "main":  
                warnings.append(Warning(
                    line, col, 
                    f"Unused function '{name}'",
                    "UNUSED_FUNC"
                ))
        
        return warnings
    
    def _collect_declarations(self, node):
        if node is None:
            return
        
        if node.node_type == 'Assignment':
            # Check if this is a variable declaration (first assignment)
            var_name = node.value
            self.declared_vars.add((var_name, node.line, node.column))
        
        elif node.node_type == 'FunctionDeclaration':
            func_name = node.value
            self.declared_funcs.add((func_name, node.line, node.column))
        
        # Recursively process children
        if hasattr(node, 'children'):
            for child in node.children:
                self._collect_declarations(child)
    
    def _collect_usages(self, node):
        if node is None:
            return
        
        if node.node_type == 'Identifier':
            # Variable usage
            var_name = node.value
            matched_vars = [v for v in self.declared_vars if v[0] == var_name]
            for var in matched_vars:
                self.used_vars.add(var)
        
        elif node.node_type == 'FunctionCall':
            # Function usage
            func_name = node.value
            matched_funcs = [f for f in self.declared_funcs if f[0] == func_name]
            for func in matched_funcs:
                self.used_funcs.add(func)
        
        elif node.node_type == 'Assignment':
            # The right side of an assignment uses a variable
            if len(node.children) > 0:
                self._collect_usages(node.children[0])
        
        # Recursively process children
        if hasattr(node, 'children'):
            for child in node.children:
                self._collect_usages(child)


# Optimizer manager to run all optimization passes
class OptimizerManager:
    def __init__(self, ast):
        self.ast = ast
        self.passes = []
        self.warnings = []
        
    def add_pass(self, optimizer_class):
        self.passes.append(optimizer_class)
        
    def run_optimizations(self):
        total_optimizations = 0
        
        # Keep running passes until no more optimizations are possible
        while True:
            pass_optimized = False
            
            for optimizer_class in self.passes:
                optimizer = optimizer_class(self.ast)
                self.ast = optimizer.optimize()
                
                if optimizer.was_optimized():
                    pass_optimized = True
                    total_optimizations += 1
                
                # Collect warnings if supported
                if hasattr(optimizer, 'get_warnings'):
                    self.warnings.extend(optimizer.get_warnings())
            
            # If no pass made an optimization, we're done
            if not pass_optimized:
                break
        
        return self.ast, self.warnings, total_optimizations