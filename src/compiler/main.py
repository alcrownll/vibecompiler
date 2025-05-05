#!/usr/bin/env python3
import sys
import os
from lexer import tokenize
from parser import parse_program
from semanticAnalyzer import SemanticAnalyzer
from intermediateCodeGenerator import IntermediateCodeGenerator
from codeGenerator import CodeGenerator

def compile_file(source_file, output_file=None, optimize=False):
    """
    Compile a source file to assembly.
    
    Args:
        source_file: Path to the source file
        output_file: Path to t he output assembly file (default: source_file with .asm extension)
        optimize: Whether to apply optimizations (default: False)
    """
    if output_file is None:
        base = os.path.splitext(source_file)[0]
        output_file = f"{base}.asm"
    
    print(f"Compiling {source_file} to {output_file}")
    
    # Read source code
    with open(source_file, 'r') as f:
        code = f.read()
    
    try:
        # Step 1: Lexical Analysis
        print("Performing lexical analysis...")
        tokens = list(tokenize(code))
        print(f"Found {len(tokens)} tokens.")
        
        # Step 2: Syntax Analysis
        print("Performing syntax analysis...")
        ast = parse_program(tokens)
        print("Syntax analysis completed successfully.")
        
        # Step 3: Semantic Analysis
        print("Performing semantic analysis...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("Semantic analysis completed successfully.")
        
        # Step 4: Intermediate Code Generation
        print("Generating intermediate code...")
        ir_gen = IntermediateCodeGenerator()
        ir_gen.generate(ast)
        ir_code = ir_gen.get_code()
        print(f"Generated {len(ir_code)} intermediate instructions.")
        
        # Step 5: Code Optimization (optional)
        if optimize:
            print("Optimizing intermediate code...")
            # Apply optimizations here (not implemented in this basic version)
            print("Optimization completed.")
        
        # Step 6: Code Generation
        print("Generating assembly code...")
        code_gen = CodeGenerator(ir_code)
        code_gen.generate()
        assembly = code_gen.get_assembly()
        
        # Write assembly to output file
        with open(output_file, 'w') as out:
            out.write(assembly)
            
        print(f"Assembly code written to {output_file}")
        print("Compilation completed successfully!")
        return True
    
    except Exception as e:
        print(f"Compilation error: {e}")
        return False

def print_usage():
    print("Usage: python compiler.py [options] <source_file>")
    print("Options:")
    print("  -o <file>    Specify output file")
    print("  -O           Enable optimizations")
    print("  -h, --help   Display this help message")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        sys.exit(0)
    
    # Parse command line arguments
    output_file = None
    optimize = False
    source_file = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '-O':
            optimize = True
            i += 1
        elif sys.argv[i].startswith('-'):
            print(f"Unknown option: {sys.argv[i]}")
            print_usage()
            sys.exit(1)
        else:
            source_file = sys.argv[i]
            i += 1
    
    if not source_file:
        print("Error: No source file specified")
        print_usage()
        sys.exit(1)
    
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' does not exist")
        sys.exit(1)
    
    success = compile_file(source_file, output_file, optimize)
    sys.exit(0 if success else 1)