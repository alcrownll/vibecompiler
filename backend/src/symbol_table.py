from typing import Dict, Optional, List
from .errors import SemanticError

class Symbol:
    def __init__(self, name: str, type: str, scope_level: int, is_function: bool = False):
        self.name = name
        self.type = type
        self.scope_level = scope_level
        self.is_function = is_function
        self.parameters: List[str] = []  # For functions
        self.initialized = False

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.scope_stack: List[Dict[str, Symbol]] = [{}]
        self.current_scope_level = 0

    def enter_scope(self):
        """Enter a new scope level"""
        self.current_scope_level += 1
        self.scope_stack.append({})

    def exit_scope(self):
        """Exit the current scope level"""
        if self.current_scope_level > 0:
            self.scope_stack.pop()
            self.current_scope_level -= 1
            # Remove symbols from the current scope
            self.symbols = {name: sym for name, sym in self.symbols.items() 
                          if sym.scope_level <= self.current_scope_level}

    def declare_symbol(self, name: str, type: str, is_function: bool = False) -> Symbol:
        """Declare a new symbol in the current scope"""
        if name in self.scope_stack[-1]:
            raise SemanticError(f"Symbol '{name}' already declared in this scope")
        
        symbol = Symbol(name, type, self.current_scope_level, is_function)
        self.scope_stack[-1][name] = symbol
        self.symbols[name] = symbol
        return symbol

    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in the current and outer scopes"""
        # Search from innermost to outermost scope
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None

    def mark_initialized(self, name: str):
        """Mark a symbol as initialized"""
        symbol = self.lookup_symbol(name)
        if symbol:
            symbol.initialized = True

    def is_initialized(self, name: str) -> bool:
        """Check if a symbol is initialized"""
        symbol = self.lookup_symbol(name)
        return symbol.initialized if symbol else False

    def get_symbol_type(self, name: str) -> Optional[str]:
        """Get the type of a symbol"""
        symbol = self.lookup_symbol(name)
        return symbol.type if symbol else None

    def add_function_parameter(self, func_name: str, param_name: str, param_type: str):
        """Add a parameter to a function symbol"""
        symbol = self.lookup_symbol(func_name)
        if symbol and symbol.is_function:
            symbol.parameters.append((param_name, param_type)) 