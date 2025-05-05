import sys
from lexer import tokenize
from parser import parse_program
from semanticAnalyzer import SemanticAnalyzer
from intermediateCodeGenerator import IntermediateCodeGenerator

class CodeGenerator:
    def __init__(self, ir_code):
        self.ir_code = ir_code
        self.assembly = []
        self.globals = set()
        self.current_function = None
        self.stack_offset = 0
        self.variable_map = {}  # Maps variables to memory locations
        self.temp_map = {}      # Maps temporary registers to memory locations
        self.label_counter = 0
        
    def generate(self):
        # Add some initial boilerplate
        self.emit(".section .text")
        self.emit(".global _start")
        self.emit("_start:")
        
        # Call the main function if it exists
        self.emit("  call main")
        
        # Exit the program
        self.emit("  mov eax, 1")       # syscall number for exit
        self.emit("  xor ebx, ebx")     # exit code 0
        self.emit("  int 0x80")         # call kernel
        
        # Process the IR code
        i = 0
        while i < len(self.ir_code):
            instr = self.ir_code[i]
            
            if instr['op'] == 'function':
                i = self.process_function(i)
            elif instr['op'] == 'label':
                self.emit(f"{instr['result']}:")
                i += 1
            else:
                # Skip non-function instructions at global scope
                i += 1
        
        # Add global variable declarations
        if self.globals:
            self.emit("\n.section .data")
            for var in self.globals:
                self.emit(f"{var}: .word 0")
        
        # Add string literals
        for instr in self.ir_code:
            if instr['op'] == 'assign' and isinstance(instr['arg1'], str) and instr['arg1'].startswith('"'):
                # Extract string without quotes
                string_value = instr['arg1'][1:-1]
                label = f"str_{self.label_counter}"
                self.label_counter += 1
                self.emit(f"{label}: .ascii \"{string_value}\\0\"")
                
                # Update the IR instruction to use the label
                instr['arg1'] = label
        
        return self.assembly
    
    def process_function(self, start_index):
        """Process a function definition and return the index after it"""
        func_instr = self.ir_code[start_index]
        func_name = func_instr['arg1']
        
        self.current_function = func_name
        self.stack_offset = 0
        self.variable_map = {}
        self.temp_map = {}
        
        # Emit function label
        self.emit(f"\n{func_name}:")
        
        # Function prologue
        self.emit("  push ebp")
        self.emit("  mov ebp, esp")
        
        # Process parameters
        param_count = 0
        i = start_index + 1
        while i < len(self.ir_code) and self.ir_code[i]['op'] == 'param':
            param_name = self.ir_code[i]['arg1']
            self.variable_map[param_name] = 8 + (param_count * 4)  # Parameters are above the return address and old ebp
            param_count += 1
            i += 1
        
        # Allocate space for local variables (we'll update this later)
        local_vars_index = len(self.assembly)
        self.emit("  sub esp, 0")  # Placeholder for local vars
        
        # Process function body
        while i < len(self.ir_code):
            instr = self.ir_code[i]
            if instr['op'] == 'end_function':
                break
                
            self.generate_instruction(instr)
            i += 1
        
        # Function epilogue (for non-void functions, the return value should be in eax)
        epilogue_label = f".L{func_name}_epilogue"
        self.emit(f"{epilogue_label}:")
        self.emit("  mov esp, ebp")
        self.emit("  pop ebp")
        self.emit("  ret")
        
        # Update the local variables space allocation
        local_vars_size = abs(self.stack_offset) if self.stack_offset < 0 else 0
        if local_vars_size > 0:
            self.assembly[local_vars_index] = f"  sub esp, {local_vars_size}"
        
        return i + 1  # Skip the end_function instruction
    
    def generate_instruction(self, instr):
        op = instr['op']
        
        if op == 'assign':
            self.gen_assign(instr)
        elif op in ['add', 'sub', 'mul', 'div']:
            self.gen_arithmetic(instr)
        elif op in ['eq', 'neq', 'lt', 'gt', 'lte', 'gte']:
            self.gen_comparison(instr)
        elif op in ['and', 'or']:
            self.gen_logical(instr)
        elif op == 'if_true':
            self.gen_if_true(instr)
        elif op == 'if_false':
            self.gen_if_false(instr)
        elif op == 'goto':
            self.gen_goto(instr)
        elif op == 'label':
            self.emit(f"{instr['result']}:")
        elif op == 'call':
            self.gen_call(instr)
        elif op == 'param_push':
            self.gen_param_push(instr)
        elif op == 'return':
            self.gen_return(instr)
        elif op == 'print':
            self.gen_print(instr)
        elif op == 'break':
            self.gen_break(instr)
        else:
            self.emit(f"  # Unimplemented operation: {op}")
    
    def gen_assign(self, instr):
        dest = instr['result']
        src = instr['arg1']
        
        # Check if assigning a literal value
        if isinstance(src, (int, float)):
            self.emit(f"  mov eax, {src}")
            self.store_variable(dest, 'eax')
        elif isinstance(src, str) and src.startswith('"'):
            # String literal (address)
            str_label = src[1:-1]  # Remove quotes
            self.emit(f"  lea eax, [{str_label}]")
            self.store_variable(dest, 'eax')
        elif src in ['true', 'false']:
            # Boolean literal
            value = 1 if src == 'true' else 0
            self.emit(f"  mov eax, {value}")
            self.store_variable(dest, 'eax')
        elif src == 'null':
            # Null literal
            self.emit("  xor eax, eax")
            self.store_variable(dest, 'eax')
        else:
            # Variable or temp register
            self.load_variable(src, 'eax')
            self.store_variable(dest, 'eax')
    
    def gen_arithmetic(self, instr):
        op = instr['op']
        arg1 = instr['arg1']
        arg2 = instr['arg2']
        result = instr['result']
        
        # Load first operand into eax
        self.load_variable(arg1, 'eax')
        
        # Load second operand into ebx
        self.load_variable(arg2, 'ebx')
        
        # Perform operation
        if op == 'add':
            self.emit("  add eax, ebx")
        elif op == 'sub':
            self.emit("  sub eax, ebx")
        elif op == 'mul':
            self.emit("  imul eax, ebx")
        elif op == 'div':
            self.emit("  cdq")  # Sign-extend eax into edx:eax
            self.emit("  idiv ebx")
        
        # Store result
        self.store_variable(result, 'eax')
    
    def gen_comparison(self, instr):
        op = instr['op']
        arg1 = instr['arg1']
        arg2 = instr['arg2']
        result = instr['result']
        
        # Load operands
        self.load_variable(arg1, 'eax')
        self.load_variable(arg2, 'ebx')
        
        # Compare
        self.emit("  cmp eax, ebx")
        
        # Set result based on condition
        op_map = {
            'eq': 'e',   # Equal
            'neq': 'ne', # Not equal
            'lt': 'l',   # Less than
            'gt': 'g',   # Greater than
            'lte': 'le', # Less than or equal
            'gte': 'ge'  # Greater than or equal
        }
        
        condition = op_map[op]
        self.emit(f"  set{condition} cl")
        self.emit("  movzx eax, cl")  # Zero-extend cl into eax
        
        # Store result
        self.store_variable(result, 'eax')
    
    def gen_logical(self, instr):
        op = instr['op']
        arg1 = instr['arg1']
        arg2 = instr['arg2']
        result = instr['result']
        
        # Load operands
        self.load_variable(arg1, 'eax')
        self.load_variable(arg2, 'ebx')
        
        # Perform logical operation
        if op == 'and':
            self.emit("  and eax, ebx")
        elif op == 'or':
            self.emit("  or eax, ebx")
        
        # Store result
        self.store_variable(result, 'eax')
    
    def gen_if_true(self, instr):
        condition = instr['arg1']
        label = instr['result']
        
        # Load condition
        self.load_variable(condition, 'eax')
        
        # Test if true
        self.emit("  test eax, eax")
        self.emit(f"  jnz {label}")
    
    def gen_if_false(self, instr):
        condition = instr['arg1']
        label = instr['result']
        
        # Load condition
        self.load_variable(condition, 'eax')
        
        # Test if false
        self.emit("  test eax, eax")
        self.emit(f"  jz {label}")
    
    def gen_goto(self, instr):
        label = instr['result']
        self.emit(f"  jmp {label}")
    
    def gen_call(self, instr):
        func_name = instr['arg1']
        num_args = instr['arg2']
        result = instr['result']
        
        # Call the function
        self.emit(f"  call {func_name}")
        
        # Clean up the stack (caller clean-up convention)
        if num_args > 0:
            self.emit(f"  add esp, {num_args * 4}")
        
        # Store the result
        if result is not None:
            self.store_variable(result, 'eax')
    
    def gen_param_push(self, instr):
        arg = instr['arg1']
        self.load_variable(arg, 'eax')
        self.emit("  push eax")
    
    def gen_return(self, instr):
        value = instr['arg1']
        if value is not None:
            self.load_variable(value, 'eax')
        
        # Jump to epilogue
        self.emit(f"  jmp .L{self.current_function}_epilogue")
    
    def gen_print(self, instr):
        value = instr['arg1']
        self.load_variable(value, 'eax')
        
        # For simplicity, we'll just print the number (further implementation would handle different types)
        self.emit("  push eax")
        self.emit("  call print_int")  # We'll define this function later
        self.emit("  add esp, 4")  # Clean up stack
    
    def gen_break(self, instr):
        # This is a simplification - in real code, we would need to jump to the end of the current loop
        self.emit("  # break statement - in real code, jump to end of loop")
    
    def load_variable(self, var, reg):
        """Load variable into register"""
        if isinstance(var, (int, float)):
            # Immediate value
            self.emit(f"  mov {reg}, {var}")
        elif var in self.variable_map:
            # Local variable
            offset = self.variable_map[var]
            self.emit(f"  mov {reg}, [ebp+{offset}]" if offset > 0 else f"  mov {reg}, [ebp{offset}]")
        elif var in self.temp_map:
            # Temporary variable
            offset = self.temp_map[var]
            self.emit(f"  mov {reg}, [ebp{offset}]")
        else:
            # Global variable
            self.globals.add(var)
            self.emit(f"  mov {reg}, [{var}]")
    
    def store_variable(self, var, reg):
        """Store register value into variable"""
        if var in self.variable_map:
            # Local variable
            offset = self.variable_map[var]
            self.emit(f"  mov [ebp+{offset}], {reg}" if offset > 0 else f"  mov [ebp{offset}], {reg}")
        elif var in self.temp_map:
            # Temporary variable
            offset = self.temp_map[var]
            self.emit(f"  mov [ebp{offset}], {reg}")
        elif var.startswith('t'):
            # New temporary variable
            self.stack_offset -= 4
            self.temp_map[var] = self.stack_offset
            self.emit(f"  mov [ebp{self.stack_offset}], {reg}")
        else:
            # Global variable
            self.globals.add(var)
            self.emit(f"  mov [{var}], {reg}")
    
    def emit(self, asm):
        self.assembly.append(asm)
    
    def get_assembly(self):
        # Add helper functions
        self.emit("\n# Helper functions")
        self.emit("print_int:")
        self.emit("  push ebp")
        self.emit("  mov ebp, esp")
        self.emit("  # Simple implementation to print integer in eax")
        self.emit("  # In a real implementation, this would convert to string and call write syscall")
        self.emit("  mov eax, [ebp+8]")
        self.emit("  add eax, '0'")
        self.emit("  push eax")
        self.emit("  mov eax, 4")         # write syscall
        self.emit("  mov ebx, 1")         # stdout
        self.emit("  mov ecx, esp")       # buffer
        self.emit("  mov edx, 1")         # count
        self.emit("  int 0x80")
        self.emit("  add esp, 4")         # clean up stack
        self.emit("  mov esp, ebp")
        self.emit("  pop ebp")
        self.emit("  ret")
        
        return '\n'.join(self.assembly)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python code_generator.py <source_file> [output_file]")
        sys.exit(1)
    
    source_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.asm"
    
    with open(source_file, 'r') as f:
        code = f.read()
    
    try:
        # Lexical analysis
        tokens = tokenize(code)
        
        # Syntax analysis
        ast = parse_program(tokens)
        
        # Semantic analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Generate intermediate code
        ir_gen = IntermediateCodeGenerator()
        ir_gen.generate(ast)
        ir_code = ir_gen.get_code()
        
        # Generate assembly code
        code_gen = CodeGenerator(ir_code)
        asm = code_gen.generate()
        assembly = code_gen.get_assembly()
        
        # Write to output file
        with open(output_file, 'w') as out:
            out.write(assembly)
            
        print(f"Compilation completed successfully! Assembly written to {output_file}")
    except Exception as e:
        print(f"Compilation error: {e}")