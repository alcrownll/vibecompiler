import React, { useState } from 'react';
import { ClipboardIcon } from '@heroicons/react/24/outline';

type CodeBlockProps = {
  children: string;
};

const CodeBlock: React.FC<CodeBlockProps> = ({ children }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(children).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };

  const highlightSyntax = (code: string) => {
  const lines = code.split('\n');
  const processedLines = lines.map(line => {
    // If it's a comment line starting with ~
    if (line.trim().startsWith('~')) {
      return `<span style="color: #34D399;">${line}</span>`;
    }

    // Apply syntax highlighting
    let highlighted = line
      // Strings
      .replace(/("(.*?)")/g, '<span style="color: #CE9178;">$1</span>') // Orange

      // Keywords
      .replace(/\b(starterPack|smash|pass|maybe|grind)\b/g, '<span style="color: #C586C0; font-weight: bold;">$1</span>') // Pink
      .replace(/\b(shoutout)\b/g, '<span style="color: #DCDCAA; font-weight: medium;">$1</span>') // Yellow
      .replace(/\b(clout|ratio|gang|tea|mood|wiki)\b/g, '<span style="color: #34D399; font-weight: medium;">$1</span>') // Green
      .replace(/\b(cap|noCap|ghosted)\b/g, '<span style="color: #3D9CD6; font-weight: medium;">$1</span>') // darkblue
      .replace(/([{}()])/g, '<span style="color: #60A5FA;">$1</span>'); // Blue
      

    // Wrap the entire line with a default blue span to catch unstyled text
    return `<span style="color: #78DCFE;">${highlighted}</span>`;
  });

  return processedLines.join('\n');
};


  return (
    <>
      <div className="relative bg-[#0F0A27] text-white rounded-lg mt-4 max-w-[50%] overflow-x-auto">
        {/* Top bar */}
        <div className="flex justify-between items-center text-xs bg-gray-800 text-gray-300 px-3 py-1 rounded-t-lg font-mono">
          <span>.vibe</span>
          <button onClick={copyToClipboard} className="hover:text-white transition">
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>

        {/* Code content */}
        <pre className="p-4 text-sm whitespace-pre overflow-x-auto font-mono">
          {/* Render the highlighted code */}
          <code dangerouslySetInnerHTML={{ __html: highlightSyntax(children) }} />
        </pre>
      </div>
    </>
  );
};

export default CodeBlock;