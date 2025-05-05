def enhanced_tokenize(code):
    tokens = []
    error_collector = ErrorCollector()
    line_num = 1
    line_start = 0
    
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
        ('TRY',         r'tryhard-flopped'),
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
        ('COMMENT',     r'~.*'),
        ('NEWLINE',     r'\n'),
        ('SKIP',        r'[ \t]+'),
        ('MISMATCH',    r'.'),
    ]
    
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    
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
            error_collector.add_error(LexicalError(
                line_num, 
                column, 
                f"Unexpected character '{value}'"
            ))
        elif kind == 'STRING' and '\\' in value:
            # Check for valid escape sequences
            invalid_escapes = re.findall(r'\\[^"\\nt]', value)
            if invalid_escapes:
                error_collector.add_error(LexicalError(
                    line_num,
                    column,
                    f"Invalid escape sequence(s): {''.join(invalid_escapes)}"
                ))
        
        # Check for unclosed strings
        if kind == 'STRING' and not (value.startswith('"') and value.endswith('"')):
            error_collector.add_error(LexicalError(
                line_num,
                column,
                "Unclosed string literal"
            ))
        
        # Add valid token to list
        if kind != 'MISMATCH':
            tokens.append((kind, value, line_num, column))
    
    return tokens, error_collector

# ======= CODE OPTIMIZATION =======

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
        from ast import ASTNode  # Import locally to avoid circular imports
        
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
                    from ast import ASTNode  # Import locally
                    return ASTNode('Block', children=[])
        
        # Handle while loops with constant false conditions
        if node.node_type == 'While':
            condition = node.children[0]
            
            if condition.node_type == 'Boolean' and condition.value is False:
                self.optimized = True
                # Return an empty block instead of the loop
                from ast import ASTNode
                return ASTNode('Block', children=[])
        
        return node

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

# ======= INTEGRATION WITH COMPILER PIPELINE =======

class CompilerPipeline:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = None
        self.ast = None
        self.ir_code = None
        self.target_code = None
        self.error_collector = ErrorCollector()
        self.optimization_stats = {}
        
    def run(self):
        try:
            # Step 1: Lexical Analysis with error handling
            tokens, lex_errors = enhanced_tokenize(self.source_code)
            self.tokens = tokens
            
            # Add lexical errors to our collector
            for error in lex_errors.errors:
                self.error_collector.add_error(error)
            
            if self.error_collector.has_errors():
                return False, self.error_collector.get_json_output()
            
            # Step 2: Parsing
            from parser import parse_program
            try:
                self.ast = parse_program(self.tokens)
            except Exception as e:
                # Convert parser exceptions to our error format
                if hasattr(e, 'line') and hasattr(e, 'column'):
                    self.error_collector.add_error(SyntaxError(
                        e.line, e.column, str(e)
                    ))
                else:
                    # Default to first token position if no line info
                    self.error_collector.add_error(SyntaxError(
                        self.tokens[0][2] if self.tokens else 1,
                        self.tokens[0][3] if self.tokens else 0,
                        str(e)
                    ))
                return False, self.error_collector.get_json_output()
            
            # Step 3: Semantic Analysis
            from semanticAnalyzer import SemanticAnalyzer
            analyzer = SemanticAnalyzer()
            try:
                analyzer.analyze(self.ast)
            except Exception as e:
                # Convert semantic errors
                if hasattr(e, 'line') and hasattr(e, 'column'):
                    self.error_collector.add_error(SemanticError(
                        e.line, e.column, str(e)
                    ))
                else:
                    self.error_collector.add_error(SemanticError(
                        1, 0, str(e)
                    ))
                return False, self.error_collector.get_json_output()
            
            # Step 4: Code Optimization
            optimizer = OptimizerManager(self.ast)
            optimizer.add_pass(ConstantFolding)
            optimizer.add_pass(DeadCodeElimination)
            optimizer.add_pass(UnusedCodeAnalyzer)
            
            self.ast, warnings, opt_count = optimizer.run_optimizations()
            
            # Add optimization warnings
            for warning in warnings:
                self.error_collector.add_error(warning)
            
            self.optimization_stats = {
                "total_optimizations": opt_count
            }
            
            # Step 5: Intermediate Code Generation
            from intermediateCodeGenerator import IntermediateCodeGenerator
            ir_gen = IntermediateCodeGenerator()
            ir_gen.generate(self.ast)
            self.ir_code = ir_gen.get_code()
            
            # Step 6: Target Code Generation
            from codeGenerator import CodeGenerator
            code_gen = CodeGenerator(self.ir_code)
            code_gen.generate()
            self.target_code = code_gen.get_assembly()
            
            return True, {
                "target_code": self.target_code,
                "optimization_stats": self.optimization_stats,
                "warnings": [w.to_dict() for w in self.error_collector.warnings]
            }
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            tb = traceback.format_exc()
            logger.error(f"Compilation error: {error_msg}\n{tb}")
            
            # Add as generic error if we haven't caught it earlier
            if not self.error_collector.has_errors():
                self.error_collector.add_error(CompilerError(
                    1, 0, f"Internal compiler error: {error_msg}", "INTERNAL", "error"
                ))
            
            return False, self.error_collector.get_json_output()

# Update Flask route to use the enhanced compiler pipeline
def compile_vibe_enhanced(source):
    """Enhanced compile function for Flask route"""
    compiler = CompilerPipeline(source)
    success, result = compiler.run()
    
    return {
        'success': success,
        'result': result
    }