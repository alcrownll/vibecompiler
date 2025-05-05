# server.py
from flask import Flask, request, jsonify
from lexer import tokenize
from parser import parse_program
from semanticAnalyzer import SemanticAnalyzer
from intermediateCodeGenerator import IntermediateCodeGenerator
from codeGenerator import CodeGenerator

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_vibe():
    source = request.json.get('code')
    try:
        tokens = list(tokenize(source))
        ast = parse_program(tokens)
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        ir_gen = IntermediateCodeGenerator()
        ir_gen.generate(ast)
        code_gen = CodeGenerator(ir_gen.get_code())
        code_gen.generate()
        assembly = code_gen.get_assembly()
        return jsonify({ 'success': True, 'output': assembly })
    except Exception as e:
        return jsonify({ 'success': False, 'error': str(e) })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
