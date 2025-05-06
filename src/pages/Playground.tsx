import { useState } from 'react';
import CodeEditor from '../CodeEditor';
import Output from '../Output';

interface CompileError {
  line: number;
  column: number;
  message: string;
}

const sampleCode = `~ This is a sample vibe code
starterPack myProgram {
    shoutout("Hello Vibe World!")

    ~ Data type examples
    clout myInteger = 42
    ratio myFloat = 3.14
    tea myString = "This is a string"
    mood myBoolean = noCap
    gang myArray = [1, 2, 3, 4, 5]

    ~ Conditional example
    smash(myBoolean) {
        shoutout("This is true!")
    } maybe(myInteger > 50) {
        shoutout("Integer is greater than 50")
    } pass {
        shoutout("This is the else block")
    }
}`;

const Playground = () => {
  const [editorCode, setEditorCode] = useState(sampleCode);
  const [outputText, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasRun, setHasRun] = useState(false);

  const runCode = async () => {
    setIsLoading(true);
    setOutput('');
    setHasRun(true);
    try {
      const response = await fetch('http://localhost:8000/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_code: editorCode })
      });

      const result = await response.json();

      if (result.program_output) {
        setOutput(result.program_output);
      } else if (result.error) {
        setOutput(`Compilation Failed:\n${result.error}`);
      } else if (result.assembly_code) {
        setOutput(result.assembly_code.join('\n'));
      } else {
        setOutput('Unknown error occurred');
      }
    } catch (error: any) {
      setOutput(`Network Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const saveFile = () => {
    const blob = new Blob([editorCode], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'mycode.vibe';
    link.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen text-white px-4 flex flex-col items-center justify-start py-10">
      {/* Top Container */}
      <div className="w-full max-w-7xl flex justify-between items-center mb-6 px-2">
        <span className="text-gray-300 text-sm">
          Don't know where to start? <a href="/docs" className="underline text-blue-400">Check Documentation</a>
        </span>
        <div className="flex space-x-3">
          <button
            className="bg-gray-700 hover:bg-gray-600 text-white px-10 py-2 rounded-[50px]"
            onClick={saveFile}
          >
            Save
          </button>
          <button
            className="bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-white px-10 py-2 rounded-[50px]"
            onClick={runCode}
            disabled={isLoading}
          >
            {isLoading ? 'Running...' : 'Run'}
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
            <CodeEditor
              language="vibe"
              value={editorCode}
              onChange={setEditorCode}
            />
          </div>
        </div>
        <div className="w-1/3 relative rounded-lg overflow-hidden h-[500px]">
          <div className="relative z-10 w-full h-full">
            <div className="h-full">
              <Output output={outputText} hasRun={hasRun} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;
