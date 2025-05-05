import sys
from lexer import tokenize
from parser import parse_program
from semanticAnalyzer import SemanticAnalyzer

class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = []
        self.current_function = None
    
    def generate(self, ast):
        if ast is None:
            return
            
        method_name = f"gen_{ast.node_type}"
        method = getattr(self, method_name, self.generic_gen)
        return method(ast)
    
    def generic_gen(self, node):
        raise RuntimeError(f"No generation method for {node.node_type}")
    
    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, operation, arg1=None, arg2=None, result=None):
        code_line = {
            'op': operation,
            'arg1': arg1,
            'arg2': arg2,
            'result': result
        }
        self.code.append(code_line)
        return result
    
    def gen_Program(self, node):
        for child in node.children:
            self.generate(child)
    
    def gen_Block(self, node):
        for child in node.children:
            self.generate(child)
    
    def gen_Assignment(self, node):
        var_name = node.value
        expr_result = self.generate(node.children[0])
        self.emit('assign', expr_result, None, var_name)
        return var_name
    
    def gen_Identifier(self, node):
        return node.value
    
    def gen_Number(self, node):
        temp = self.new_temp()
        self.emit('assign', node.value, None, temp)
        return temp
    
    def gen_String(self, node):
        temp = self.new_temp()
        self.emit('assign', f'"{node.value}"', None, temp)
        return temp
    
    def gen_Boolean(self, node):
        temp = self.new_temp()
        value = 'true' if node.value else 'false'
        self.emit('assign', value, None, temp)
        return temp
    
    def gen_Null(self, node):
        temp = self.new_temp()
        self.emit('assign', 'null', None, temp)
        return temp
    
    def gen_BinaryOp(self, node):
        left_result = self.generate(node.children[0])
        right_result = self.generate(node.children[1])
        result = self.new_temp()
        
        # Map the operator to three-address code operation
        op_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            '==': 'eq',
            '!=': 'neq',
            '<': 'lt',
            '>': 'gt',
            '<=': 'lte',
            '>=': 'gte',
            '&&': 'and',
            '||': 'or'
        }
        
        operation = op_map.get(node.value, node.value)
        self.emit(operation, left_result, right_result, result)
        return result
    
    def gen_Print(self, node):
        expr_result = self.generate(node.children[0])
        self.emit('print', expr_result)
        return None
    
    def gen_If(self, node):
        condition_result = self.generate(node.children[0])
        end_label = self.new_label()
        
        # Handle if-elseif-else chains
        has_else = len(node.children) > 2 and node.children[-1] is not None and node.children[-1].node_type != 'ElseIf'
        
        # Generate code for 'if' part
        else_label = self.new_label()
        self.emit('if_false', condition_result, None, else_label)
        self.generate(node.children[1])  # Then-block
        
        if len(node.children) <= 2:  # Simple if with no else
            self.emit('label', None, None, else_label)
            return
            
        self.emit('goto', None, None, end_label)
        self.emit('label', None, None, else_label)
        
        # Handle elseif parts
        for i in range(2, len(node.children)):
            child = node.children[i]
            
            if child is None:
                continue
                
            if child.node_type == 'ElseIf':
                next_else_label = self.new_label()
                
                # Generate elseif condition
                elseif_condition = self.generate(child.children[0])
                self.emit('if_false', elseif_condition, None, next_else_label)
                
                # Generate elseif body
                self.generate(child.children[1])
                self.emit('goto', None, None, end_label)
                self.emit('label', None, None, next_else_label)
            else:
                # This is the else block
                self.generate(child)
                
        if not has_else:
            self.emit('label', None, None, else_label)
            
        self.emit('label', None, None, end_label)
    
    def gen_While(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('label', None, None, start_label)
        
        # Generate condition
        condition_result = self.generate(node.children[0])
        self.emit('if_false', condition_result, None, end_label)
        
        # Generate loop body
        self.generate(node.children[1])
        
        # Jump back to condition check
        self.emit('goto', None, None, start_label)
        self.emit('label', None, None, end_label)
    
    def gen_For(self, node):
        init = node.children[0]
        condition = node.children[1]
        increment = node.children[2]
        body = node.children[3]
        
        start_label = self.new_label()
        condition_label = self.new_label()
        end_label = self.new_label()
        
        # Generate initialization
        if init:
            self.generate(init)
            
        # Jump to condition check
        self.emit('goto', None, None, condition_label)
        
        # Start of loop body
        self.emit('label', None, None, start_label)
        
        # Generate loop body
        self.generate(body)
        
        # Generate increment
        if increment:
            self.generate(increment)
            
        # Condition check
        self.emit('label', None, None, condition_label)
        if condition:
            condition_result = self.generate(condition)
            self.emit('if_true', condition_result, None, start_label)
        else:
            # If no condition, loop forever (typically there will be a break)
            self.emit('goto', None, None, start_label)
            
        self.emit('label', None, None, end_label)
    
    def gen_Break(self, node):
        # In a full compiler, we'd keep track of loop labels and jump to the end of the current loop
        # For simplicity, we'll just emit a 'break' operation
        self.emit('break')
    
    def gen_FunctionDeclaration(self, node):
        function_name = node.value
        parameters_node = node.children[0]
        body_node = node.children[1]
        
        # Start function definition
        self.emit('function', function_name)
        
        # Generate parameters
        parameters = parameters_node.value  # List of parameter names
        for param in parameters:
            self.emit('param', param)
        
        # Save current function name
        old_function = self.current_function
        self.current_function = function_name
        
        # Generate function body
        self.generate(body_node)
        
        # End function definition
        self.emit('end_function')
        
        # Restore previous function name
        self.current_function = old_function
    
    def gen_FunctionCall(self, node):
        function_name = node.value
        arguments = node.children
        
        # Push arguments
        for arg in arguments:
            arg_result = self.generate(arg)
            self.emit('param_push', arg_result)
        
        # Call function
        result = self.new_temp()
        self.emit('call', function_name, len(arguments), result)
        
        return result
    
    def gen_Return(self, node):
        expr_result = self.generate(node.children[0])
        self.emit('return', expr_result)
        return None
        
    def get_code(self):
        return self.code
        
    def print_code(self):
        for i, line in enumerate(self.code):
            if line['op'] == 'label':
                print(f"{line['result']}:")
            else:
                args = []
                if line['arg1'] is not None:
                    args.append(str(line['arg1']))
                if line['arg2'] is not None:
                    args.append(str(line['arg2']))
                    
                if line['result'] is not None:
                    print(f"  {line['result']} = {line['op']} {', '.join(args)}")
                else:
                    print(f"  {line['op']} {', '.join(args)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python intermediate_code_generator.py <source_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    
    try:
        tokens = tokenize(code)
        ast = parse_program(tokens)
        
        # Run semantic analysis first
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Generate intermediate code
        generator = IntermediateCodeGenerator()
        generator.generate(ast)
        
        print("Intermediate Code:")
        generator.print_code()
        print("Intermediate code generation completed successfully.")
    except Exception as e:
        print(f"Error: {e}")