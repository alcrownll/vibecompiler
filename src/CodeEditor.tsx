import { useRef } from 'react';
import { Editor, OnMount } from '@monaco-editor/react';
import * as monaco from 'monaco-editor';

interface CodeEditorProps {
    language: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ language }) => {
    const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

    const editorOptions: monaco.editor.IStandaloneEditorConstructionOptions = {
        automaticLayout: true,
        tabSize: 4,
        detectIndentation: false,
        wordWrap: 'on',
        autoIndent: 'full',
        formatOnType: true,
        formatOnPaste: true,
    };

    const onMount: OnMount = (editor) => {
        editorRef.current = editor;
        editor.focus();
    };

    return (
        <div className="w-full h-[85vh] flex flex-col">
            <div className="relative flex-1 w-full">
                <Editor
                    height="100%"
                    theme="vs-dark"
                    language={language}
                    options={editorOptions}
                    onMount={onMount}
                />
            </div>
        </div>
    );
};

export default CodeEditor;
