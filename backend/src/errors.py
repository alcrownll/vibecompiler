from typing import Optional, List, Tuple, Any

class CompilerError(Exception):
    """Base class for all compiler errors"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.node = node
        self.code_snippet = code_snippet
        
    def __str__(self):
        if self.line is not None and self.column is not None:
            return f"Error at line {self.line}, column {self.column}: {self.message}"
        return self.message

class LexicalError(CompilerError):
    """Errors during lexical analysis - 'not vibing' token errors"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"main character syndrome: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class SyntaxError(CompilerError):
    """Errors during syntax analysis - 'not vibing' structure errors"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"not vibing: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class SemanticError(CompilerError):
    """Errors during semantic analysis - 'sus behavior' warnings"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"sus behavior: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class TypeError(SemanticError):
    """Type-related semantic errors"""
    def __init__(self, message: str, expected_type: str, actual_type: str, 
                 line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"lowkey caught in 4K: expected {expected_type}, got {actual_type}. {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class NameError(SemanticError):
    """Variable/function name related errors"""
    def __init__(self, name: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"ghosted reference: '{name}' isn't in the vibe"
        super().__init__(vibe_message, line, column, node, code_snippet)

class ScopeError(SemanticError):
    """Scope-related semantic errors"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"out of pocket: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class CodeGenerationError(CompilerError):
    """Errors during code generation"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"big yikes: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class OptimizationError(CompilerError):
    """Errors during code optimization"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"mid behavior: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class RuntimeError(CompilerError):
    """Errors during program execution"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        vibe_message = f"dead fr: {message}"
        super().__init__(vibe_message, line, column, node, code_snippet)

class DivisionByZeroError(RuntimeError):
    """Division by zero runtime error"""
    def __init__(self, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        super().__init__("dividing by zero? that's cap fr fr", line, column, node, code_snippet)

class IndexError(RuntimeError):
    """Array index out of bounds error"""
    def __init__(self, index: int, array_size: int, line: Optional[int] = None, 
                 column: Optional[int] = None, node: Any = None, 
                 code_snippet: Optional[str] = None):
        super().__init__(f"gang member {index} got ghosted (gang size is {array_size})", 
                        line, column, node, code_snippet)

class IOError(RuntimeError):
    """Input/output related errors"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, 
                 node: Any = None, code_snippet: Optional[str] = None):
        super().__init__(f"tea spilled: {message}", line, column, node, code_snippet)

def format_error(error: CompilerError) -> str:
    """Format an error message with location information and code snippet"""
    message = str(error)
    
    if error.code_snippet:
        message += f"\n\n{error.code_snippet}"
        if error.line is not None and error.column is not None:
            # Add a marker pointing to the error location
            pointer = ' ' * (error.column - 1) + '^'
            message += f"\n{pointer}"
    
    return message

def get_code_snippet(code: str, line: int, context_lines: int = 1) -> str:
    """Extract code snippet around the error location"""
    lines = code.split('\n')
    start = max(0, line - context_lines - 1)
    end = min(len(lines), line + context_lines)
    
    result = []
    for i in range(start, end):
        line_number = i + 1
        prefix = f"{line_number}: " if line_number == line else f"{line_number}| "
        result.append(prefix + lines[i])
    
    return '\n'.join(result)


