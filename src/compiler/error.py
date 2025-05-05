"""
Error handling module for VibeScript compiler.
Provides classes for different types of errors and a collector to manage them.
"""

import json
from enum import Enum


class ErrorType(Enum):
    LEXICAL = "lexical"
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    INTERNAL = "internal"
    WARNING = "warning"


class CompilerError:
    """Base class for all compiler errors"""
    
    def __init__(self, line, column, message, error_code="GENERIC", severity="error"):
        self.line = line
        self.column = column
        self.message = message
        self.error_code = error_code
        self.severity = severity  # "error" or "warning"
    
    def __str__(self):
        return f"{self.severity.upper()} at line {self.line}, column {self.column}: {self.message}"
    
    def to_dict(self):
        """Convert error to dictionary for JSON serialization"""
        return {
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "code": self.error_code,
            "severity": self.severity
        }


class LexicalError(CompilerError):
    """Error during lexical analysis (tokenization)"""
    
    def __init__(self, line, column, message):
        super().__init__(line, column, message, "LEX_ERROR", "error")


class SyntaxError(CompilerError):
    """Error during syntax analysis (parsing)"""
    
    def __init__(self, line, column, message):
        super().__init__(line, column, message, "SYNTAX_ERROR", "error")


class SemanticError(CompilerError):
    """Error during semantic analysis"""
    
    def __init__(self, line, column, message, error_code="SEM_ERROR"):
        super().__init__(line, column, message, error_code, "error")


class Warning(CompilerError):
    """Warning message that doesn't prevent compilation"""
    
    def __init__(self, line, column, message, error_code="WARNING"):
        super().__init__(line, column, message, error_code, "warning")


class ErrorCollector:
    """Collects and manages errors during compilation"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, error):
        """Add an error or warning to the collector"""
        if error.severity == "warning":
            self.warnings.append(error)
        else:
            self.errors.append(error)
    
    def has_errors(self):
        """Check if there are any errors (not warnings)"""
        return len(self.errors) > 0
    
    def has_warnings(self):
        """Check if there are any warnings"""
        return len(self.warnings) > 0
    
    def get_all(self):
        """Get all errors and warnings"""
        return self.errors + self.warnings
    
    def get_formatted_output(self):
        """Get human-readable output of all errors and warnings"""
        result = []
        
        if self.has_errors():
            result.append("ERRORS:")
            for error in self.errors:
                result.append(f"  {str(error)}")
        
        if self.has_warnings():
            result.append("WARNINGS:")
            for warning in self.warnings:
                result.append(f"  {str(warning)}")
        
        return "\n".join(result)
    
    def get_json_output(self):
        """Get JSON-serializable output of all errors and warnings"""
        return {
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings]
        }


class DebugHelper:
    """Provides debugging utilities for the compiler"""
    
    @staticmethod
    def token_stream_debug(tokens):
        """Generate a human-readable representation of token stream"""
        result = []
        result.append("TOKEN STREAM:")
        
        for token in tokens:
            kind, value, line, column = token
            result.append(f"  {kind:15} '{value}' at line {line}, column {column}")
        
        return "\n".join(result)
    
    @staticmethod
    def ast_debug(ast_node, indent=0):
        """Generate a human-readable representation of AST"""
        if ast_node is None:
            return "None"
        
        result = []
        indent_str = "  " * indent
        
        # Get node type and value
        node_info = f"{ast_node.node_type}"
        if hasattr(ast_node, 'value') and ast_node.value is not None:
            node_info += f": {ast_node.value}"
        
        result.append(f"{indent_str}{node_info}")
        
        # Process children recursively
        if hasattr(ast_node, 'children'):
            for child in ast_node.children:
                result.append(DebugHelper.ast_debug(child, indent + 1))
        
        return "\n".join(result)
    
    @staticmethod
    def highlight_error_in_code(source_code, line, column, context_lines=2):
        """Generate error highlighting in source code"""
        lines = source_code.split('\n')
        
        # Adjust for 1-based indexing to 0-based
        line_idx = max(0, min(line - 1, len(lines) - 1))
        
        start_line = max(0, line_idx - context_lines)
        end_line = min(len(lines), line_idx + context_lines + 1)
        
        result = []
        result.append("ERROR CONTEXT:")
        
        for i in range(start_line, end_line):
            line_num = i + 1
            prefix = "-> " if i == line_idx else "   "
            result.append(f"{prefix}{line_num}: {lines[i]}")
            
            # Add error pointer
            if i == line_idx:
                result.append("   " + " " * column + "^")
        
        return "\n".join(result)