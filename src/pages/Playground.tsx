import { useState } from 'react';
import CodeEditor from '../CodeEditor';
import Output from '../Output';

const Playground = () => {
  const [editorCode, setEditorCode] = useState('');
  const [outputText, setOutput] = useState('');

  // Function to run code
  const runCode = async () => {
    try {
      const response = await fetch('http://localhost:5000/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: editorCode })
      });

      const result = await response.json();
      if (result.success) {
        setOutput(result.output);
      } else {
        setOutput(`Error: ${result.error}`);
      }
    } catch (error: any) {
      setOutput(`Network Error: ${error.message}`);
    }
  };

  return (
    <div className="min-h-screen text-white px-4 flex flex-col items-center justify-start py-10">
      {/* Top Container */}
      <div className="w-full max-w-7xl flex justify-between items-center mb-6 px-2">
        <span className="text-gray-300 text-sm">
          Don't know where to start? <a href="/docs" className="underline text-blue-400">Check Documentation</a>
        </span>
        <div className="flex space-x-3">
          <button className="bg-gray-700 hover:bg-gray-600 text-white px-10 py-2 rounded-[50px]">Save</button>
          <button
            className="bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-white px-10 py-2 rounded-[50px]"
            onClick={runCode}
          >
            Run
          </button>
        </div>
      </div>

      {/* Bottom Container */}
      <div className="flex w-full max-w-7xl space-x-4">
        <div className="w-2/3 relative rounded-lg overflow-hidden h-[500px]">
          <div
            className="absolute inset-0 bg-cover bg-center opacity-10"
            style={{ backgroundImage: "url('/BiggerContainer.svg')" }}
          ></div>
          <div className="relative z-10 h-full">
            {/* CodeEditor now receives setEditorCode */}
            <CodeEditor language='vibe' />
          </div>
        </div>

        <div className="w-1/3 relative rounded-lg overflow-hidden h-[500px]">
          <div className="relative z-10 w-full h-full">
            <div className="h-full">
              <Output output={outputText} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;
