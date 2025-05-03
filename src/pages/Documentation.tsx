const Documentation = () => {
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

  return (
    <div className="h-screen flex text-white">
      {/* Left Column (Navigation) */}
      <div className="w-1/3 p-8 sticky top-0 h-screen">
        <h2 className="text-xl font-semibold mb-4">Quick Navigation</h2>
        <ul className="space-y-2 text-sm">
          <li><a onClick={() => scrollToSection('what-is-vibelang')} className="hover:underline cursor-pointer">Introduction</a></li>
          <li><a onClick={() => scrollToSection('getting-started')} className="hover:underline cursor-pointer">Getting Started</a></li>
          <li><a onClick={() => scrollToSection('syntax-basics')} className="hover:underline cursor-pointer">Syntax Basics</a></li>
          <li><a onClick={() => scrollToSection('data-types')} className="hover:underline cursor-pointer">Data Types</a></li>
          <li><a onClick={() => scrollToSection('variables')} className="hover:underline cursor-pointer">Variables</a></li>
          <li><a onClick={() => scrollToSection('operators')} className="hover:underline cursor-pointer">Operators</a></li>
          <li><a onClick={() => scrollToSection('control-flow')} className="hover:underline cursor-pointer">Control Flow</a></li>
          <li><a onClick={() => scrollToSection('functions')} className="hover:underline cursor-pointer">Functions</a></li>
          <li><a onClick={() => scrollToSection('input-output')} className="hover:underline cursor-pointer">Input & Output</a></li>
          <li><a onClick={() => scrollToSection('error-handling')} className="hover:underline cursor-pointer">Error Handling</a></li>
          <li><a onClick={() => scrollToSection('code-examples')} className="hover:underline cursor-pointer">Code Examples</a></li>
          <li><a onClick={() => scrollToSection('glossary')} className="hover:underline cursor-pointer">Glossary</a></li>
          <li><a onClick={() => scrollToSection('faq')} className="hover:underline cursor-pointer">FAQ</a></li>
        </ul>
      </div>

      {/* Right Column (Content) */}
      <div id="right-pane" className="w-2/3 overflow-y-scroll no-scrollbar px-8 py-12 scroll-smooth">
        <h1 className="text-4xl font-bold mb-6">VibeLang Documentation</h1>

        <section id="what-is-vibelang" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">🚀 What is VibeLang?</h2>
          <p>VibeLang is a fun, expressive programming language that turns Gen Z slang into code.</p>
        </section>

        <section id="getting-started" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">✨ Getting Started</h2>
          <p>Install the VibeLang CLI or use the online playground. Type your first VibeLang script and run it!</p>
        </section>

        <section id="syntax-basics" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📝 Syntax Basics</h2>
          <ul className="list-disc ml-6 space-y-2">
            <li><code>let's vibe</code> — Declare a variable</li>
            <li><code>say</code> — Output to screen</li>
            <li><code>on god</code> — Assert/condition</li>
          </ul>
        </section>

        <section id="data-types" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📦 Data Types</h2>
          <ul className="list-disc ml-6 space-y-2">
            <li><strong>mood</strong> — Boolean</li>
            <li><strong>number</strong> — Integer</li>
            <li><strong>text</strong> — String</li>
            <li><strong>squad</strong> — List</li>
          </ul>
        </section>

        <section id="variables" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📌 Variables</h2>
          <p>Use <code>let's vibe</code> to declare variables. Example: <code>let's vibe mood = fr</code></p>
        </section>

        <section id="operators" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">➕ Operators</h2>
          <p>Supports +, -, *, /, %, ==, !=, && (and), || (or) with a VibeLang twist.</p>
        </section>

        <section id="control-flow" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">🕹️ Control Flow</h2>
          <p>Use <code>on god</code> for conditions, and <code>keep it up</code> for loops.</p>
        </section>

        <section id="functions" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">💅 Functions</h2>
          <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto">
{`glow up shoutout(name) {
  say "hey " + name
}`}
          </pre>
        </section>

        <section id="input-output" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📥📤 Input & Output</h2>
          <p><code>say</code> is used for output. Input is currently manual via pre-defined values (future support coming).</p>
        </section>

        <section id="error-handling" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">🚨 Error Handling</h2>
          <p>Syntax errors will throw “not vibing” errors. Semantic issues give “sus behavior” warnings.</p>
        </section>

        <section id="code-examples" className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">📚 Code Examples</h2>
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
            <li><strong>fr</strong> — true</li>
            <li><strong>nah</strong> — false</li>
            <li><strong>say</strong> — print</li>
            <li><strong>glow up</strong> — function declaration</li>
          </ul>
        </section>

        <section id="faq" className="mb-20">
          <h2 className="text-2xl font-semibold mb-2">❓ FAQ</h2>
          <p><strong>Q:</strong> Can I use standard JavaScript too?<br /><strong>A:</strong> Yep, but it's not as drippy.</p>
        </section>
      </div>
    </div>
  );
};

export default Documentation;