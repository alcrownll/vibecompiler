from typing import List, Optional, Dict, Any
from .lexer import Lexer
from .parser import Parser
from .semantic_analyzer import SemanticAnalyzer
from .intermediate_code import IntermediateCodeGenerator
from .code_generator import AssemblyGenerator
from .vm import VibeVM
from .errors import CompilerError, format_error

class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)
        self.semantic_analyzer = SemanticAnalyzer()
        self.intermediate_generator = IntermediateCodeGenerator()
        self.code_generator = AssemblyGenerator()

    def compile(self, source_code: str) -> List[str]:
        try:
            # Lexical Analysis
            tokens = self.lexer.tokenize(source_code)
            
            # Syntax Analysis
            ast = self.parser.parse(source_code)
            
            # Semantic Analysis
            self.semantic_analyzer.analyze(ast)
            
            # Intermediate Code Generation
            intermediate_code = self.intermediate_generator.generate(ast)
            
            # Optimization
            self.intermediate_generator.optimize()
            
            # Code Generation
            assembly_code = self.code_generator.generate(intermediate_code)
            
            # Final Optimization
            self.code_generator.optimize()
            
            return assembly_code
            
        except Exception as e:
            if isinstance(e, CompilerError):
                raise e
            error_message = str(e)
            if hasattr(e, 'node') and e.node:
                error_message += f" at line {e.node.line}, column {e.node.column}"
            raise CompilerError(error_message)

    def compile_and_run(self, source_code: str) -> Dict[str, Any]:
        try:
            # Lexical Analysis
            tokens = self.lexer.tokenize(source_code)
            
            # Syntax Analysis
            ast = self.parser.parse(source_code)
            
            # Semantic Analysis
            self.semantic_analyzer.analyze(ast)
            
            # Intermediate Code Generation
            intermediate_code = self.intermediate_generator.generate(ast)
            
            # Optimization
            self.intermediate_generator.optimize()
            
            # Code Generation
            assembly_code = self.code_generator.generate(intermediate_code)
            
            # Final Optimization
            self.code_generator.optimize()
            
            # Run the VM/interpreter
            vm = VibeVM(intermediate_code)
            program_output = vm.run()
            
            return {
                'assembly_code': assembly_code,
                'program_output': program_output
            }
        except Exception as e:
            if isinstance(e, CompilerError):
                raise e
            error_message = str(e)
            if hasattr(e, 'node') and e.node:
                error_message += f" at line {e.node.line}, column {e.node.column}"
            raise CompilerError(error_message)

def compile_source(source_code: str) -> List[str]:
    compiler = Compiler()
    return compiler.compile(source_code)

def compile_and_run_source(source_code: str) -> Dict[str, Any]:
    compiler = Compiler()
    return compiler.compile_and_run(source_code) 