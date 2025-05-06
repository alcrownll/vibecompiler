# VibeLang Compiler Backend

This is the backend component of the VibeLang compiler, which implements a complete compiler pipeline for the VibeLang programming language.

## Features

- Lexical Analysis using regular expressions
- Syntax Analysis using LL(1) parsing
- Semantic Analysis with type checking and scope management
- Intermediate Code Generation (Three-Address Code)
- Code Optimization (Constant Folding)
- Assembly Code Generation
- REST API for compilation requests

## Project Structure

```
backend/
├── src/
│   ├── lexer.py          # Lexical analyzer
│   ├── parser.py         # Syntax analyzer
│   ├── semantic_analyzer.py  # Semantic analyzer
│   ├── intermediate_code.py  # Intermediate code generator
│   ├── code_generator.py     # Assembly code generator
│   ├── compiler.py       # Main compiler class
│   └── api.py           # FastAPI endpoint
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server:
```bash
python -m src.api
```

2. Send compilation requests to `http://localhost:8000/compile`:
```bash
curl -X POST "http://localhost:8000/compile" \
     -H "Content-Type: application/json" \
     -d '{"source_code": "starterPack myProgram { clout x = 5; shoutout(x); }"}'
```

## Language Features

### Data Types
- `clout` - Integer
- `ratio` - Float
- `tea` - String
- `mood` - Boolean
- `gang` - Array
- `wiki` - Dictionary

### Control Structures
- `smash` - If statement
- `maybe` - Else if
- `pass` - Else
- `grind` - While loop
- `yeet` - For loop

### Functions
- `serve` - Function declaration
- `staph` - Break statement

### I/O
- `shoutout` - Print statement
- `spillTheTea` - Input function

### Constants
- `noCap` - True
- `cap` - False
- `ghosted` - Null

## Example Program

```vibescript
starterPack helloWorld {
    clout x = 5;
    ratio y = 3.14;
    tea message = "Hello, World!";
    
    smash (x > 0) {
        shoutout(message);
    } pass {
        shoutout("x is not positive");
    }
    
    grind (x > 0) {
        shoutout(x);
        x = x - 1;
    }
}
```

## Error Handling

The compiler provides detailed error messages for:
- Syntax errors
- Type mismatches
- Undeclared variables
- Scope violations
- Semantic errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 