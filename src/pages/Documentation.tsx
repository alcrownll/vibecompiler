import React, { useState } from 'react';

const Documentation = () => {
  const [selectedSection, setSelectedSection] = useState('');

  const scrollToSection = (id: string) => {
    const container = document.getElementById('right-pane');
    const section = document.getElementById(id);

    if (container && section) {
      container.scrollTo({
        top: section.offsetTop - container.offsetTop,
        behavior: 'smooth',
      });
    }
  };

  const handleDropdownChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const id = e.target.value;
    setSelectedSection(id);
    scrollToSection(id);
  };

  const sections = [
    { id: 'what-is-vibelang', label: 'Introduction' },
    { id: 'getting-started', label: 'Getting Started' },
    { id: 'syntax-basics', label: 'Syntax Basics' },
    { id: 'data-types', label: 'Data Types' },
    { id: 'operators', label: 'Operators' },
    { id: 'control-flow', label: 'Control Flow' },
    { id: 'functions', label: 'Functions' },
    { id: 'input-output', label: 'Input & Output' },
    { id: 'error-handling', label: 'Error Handling' },
    { id: 'code-examples', label: 'Code Examples' },
    { id: 'glossary', label: 'Glossary' },
    { id: 'faq', label: 'FAQ' },
  ];

  

  return (
    <div className="h-screen flex flex-col md:flex-row text-white">
      {/* Mobile Dropdown Navigation */}
      <div className="md:hidden p-4">
        <h2 className="text-xl font-semibold mb-2">Quick Navigation</h2>
        <select
          value={selectedSection}
          onChange={handleDropdownChange}
          className="w-full p-2 bg-gray-800 text-white rounded"
        >
          <option value="">Select Section</option>
          {sections.map((section) => (
            <option key={section.id} value={section.id}>
              {section.label}
            </option>
          ))}
        </select>
      </div>

      {/* Desktop Sidebar Navigation */}
      <div className="hidden md:block w-full md:w-1/3 p-8 sticky top-0 h-auto md:h-screen">
        <h2 className="text-xl font-semibold mb-4">Quick Navigation</h2>
        <ul className="space-y-2 text-sm">
          {sections.map((section) => (
            <li key={section.id}>
              <a
                onClick={() => scrollToSection(section.id)}
                className="hover:underline cursor-pointer"
              >
                {section.label}
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Right Pane Content */}
      <div
        id="right-pane"
        className="w-full md:w-2/3 overflow-y-scroll no-scrollbar px-4 md:px-8 py-8 md:py-12 scroll-smooth mb-10"
      >
       <h1 className="text-4xl font-bold mb-6 text-center">VibeLang Documentation</h1>

        {/* Sections */}
        <section id="what-is-vibelang" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">🚀 What is VibeLang?</h2>
          <p>Vibe is a Gen Z-inspired programming language that blends modern programming concepts with internet slang, making coding fun, accessible, and relevant for younger coders. Vibe reimagines traditional programming syntax by incorporating expressions that feel familiar to users, using everyday phrases and slang like smash for if statements and shoutout() for output. Whether you're just starting out or looking for an intuitive way to code, Vibe offers a relatable approach to programming.</p>
        </section>

        <section id="getting-started" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">✨ Getting Started</h2>
          <ul className="list-disc pl-5 space-y-4">
            <li>
              <strong>File Extension:</strong> Vibe programs use the <code>.vibe</code> file extension.
            </li>

            <li>
              <strong>Compiler Setup:</strong>
              <p>
                To get started with Vibe, you can run it locally by forking our project{" "}
                <a href="https://github.com/alcrownll/vibecompiler" target="_blank" className="text-blue-500 underline">
                  here
                </a>.
              </p>
              <p>
                You can also try out the programming language in the{" "}
                <a href="/vibeprogramminglanguage/playground" className="text-blue-500 underline">
                  Playground
                </a>{" "}
                section.
              </p>
            </li>

            <li>
              <strong>First Program:</strong>
               <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto text-white mt-2 max-w-md">
        {`starterPack
            shoutout("Welcome to Vibe!")`}
              </pre>
            </li>
          </ul>
        </section>


        <section id="syntax-basics" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📝 Syntax Basics</h2>
          <ul className="list-disc pl-5 space-y-4">
            <li>
              <strong>Program Declaration:</strong> Every Vibe program starts with <code>starterPack</code>, marking the entry point.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto text-white mt-2 max-w-md">
        {`starterPack
            shoutout("Welcome to Vibe!")`}
              </pre>
            </li>

            <li>
              <strong>Comments:</strong> Single-line comments begin with the <code>~</code> symbol.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto text-white mt-2 max-w-md">
        {`~ This is a comment`}
              </pre>
            </li>

            <li>
              <strong>Whitespace:</strong> Indentation defines code blocks. No curly braces <code>{`{}`}</code> are required.
            </li>
          </ul>
        </section>


        <section id="data-types" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📦 Data Types & Constants</h2>

          <p className="mb-4">Vibe provides several built-in data types, each represented with a fun keyword.</p>

          <ul className="list-disc ml-6 space-y-4">
            <li>
              <strong>clout</strong> — Integer (whole numbers)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`clout number = 10`}
              </pre>
            </li>

            <li>
              <strong>ratio</strong> — Float (decimal numbers)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`ratio price = 3.14`}
              </pre>
            </li>

            <li>
              <strong>tea</strong> — String (text values)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`tea name = "Vibe"`}
              </pre>
            </li>

            <li>
              <strong>mood</strong> — Boolean (true/false)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`mood isHappy = noCap`}
              </pre>
            </li>

            <li>
              <strong>gang</strong> — Array (ordered collections)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`gang nums = [1, 2, 3]`}
              </pre>
            </li>

            <li>
              <strong>wiki</strong> — Dictionary (key-value pairs)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`wiki user = {name: "Alice", age: 25}`}
              </pre>
            </li>

            <li>
              <strong>ghosted</strong> — Null (no value / uninitialized)
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`data = ghosted`}
              </pre>
            </li>
          </ul>
        </section>

        <section id="operators" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">➕ Operators</h2>
          <p className="mb-4">Vibe supports standard arithmetic, comparison, and logical operators with a chill syntax.</p>

          <ul className="list-disc ml-6 space-y-4">
            <li>
              <strong>Arithmetic Operators</strong> — Perform basic math operations.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`+, -, *, /, %`}
              </pre>
            </li>

            <li>
              <strong>Comparison Operators</strong> — Compare values.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`==, !=`}
              </pre>
            </li>

            <li>
              <strong>Logical Operators</strong> — Combine boolean expressions.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`&&  // and
        ||  // or`}
              </pre>
            </li>
          </ul>
        </section>


        <section id="control-flow" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">🕹️ Control Flow</h2>
          <p className="mb-4">Vibe provides expressive control flow keywords with a conversational tone:</p>

          <ul className="list-disc ml-6 space-y-4">
            <li>
              <strong>If Statement</strong> — Start with <code>smash</code>.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`smash condition:
            shoutout("It's true!")
        else:
            shoutout("It's false!")`}
              </pre>
            </li>

            <li>
              <strong>Else-If</strong> — Use <code>maybe</code> for intermediate conditions.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`smash condition:
            shoutout("It's true!")
        maybe condition2:
            shoutout("It's maybe true!")
        else:
            shoutout("It's false!")`}
              </pre>
            </li>

            <li>
              <strong>While Loop</strong> — Use <code>grind</code> to loop while a condition is true.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`grind condition:
            shoutout("Still grinding!")`}
              </pre>
            </li>

            <li>
              <strong>For Loop</strong> — Use <code>yeet</code> for a fixed-range loop.
              <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto mt-2 max-w-md">
        {`yeet i = 0 to 5:
            shoutout("Yeeting!")`}
              </pre>
            </li>
          </ul>
        </section>


        <section id="functions" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">💅 Functions</h2>
          <p className="mb-2"><strong>Function Declaration:</strong> Use the <code>serve</code> keyword to define a function.</p>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto max-w-md mb-4">
        {`serve greet(name: tea) -> tea:
            shoutout("Hello, " + name)`}
          </pre>

          <p className="mb-2"><strong>Function Call:</strong></p>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto max-w-md">
        {`greet("Alice")`}
          </pre>
        </section>


        <section id="input-output" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📥📤 Input & Output</h2>

          <p className="mb-2"><strong>Output:</strong> Use <code>shoutout()</code> to print to the console.</p>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto max-w-md mb-4">
        {`shoutout("Hello, world!")`}
          </pre>

          <p className="mb-2"><strong>Input:</strong> <code>spillTheTea()</code> will be introduced in a future version to support user input.</p>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm text-white overflow-x-auto max-w-md">
        {`~ Not yet implemented in this version.`}
          </pre>
        </section>


        <section id="error-handling" className="mb-8">
        <h2 className="text-2xl font-semibold mb-2">🚨 Error Handling</h2>
        <p className="mb-4">Vibe throws errors with its own unique flavor. Here's how different issues are reported:</p>
        <ul className="list-disc ml-6 space-y-2">
          <li><strong>Lexical Error:</strong> <code>"main character syndrome"</code></li>
          <li><strong>Syntax Error:</strong> <code>"not vibing"</code></li>
          <li><strong>Type Error:</strong> <code>"lowkey caught in 4K"</code></li>
          <li><strong>Name Error:</strong> <code>"ghosted reference"</code></li>
          <li><strong>Scope Error:</strong> <code>"out of pocket"</code></li>
          <li><strong>Runtime Error:</strong> <code>"dead fr"</code></li>
          <li><strong>Division by Zero:</strong> <code>"dividing by zero? that's cap fr fr"</code></li>
          <li><strong>Array Index Error:</strong> <code>"gang member X got ghosted"</code></li>
          <li><strong>IO Error:</strong> <code>"tea spilled"</code></li>
        </ul>
      </section>


      <section id="code-examples" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📚 Code Examples</h2>
          <p className="mb-4">Here are some basic examples of Vibe in action:</p>

          <h3 className="text-xl font-semibold mb-2">Hello World Example:</h3>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto">
            {`starterPack
            shoutout("Hello, world!")`}
          </pre>

          <h3 className="text-xl font-semibold mb-2">If-Else Example:</h3>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto">
            {`starterPack
            let number = 10 ~ clout
            smash number > 5:
                shoutout("Number is greater than 5!")
            else:
                shoutout("Number is 5 or less.")`}
          </pre>

          <h3 className="text-xl font-semibold mb-2">Vibe Example (Mood Check):</h3>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto">
            {`let's vibe mood = fr
            on god (mood) {
                say "we vibin fr"
            }`}
          </pre>
        </section>


        <section id="glossary" className="mb-8">
        <h2 className="text-2xl font-semibold mb-2">📖 Glossary</h2>
        <ul className="list-disc ml-6 space-y-2">
          <li><strong>StarterPack</strong> — The main entry point for a Vibe program.</li>
          <li><strong>clout</strong> — Integer data type.</li>
          <li><strong>ratio</strong> — Float data type.</li>
          <li><strong>tea</strong> — String data type.</li>
          <li><strong>mood</strong> — Boolean data type.</li>
          <li><strong>gang</strong> — Array/List data type.</li>
          <li><strong>wiki</strong> — Dictionary/Map data type.</li>
          <li><strong>ghosted</strong> — Null value.</li>
        </ul>
      </section>


      <section id="faq" className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">❓ FAQ</h2>

          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold">Is VibeLang a real programming language?</h3>
              <p>Yes! VibeLang is a real, functioning language with its own compiler. It’s designed to make coding more fun and intuitive, especially for younger audiences.</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold">Where can I try VibeLang?</h3>
              <p>You can try VibeLang in the <a href="/vibeprogramminglanguage/playground" className="text-blue-500 underline">Playground</a> or clone the <a href="https://github.com/alcrownll/vibecompiler" target="_blank" className="text-blue-500 underline">GitHub repo</a> to run it locally.</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold">Is it suitable for beginners?</h3>
              <p>Absolutely. VibeLang was built to be beginner-friendly and uses Gen Z slang and simple syntax to help new coders learn in a fun way.</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold">What platforms does VibeLang support?</h3>
              <p>Currently, you can run VibeLang in the web-based Playground or via Node.js locally using the compiler from GitHub.</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold">Can I contribute?</h3>
              <p>Yes! VibeLang is open source. Feel free to contribute on <a href="https://github.com/alcrownll/vibecompiler" target="_blank" className="text-blue-500 underline">GitHub</a>.</p>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

export default Documentation;