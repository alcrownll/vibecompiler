from typing import List, Dict, Optional
from .parser import ASTNode

class ThreeAddressCode:
    def __init__(self, op: str, arg1: Optional[str] = None, arg2: Optional[str] = None, result: Optional[str] = None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        if self.op in ['LABEL', 'GOTO']:
            return f"{self.op} {self.arg1}"
        elif self.op in ['IF', 'IF_FALSE']:
            return f"{self.op} {self.arg1} GOTO {self.arg2}"
        elif self.op in ['PARAM', 'CALL']:
            return f"{self.op} {self.arg1}"
        elif self.op == 'RETURN':
            return f"RETURN {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

class IntermediateCodeGenerator:
    def __init__(self):
        self.code: List[ThreeAddressCode] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table: Dict[str, str] = {}  # Maps variable names to their types
        self.debug = True  # Enable debug mode

    def debug_print(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    def generate(self, ast: ASTNode) -> List[ThreeAddressCode]:
        self.visit(ast)
        self.debug_print("Generated intermediate code:")
        for instr in self.code:
            self.debug_print(f"  {instr}")
        return self.code

    def new_temp(self) -> str:
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        self.debug_print(f"Created new temporary variable: {temp}")
        return temp

    def new_label(self) -> str:
        label = f"L{self.label_counter}"
        self.label_counter += 1
        self.debug_print(f"Created new label: {label}")
        return label

    def visit(self, node: ASTNode):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        for child in node.children:
            self.visit(child)

    def visit_PROGRAM(self, node: ASTNode):
        for child in node.children:
            self.visit(child)

    def visit_VAR_DECL(self, node: ASTNode):
        var_type = node.value
        name = node.children[0].value
        self.symbol_table[name] = var_type
        
        if len(node.children) > 1:
            value = self.visit(node.children[1])
            if var_type == 'ARRAY_TYPE':
                # Store the array as a string representation for now
                self.code.append(ThreeAddressCode('=', value, None, name))
            else:
                self.code.append(ThreeAddressCode('=', value, None, name))

    def visit_FUNCTION(self, node: ASTNode):
        func_name = node.value
        params = node.children[0].children
        body = node.children[1]
        
        # Function entry
        self.code.append(ThreeAddressCode('LABEL', func_name))
        
        # Process parameters
        for param in params:
            self.symbol_table[param.value] = 'PARAM'
        
        # Process function body
        for statement in body.children:
            self.visit(statement)

    def visit_IF(self, node: ASTNode):
        condition = self.visit(node.children[0])
        else_label = self.new_label()
        end_label = self.new_label()
        
        # If condition is false, jump to else or end
        self.code.append(ThreeAddressCode('IF_FALSE', condition, else_label))
        
        # Process if body
        for statement in node.children[1].children:
            self.visit(statement)
        
        # Jump to end after if body
        self.code.append(ThreeAddressCode('GOTO', end_label))
        
        # Else label and body
        self.code.append(ThreeAddressCode('LABEL', else_label))
        if len(node.children) > 2:
            for statement in node.children[2].children:
                self.visit(statement)
        
        # End label
        self.code.append(ThreeAddressCode('LABEL', end_label))

    def visit_WHILE(self, node: ASTNode):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.debug_print(f"Generating while loop with start label {start_label} and end label {end_label}")
        
        # Start of loop
        self.code.append(ThreeAddressCode('LABEL', start_label))
        
        # Evaluate condition
        condition = self.visit(node.children[0])
        self.debug_print(f"While condition: {condition}")
        
        # If condition is false, jump to end
        self.code.append(ThreeAddressCode('IF_FALSE', condition, end_label))
        
        # Process loop body
        self.debug_print("Generating while loop body")
        for statement in node.children[1].children:
            self.visit(statement)
        
        # Update loop variable
        if node.children[0].type == 'BINARY_OP' and node.children[0].value == '<':
            # For i < N pattern, increment i
            left_var = node.children[0].children[0].value
            temp = self.new_temp()
            self.code.append(ThreeAddressCode('=', left_var, None, temp))
            self.code.append(ThreeAddressCode('+', temp, '1', temp))
            self.code.append(ThreeAddressCode('=', temp, None, left_var))
        
        # Jump back to start
        self.code.append(ThreeAddressCode('GOTO', start_label))
        
        # End label
        self.code.append(ThreeAddressCode('LABEL', end_label))

    def visit_FOR(self, node: ASTNode):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.debug_print(f"Generating for loop with start label {start_label} and end label {end_label}")
        
        # Process initialization
        self.debug_print("Generating for loop initialization")
        self.visit(node.children[0])
        
        # Start of loop
        self.code.append(ThreeAddressCode('LABEL', start_label))
        
        # Evaluate condition
        condition = self.visit(node.children[1])
        self.debug_print(f"For condition: {condition}")
        
        # If condition is false, jump to end
        self.code.append(ThreeAddressCode('IF_FALSE', condition, end_label))
        
        # Process loop body
        self.debug_print("Generating for loop body")
        for statement in node.children[3].children:
            self.visit(statement)
        
        # Process update
        self.debug_print("Generating for loop update")
        # Get the loop variable from the initialization
        init_node = node.children[0]
        if init_node.type == 'VAR_DECL':
            loop_var = init_node.children[0].value
            # Create temporary for the update
            temp = self.new_temp()
            self.code.append(ThreeAddressCode('=', loop_var, None, temp))
            self.code.append(ThreeAddressCode('+', temp, '1', temp))
            self.code.append(ThreeAddressCode('=', temp, None, loop_var))
        
        # Jump back to start
        self.code.append(ThreeAddressCode('GOTO', start_label))
        
        # End label
        self.code.append(ThreeAddressCode('LABEL', end_label))

    def visit_BINARY_OP(self, node: ASTNode) -> str:
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        result = self.new_temp()
        
        self.debug_print(f"Generating binary operation: {left} {node.value} {right} -> {result}")
        
        # Handle comparison operators
        if node.value in ['<', '>', '<=', '>=', '==', '!=', '<>']:
            # For comparisons, we need to evaluate both sides and compare
            left_temp = self.new_temp()
            right_temp = self.new_temp()
            self.code.append(ThreeAddressCode('=', left, None, left_temp))
            self.code.append(ThreeAddressCode('=', right, None, right_temp))
            self.code.append(ThreeAddressCode(node.value, left_temp, right_temp, result))
        else:
            # Regular arithmetic operations
            self.code.append(ThreeAddressCode(node.value, left, right, result))
        return result

    def visit_IDENTIFIER(self, node: ASTNode) -> str:
        return node.value

    def visit_LITERAL(self, node: ASTNode) -> str:
        return node.value

    def visit_PRINT(self, node: ASTNode):
        value = self.visit(node.children[0])
        self.code.append(ThreeAddressCode('PRINT', value))

    def visit_ARRAY_LITERAL(self, node: ASTNode) -> str:
        # Return a string representation of the array for now
        elements = [self.visit(child) for child in node.children]
        return '[' + ','.join(elements) + ']'

    def optimize(self):
        # Simple constant folding optimization
        i = 0
        while i < len(self.code):
            instr = self.code[i]
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
                        
                        # Replace the instruction with a simple assignment
                        self.code[i] = ThreeAddressCode('=', result, None, instr.result)
                except:
                    pass
            i += 1 