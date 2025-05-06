from typing import Optional
from .parser import ASTNode

class CompilerError(Exception):
    """Base class for all compiler errors"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, node: Optional[ASTNode] = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.node = node

    def __str__(self):
        if self.line is not None and self.column is not None:
            return f"Error at line {self.line}, column {self.column}: {self.message}"
        return self.message

class LexicalError(CompilerError):
    """Errors during lexical analysis"""
    pass

class SyntaxError(CompilerError):
    """Errors during syntax analysis"""
    pass

class SemanticError(CompilerError):
    """Errors during semantic analysis"""
    pass

class CodeGenerationError(CompilerError):
    """Errors during code generation"""
    pass

class OptimizationError(CompilerError):
    """Errors during code optimization"""
    pass

class RuntimeError(CompilerError):
    """Errors during program execution"""
    pass

def format_error(error: CompilerError) -> str:
    """Format an error message with location information"""
    if error.line is not None and error.column is not None:
        return f"Error at line {error.line}, column {error.column}: {error.message}"
    return str(error) 