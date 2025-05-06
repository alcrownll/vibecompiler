from typing import List
from .intermediate_code import ThreeAddressCode

class AssemblyGenerator:
    def __init__(self):
        self.registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
        self.register_map = {}  # Maps temporaries to registers
        self.assembly = []
        self.stack_offset = 0
        self.variable_offset = {}  # Maps variables to stack offsets

    def generate(self, intermediate_code: List[ThreeAddressCode]) -> List[str]:
        self.assembly = []
        self.assembly.append(".text")
        self.assembly.append(".global main")
        self.assembly.append("main:")
        
        # Prologue
        self.assembly.append("    push {fp, lr}")
        self.assembly.append("    mov fp, sp")
        
        # Calculate stack size needed for variables
        stack_size = 0
        for instr in intermediate_code:
            if instr.result and instr.result not in self.variable_offset:
                self.variable_offset[instr.result] = stack_size
                stack_size += 4  # 4 bytes per variable
        
        if stack_size > 0:
            self.assembly.append(f"    sub sp, sp, #{stack_size}")
        
        # Generate code for each instruction
        for instr in intermediate_code:
            self.generate_instruction(instr)
        
        # Epilogue
        self.assembly.append("    mov sp, fp")
        self.assembly.append("    pop {fp, lr}")
        self.assembly.append("    bx lr")
        
        return self.assembly

    def get_register(self, temp: str) -> str:
        if temp not in self.register_map:
            if len(self.register_map) < len(self.registers):
                reg = self.registers[len(self.register_map)]
                self.register_map[temp] = reg
            else:
                # Spill to stack
                offset = self.variable_offset.get(temp, 0)
                return f"[fp, #{offset}]"
        return self.register_map[temp]

    def generate_instruction(self, instr: ThreeAddressCode):
        if instr.op == 'LABEL':
            self.assembly.append(f"{instr.arg1}:")
        elif instr.op == 'GOTO':
            self.assembly.append(f"    b {instr.arg1}")
        elif instr.op == 'IF_FALSE':
            reg = self.get_register(instr.arg1)
            self.assembly.append(f"    cmp {reg}, #0")
            self.assembly.append(f"    beq {instr.arg2}")
        elif instr.op == 'PRINT':
            reg = self.get_register(instr.arg1)
            self.assembly.append(f"    mov r0, {reg}")
            self.assembly.append("    bl printf")
        elif instr.op == '=':
            if instr.arg1.isdigit():
                self.assembly.append(f"    mov {self.get_register(instr.result)}, #{instr.arg1}")
            else:
                src_reg = self.get_register(instr.arg1)
                dst_reg = self.get_register(instr.result)
                self.assembly.append(f"    mov {dst_reg}, {src_reg}")
        elif instr.op in ['+', '-', '*', '/']:
            left_reg = self.get_register(instr.arg1)
            right_reg = self.get_register(instr.arg2)
            result_reg = self.get_register(instr.result)
            
            if instr.op == '+':
                self.assembly.append(f"    add {result_reg}, {left_reg}, {right_reg}")
            elif instr.op == '-':
                self.assembly.append(f"    sub {result_reg}, {left_reg}, {right_reg}")
            elif instr.op == '*':
                self.assembly.append(f"    mul {result_reg}, {left_reg}, {right_reg}")
            elif instr.op == '/':
                self.assembly.append(f"    sdiv {result_reg}, {left_reg}, {right_reg}")

    def optimize(self):
        # Simple peephole optimization
        i = 0
        while i < len(self.assembly):
            # Remove redundant moves
            if i + 1 < len(self.assembly):
                instr1 = self.assembly[i].strip()
                instr2 = self.assembly[i + 1].strip()
                if instr1.startswith("mov ") and instr2.startswith("mov ") and instr1.split()[2] == instr2.split()[1]:
                    self.assembly.pop(i)
                    continue
            i += 1 