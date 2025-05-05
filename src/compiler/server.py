from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import logging
import json

# Import enhanced compiler components
from error_optimizer import CompilerPipeline, enhanced_tokenize, ErrorCollector

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/compile', methods=['POST'])
def compile_vibe():
    source = request.json.get('code')
    optimization_level = request.json.get('optimization_level', 1)  # Default to level 1
    
    logger.debug(f"Received code: {source[:100]}...")  # Log first 100 chars
    logger.debug(f"Optimization level: {optimization_level}")
    
    compiler = CompilerPipeline(source)
    success, result = compiler.run()
    
    if success:
        return jsonify({
            'success': True,
            'output': result.get('target_code', ''),
            'optimization_stats': result.get('optimization_stats', {}),
            'warnings': result.get('warnings', [])
        })
    else:
        return jsonify({
            'success': False,
            'errors': result.get('errors', []),
            'warnings': result.get('warnings', [])
        })

@app.route('/validate', methods=['POST'])
def validate_vibe():
    """Endpoint to validate code without generating output"""
    source = request.json.get('code')
    
    logger.debug(f"Validating code: {source[:100]}...")
    
    # Only perform lexical and syntax analysis
    tokens, lex_errors = enhanced_tokenize(source)
    
    if lex_errors.has_errors():
        return jsonify({
            'success': False,
            'errors': [e.to_dict() for e in lex_errors.errors],
            'warnings': [w.to_dict() for w in lex_errors.warnings]
        })
    
    # Try parsing
    try:
        from parser import parse_program
        ast = parse_program(tokens)
        
        # Basic semantic checks
        from semanticAnalyzer import SemanticAnalyzer
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        return jsonify({
            'success': True,
            'message': 'Code validates successfully'
        })
    except Exception as e:
        error_collector = ErrorCollector()
        
        if hasattr(e, 'line') and hasattr(e, 'column'):
            error = {
                'line': e.line,
                'column': e.column,
                'message': str(e),
                'type': 'syntax' if 'SyntaxError' in str(type(e)) else 'semantic'
            }
        else:
            error = {
                'line': 1,
                'column': 0,
                'message': str(e),
                'type': 'unknown'
            }
        
        return jsonify({
            'success': False,
            'errors': [error]
        })

@app.route('/tokenize', methods=['POST'])
def tokenize_vibe():
    """Endpoint to get tokens from code"""
    source = request.json.get('code')
    
    tokens, errors = enhanced_tokenize(source)
    
    token_list = []
    for token in tokens:
        token_type, value, line, col = token
        token_list.append({
            'type': token_type,
            'value': value,
            'line': line,
            'column': col
        })
    
    return jsonify({
        'success': not errors.has_errors(),
        'tokens': token_list,
        'errors': [e.to_dict() for e in errors.errors] if errors.has_errors() else []
    })

@app.route('/ast', methods=['POST'])
def get_ast():
    """Endpoint to get the AST for code"""
    source = request.json.get('code')
    
    tokens, errors = enhanced_tokenize(source)
    
    if errors.has_errors():
        return jsonify({
            'success': False,
            'errors': [e.to_dict() for e in errors.errors]
        })
    
    try:
        from parser import parse_program
        ast = parse_program(tokens)
        
        # Convert AST to serializable format
        def ast_to_dict(node):
            if node is None:
                return None
            
            result = {
                'type': node.node_type,
                'value': node.value
            }
            
            if hasattr(node, 'children') and node.children:
                result['children'] = [ast_to_dict(child) for child in node.children]
            
            return result
        
        return jsonify({
            'success': True,
            'ast': ast_to_dict(ast)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/optimize', methods=['POST'])
def optimize_code():
    """Endpoint to just perform code optimization"""
    source = request.json.get('code')
    
    # Parse the AST
    tokens, errors = enhanced_tokenize(source)
    
    if errors.has_errors():
        return jsonify({
            'success': False,
            'errors': [e.to_dict() for e in errors.errors]
        })
    
    try:
        from parser import parse_program
        ast = parse_program(tokens)
        
        # Run optimizer
        from error_optimizer import OptimizerManager, ConstantFolding, DeadCodeElimination, UnusedCodeAnalyzer
        
        optimizer = OptimizerManager(ast)
        optimizer.add_pass(ConstantFolding)
        optimizer.add_pass(DeadCodeElimination)
        optimizer.add_pass(UnusedCodeAnalyzer)
        
        optimized_ast, warnings, opt_count = optimizer.run_optimizations()
        
        # Generate intermediate code from optimized AST
        from intermediateCodeGenerator import IntermediateCodeGenerator
        ir_gen = IntermediateCodeGenerator()
        ir_gen.generate(optimized_ast)
        ir_code = ir_gen.get_code()
        
        # Generate target code
        from codeGenerator import CodeGenerator
        code_gen = CodeGenerator(ir_code)
        code_gen.generate()
        target_code = code_gen.get_assembly()
        
        return jsonify({
            'success': True,
            'optimized_code': target_code,
            'optimization_count': opt_count,
            'warnings': [w.to_dict() for w in warnings]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Test endpoint to check if the server is running
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'message': 'Vibe Compiler API is running'})

if __name__ == '__main__':
    logger.info("Starting Vibe compiler server on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)