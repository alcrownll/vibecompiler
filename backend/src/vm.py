from .intermediate_code import ThreeAddressCode

class VibeVM:
    def __init__(self, code):
        self.code = code
        self.vars = {}
        self.output = []
        self.labels = {}
        self.ip = 0  # instruction pointer

    def run(self):
        # First, map labels to instruction indices
        for idx, instr in enumerate(self.code):
            if instr.op == 'LABEL':
                self.labels[instr.arg1] = idx
        self.ip = 0
        while self.ip < len(self.code):
            instr = self.code[self.ip]
            if instr.op == '=':
                self.vars[instr.result] = self.eval_arg(instr.arg1)
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
            elif instr.op == 'PRINT':
                val = self.eval_arg(instr.arg1)
                self.output.append(str(val))
            elif instr.op == 'GOTO':
                if instr.arg1 in self.labels:
                    self.ip = self.labels[instr.arg1]
                else:
                    raise RuntimeError(f'Label {instr.arg1} not found')
                continue
            elif instr.op == 'IF_FALSE':
                cond = self.eval_arg(instr.arg1)
                if not cond:
                    if instr.arg2 in self.labels:
                        self.ip = self.labels[instr.arg2]
                    else:
                        raise RuntimeError(f'Label {instr.arg2} not found')
                    continue
            # Ignore LABEL and others for now
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
                return self.vars[arg]
            try:
                if '.' in arg:
                    return float(arg)
                return int(arg)
            except ValueError:
                return arg.strip('"')  # treat as string literal
        return arg 