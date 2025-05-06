from .intermediate_code import ThreeAddressCode

class VibeVM:
    def __init__(self, code):
        self.code = code
        self.vars = {}
        self.output = []
        self.labels = {}
        self.ip = 0  # instruction pointer
        self.debug = True  # Enable debug mode

    def debug_print(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    def run(self):
        # First, map labels to instruction indices
        for idx, instr in enumerate(self.code):
            if instr.op == 'LABEL':
                self.labels[instr.arg1] = idx
                self.debug_print(f"Label {instr.arg1} at index {idx}")
        
        self.ip = 0
        while self.ip < len(self.code):
            instr = self.code[self.ip]
            self.debug_print(f"Executing instruction {self.ip}: {instr}")
            
            if instr.op == '=':
                value = self.eval_arg(instr.arg1)
                self.vars[instr.result] = value
                self.debug_print(f"Assigned {value} to {instr.result}")
            elif instr.op in ['+', '-', '*', '/']:
                left = self.eval_arg(instr.arg1)
                right = self.eval_arg(instr.arg2)
                if instr.op == '+':
                    self.vars[instr.result] = left + right
                elif instr.op == '-':
                    self.vars[instr.result] = left - right
                elif instr.op == '*':
                    self.vars[instr.result] = left * right
                elif instr.op == '/':
                    self.vars[instr.result] = left // right if isinstance(left, int) and isinstance(right, int) else left / right
                self.debug_print(f"Computed {instr.result} = {left} {instr.op} {right} = {self.vars[instr.result]}")
            elif instr.op in ['<', '>', '<=', '>=', '==', '!=', '<>']:
                left = self.eval_arg(instr.arg1)
                right = self.eval_arg(instr.arg2)
                result = self.eval_condition(left, instr.op, right)
                self.vars[instr.result] = result
                self.debug_print(f"Comparison {left} {instr.op} {right} = {result}")
            elif instr.op == 'PRINT':
                val = self.eval_arg(instr.arg1)
                self.output.append(str(val))
                self.debug_print(f"Printed: {val}")
            elif instr.op == 'GOTO':
                if instr.arg1 in self.labels:
                    self.debug_print(f"Jumping to label {instr.arg1} at index {self.labels[instr.arg1]}")
                    self.ip = self.labels[instr.arg1]
                    continue
                else:
                    raise RuntimeError(f'Label {instr.arg1} not found')
            elif instr.op == 'IF_FALSE':
                cond = self.eval_arg(instr.arg1)
                self.debug_print(f"IF_FALSE condition: {cond}")
                if not cond:
                    if instr.arg2 in self.labels:
                        self.debug_print(f"Condition false, jumping to label {instr.arg2} at index {self.labels[instr.arg2]}")
                        self.ip = self.labels[instr.arg2]
                        continue
                    else:
                        raise RuntimeError(f'Label {instr.arg2} not found')
            elif instr.op == 'LABEL':
                self.debug_print(f"Reached label {instr.arg1}")
            
            self.debug_print(f"Current variables: {self.vars}")
            self.ip += 1
        
        return '\n'.join(self.output)

    def eval_arg(self, arg):
        if arg is None:
            return None
        if isinstance(arg, str):
            if arg.startswith('[') and arg.endswith(']'):
                # Array literal
                return [self.eval_arg(x.strip()) for x in arg[1:-1].split(',') if x.strip()]
            if arg in self.vars:
                value = self.vars[arg]
                self.debug_print(f"Looked up {arg} = {value}")
                return value
            try:
                if '.' in arg:
                    return float(arg)
                return int(arg)
            except ValueError:
                return arg.strip('"')  # treat as string literal
        return arg

    def eval_condition(self, left, op, right):
        if op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        else:
            raise RuntimeError(f'Unknown comparison operator: {op}') 