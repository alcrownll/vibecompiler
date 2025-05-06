from typing import List
from .intermediate_code import ThreeAddressCode
from .errors import OptimizationError

class Optimizer:
    def __init__(self):
        self.optimizations = [
            self.constant_folding,
            self.dead_code_elimination,
            self.common_subexpression_elimination
        ]

    def optimize(self, code: List[ThreeAddressCode]) -> List[ThreeAddressCode]:
        """Apply all optimizations to the code"""
        optimized_code = code.copy()
        changed = True
        
        while changed:
            changed = False
            for optimization in self.optimizations:
                new_code, was_changed = optimization(optimized_code)
                if was_changed:
                    optimized_code = new_code
                    changed = True
                    break
        
        return optimized_code

    def constant_folding(self, code: List[ThreeAddressCode]) -> tuple[List[ThreeAddressCode], bool]:
        """Fold constant expressions"""
        changed = False
        new_code = []
        
        for instr in code:
            if instr.op in ['+', '-', '*', '/']:
                try:
                    # Try to evaluate the expression
                    if instr.arg1.isdigit() and instr.arg2.isdigit():
                        if instr.op == '+':
                            result = str(int(instr.arg1) + int(instr.arg2))
                        elif instr.op == '-':
                            result = str(int(instr.arg1) - int(instr.arg2))
                        elif instr.op == '*':
                            result = str(int(instr.arg1) * int(instr.arg2))
                        elif instr.op == '/':
                            result = str(int(instr.arg1) // int(instr.arg2))
                        
                        # Replace with a simple assignment
                        new_code.append(ThreeAddressCode('=', result, None, instr.result))
                        changed = True
                        continue
                except:
                    pass
            new_code.append(instr)
        
        return new_code, changed

    def dead_code_elimination(self, code: List[ThreeAddressCode]) -> tuple[List[ThreeAddressCode], bool]:
        """Remove dead code (unused assignments)"""
        changed = False
        new_code = []
        used_vars = set()
        
        # First pass: collect used variables
        for instr in reversed(code):
            if instr.op == '=':
                if instr.result not in used_vars:
                    # This assignment is dead
                    changed = True
                    continue
            else:
                if instr.arg1:
                    used_vars.add(instr.arg1)
                if instr.arg2:
                    used_vars.add(instr.arg2)
            new_code.insert(0, instr)
        
        return new_code, changed

    def common_subexpression_elimination(self, code: List[ThreeAddressCode]) -> tuple[List[ThreeAddressCode], bool]:
        """Eliminate common subexpressions"""
        changed = False
        new_code = []
        expression_map = {}  # Maps expressions to their result variables
        
        for instr in code:
            if instr.op in ['+', '-', '*', '/']:
                expr_key = (instr.op, instr.arg1, instr.arg2)
                if expr_key in expression_map:
                    # Replace with a copy of the previous result
                    new_code.append(ThreeAddressCode('=', expression_map[expr_key], None, instr.result))
                    changed = True
                else:
                    expression_map[expr_key] = instr.result
                    new_code.append(instr)
            else:
                new_code.append(instr)
        
        return new_code, changed 