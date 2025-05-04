import sys
from lexer import tokenize
from parser import parse_program

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, var_type):
        if name in self.symbols:
            raise RuntimeError(f"Semantic Error: Variable '{name}' already declared.")
        self.symbols[name] = var_type

    def lookup(self, name):
        if name not in self.symbols:
            raise RuntimeError(f"Semantic Error: Variable '{name}' not declared.")
        return self.symbols[name]

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        method_name = f"visit_{node['type']}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node['type']} method")

    def visit_program(self, node):
        for statement in node['body']:
            self.analyze(statement)

    def visit_declaration(self, node):
        var_type = node['var_type']
        var_name = node['var_name']
        value = node.get('value')
        self.symbol_table.declare(var_name, var_type)
        if value:
            value_type = self.analyze(value)
            if value_type != var_type:
                raise RuntimeError(f"Type Error: Expected {var_type}, got {value_type} in declaration of '{var_name}'")

    def visit_assignment(self, node):
        var_name = node['var_name']
        value = node['value']
        expected_type = self.symbol_table.lookup(var_name)
        actual_type = self.analyze(value)
        if expected_type != actual_type:
            raise RuntimeError(f"Type Error: Expected {expected_type}, got {actual_type} in assignment to '{var_name}'")

    def visit_literal(self, node):
        return node['value_type']

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python semantic_analyzer.py <source_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    ast = parse_program(tokens)

    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    print("Semantic analysis completed successfully.")
