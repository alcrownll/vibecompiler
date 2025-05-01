const Documentation = () => {
  return (
    <div className="h-screen overflow-y-scroll no-scrollbar px-8 py-12 text-white max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold mb-6">VibeLang Documentation</h1>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-2">🚀 What is VibeLang?</h2>
        <p>
          VibeLang is a fun, expressive programming language that turns Gen Z slang into code.
          It's designed for relatability and creative expression while maintaining real programming power.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-2">📝 Syntax Basics</h2>
        <ul className="list-disc ml-6 space-y-2">
          <li><strong>let's vibe</strong> — Declares a variable. (e.g., <code>let's vibe mood = "chill"</code>)</li>
          <li><strong>fr</strong> — Boolean true (e.g., <code>let's vibe isCool = fr</code>)</li>
          <li><strong>nah</strong> — Boolean false (e.g., <code>let's vibe isLame = nah</code>)</li>
          <li><strong>say</strong> — Prints output to console (e.g., <code>say "hello bestie"</code>)</li>
          <li><strong>on god</strong> — Used for asserting something or writing conditions.</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-2">🔁 Loops & 💅 Functions</h2>
        <p className="mb-2">
          Loops in VibeLang use <code>keep it up</code>, and functions are declared with <code>glow up</code>.
        </p>
        <pre className="bg-[#1f1f1f] p-4 rounded-lg text-sm overflow-x-auto">
{`glow up greet(bestie) {
  say "hey " + bestie
}

keep it up (i < 3) {
  greet("queen")
}`}
        </pre>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-2">💡 Tips</h2>
        <ul className="list-disc ml-6 space-y-2">
          <li>Keep your vibe consistent. Use relatable terms consistently.</li>
          <li>Mixing standard JS and VibeLang terms is allowed but not encouraged for full drip.</li>
        </ul>
      </section>
    </div>
  );
};

export default Documentation;
