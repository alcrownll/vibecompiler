# Vibe — A Programming Language Inspired by Gen Z Slang

Vibe is a custom programming language with syntax pulled straight from Gen Z slang — `clout` instead of `int`, `shoutout` instead of `print`, `smash` instead of `if` — paired with a full compiler pipeline and a web-based playground where you can write and run Vibe code directly in the browser.

Built for **CS Elective – Compiler Design**, this project required designing an original programming language from scratch and implementing a working compiler for it, from lexer to execution.

🔗 **Try it live:** https://vibe-compiler.web.app/vibeprogramminglanguage/home 

---

## What is Vibe?

Vibe keeps the structure of a typical imperative language (variables, functions, conditionals, loops, arrays, dictionaries) but renames every keyword to slang. A "Hello World" style program looks like this:

```vibe
starterPack vibeSample {
    clout x = 10;
    tea message = "Vibe check!";
    mood isVibing = noCap;

    smash (x > 5) {
        shoutout("x is greater than 5");
    } maybe (x == 5) {
        shoutout("x is exactly 5");
    } pass {
        shoutout("x is less than 5");
    }

    grind (x > 0) {
        x = x - 1;
    }

    serve addNumbers(clout a, clout b) {
        return a + b;
    }
}
```

### Keyword cheat sheet

| Vibe | Meaning |
|---|---|
| `starterPack` | program entry block |
| `clout` / `ratio` / `tea` / `mood` | int / float / string / boolean |
| `gang` / `wiki` | array / dictionary |
| `noCap` / `cap` / `ghosted` | true / false / null |
| `shoutout` | print |
| `spillTheTea` | input |
| `smash` / `maybe` / `pass` | if / else if / else |
| `grind` | while loop |
| `yeet` | for loop |
| `serve` | function declaration |
| `staph` | break |
| `itsGiving` | typeof |
| `chooseYourFighter` | switch |
| `tryhard` / `flopped` | try / catch |

---

## How it works

Vibe is a real compiler, not a toy interpreter — code you write goes through the full pipeline before it runs:

```
Source (.vibe) → Lexer → Parser → Semantic Analyzer → Type Checker
              → Intermediate Code Generator → Optimizer → Code Generator → Virtual Machine
```

- **Lexer** — tokenizes Vibe source using a regex-based scanner, mapping slang keywords to their underlying token types.
- **Parser** — builds an AST from the token stream.
- **Semantic Analyzer / Type Checker** — validates scoping, declarations, and types before execution.
- **Intermediate Code Generator + Optimizer** — lowers the AST into an intermediate representation and applies optimization passes.
- **Code Generator + Virtual Machine** — executes the final program and streams output back to the browser.

## The playground

The frontend is a browser-based IDE for writing and running Vibe code:

- **Monaco-powered editor** (the same engine behind VS Code) for syntax highlighting and a familiar editing experience.
- **Terminal-style output console** (built with xterm.js) that shows compilation errors and program output as it runs.
- **Multilingual UI** — available in English, Tagalog, and Bisaya/Cebuano via i18next.
- Sample programs to help new users learn the syntax quickly.

---

## Tech stack

**Frontend**
- React + TypeScript + Vite
- Tailwind CSS
- Monaco Editor
- xterm.js
- react-i18next (EN / TL / Bisaya)
- Firebase Hosting

**Backend**
- Python + FastAPI
- Custom lexer, parser, semantic analyzer, type checker, intermediate code generator, optimizer, and virtual machine (no external parser-generator libraries — the whole pipeline is hand-written)
- Deployed on Render

---

## Running it locally

### Prerequisites
- Node.js 18+
- Python 3.11+

### Setup

```bash
# clone the repo
git clone [ADD REPO URL]
cd vibecompiler

# install frontend dependencies
npm install

# install backend dependencies
pip install -r backend/requirements.txt
```

### Development

```bash
# runs the Vite dev server and the FastAPI backend together
npm run dev
```

The frontend will be available at `http://localhost:5173`, and the backend API at whatever port `backend/run.py` starts on (default FastAPI/uvicorn port).

### Build for production

```bash
npm run build
```
