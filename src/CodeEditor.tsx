import React, { useRef, useEffect } from 'react';
import { Editor, OnMount } from '@monaco-editor/react';

type CodeEditorProps = {
    language?: string;
    value?: string; // Changed from defaultValue to value for controlled component
    onChange?: (value: string) => void; // Removed undefined from return type
};

const CodeEditor: React.FC<CodeEditorProps> = ({
    language = 'vibe',
    value = '', // Changed from defaultValue to value
    onChange
}) => {
    // Use 'any' type for monaco editor instance to avoid direct import
    const editorRef = useRef<any>(null);
    const monacoRef = useRef<any>(null);

    // Define editor options
    const editorOptions = {
        automaticLayout: true,
        tabSize: 4,
        detectIndentation: false,
        wordWrap: 'on',
        autoIndent: 'full',
        formatOnType: true,
        formatOnPaste: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        fontSize: 14,
        suggestOnTriggerCharacters: true,
        quickSuggestions: {
            other: true,
            comments: true,
            strings: false
        },
        acceptSuggestionOnEnter: "on",
        tabCompletion: "on",
        snippetSuggestions: "inline"
    };

    // Sample code to verify highlighting works - updated with correct syntax
    const sampleCode = `~ This is a sample vibe code
starterPack {
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

    // Language metadata for autocompletion - updated with correct syntax from the table
    const vibeKeywords = [
        { label: 'starterPack', kind: 'keyword', detail: 'Initialize a new Vibe pack', insertText: 'starterPack {\n\t$0\n}', insertTextRules: 4 },
        { label: 'shoutout', kind: 'function', detail: 'Print to console (equivalent to print())', insertText: 'shoutout($0)', insertTextRules: 4 },
        { label: 'smash', kind: 'keyword', detail: 'Conditional statement (if)', insertText: 'smash($0) {\n\t\n}', insertTextRules: 4 },
        { label: 'maybe', kind: 'keyword', detail: 'Alternative condition (else if)', insertText: 'maybe($0) {\n\t\n}', insertTextRules: 4 },
        { label: 'pass', kind: 'keyword', detail: 'Final condition (else)', insertText: 'pass {\n\t$0\n}', insertTextRules: 4 },
        { label: 'grind', kind: 'keyword', detail: 'While loop construct', insertText: 'grind($0) {\n\t\n}', insertTextRules: 4 },
        { label: 'yeet', kind: 'keyword', detail: 'For loop construct', insertText: 'yeet($0) {\n\t\n}', insertTextRules: 4 },
        { label: 'serve', kind: 'keyword', detail: 'Function declaration (equivalent to function)', insertText: 'serve $0() {\n\t\n}', insertTextRules: 4 },
        { label: 'staph', kind: 'keyword', detail: 'Stop execution (equivalent to break)', insertText: 'staph;', insertTextRules: 4 },
        { label: 'noCap', kind: 'constant', detail: 'Boolean true value', insertText: 'noCap', insertTextRules: 0 },
        { label: 'cap', kind: 'constant', detail: 'Boolean false value', insertText: 'cap', insertTextRules: 0 },
        { label: 'ghosted', kind: 'constant', detail: 'Null value', insertText: 'ghosted', insertTextRules: 0 },
        { label: 'clout', kind: 'keyword', detail: 'Integer data type', insertText: 'clout', insertTextRules: 0 },
        { label: 'ratio', kind: 'keyword', detail: 'Float data type', insertText: 'ratio', insertTextRules: 0 },
        { label: 'tea', kind: 'keyword', detail: 'String data type', insertText: 'tea', insertTextRules: 0 },
        { label: 'mood', kind: 'keyword', detail: 'Boolean data type', insertText: 'mood', insertTextRules: 0 },
        { label: 'gang', kind: 'keyword', detail: 'Array/List data type', insertText: 'gang', insertTextRules: 0 },
        { label: 'wiki', kind: 'keyword', detail: 'Dictionary/map data structure', insertText: 'wiki', insertTextRules: 0 },
        { label: 'tryhard-flopped', kind: 'keyword', detail: 'Try-catch block', insertText: 'tryhard-flopped {\n\t$0\n}', insertTextRules: 4 },
        { label: 'chooseYourFighter', kind: 'function', detail: 'Switch statement', insertText: 'chooseYourFighter($0) {\n\t\n}', insertTextRules: 4 },
        { label: 'itsGiving', kind: 'function', detail: 'Get type of variable (equivalent to typeOf())', insertText: 'itsGiving($0)', insertTextRules: 4 },
        { label: 'spillTheTea', kind: 'function', detail: 'Get user input (equivalent to input())', insertText: 'spillTheTea($0)', insertTextRules: 4 },
    ];

    // Code snippets
    const vibeSnippets = [
        {
            label: 'vibeblock',
            kind: 'snippet',
            detail: 'Create a basic Vibe block',
            insertText: [
                'starterPack {',
                '\tshoutout("Hello Vibe World")',
                '\t$0',
                '}'
            ].join('\n'),
            insertTextRules: 4 // snippets
        },
        {
            label: 'conditional',
            kind: 'snippet',
            detail: 'Create a conditional statement',
            insertText: [
                'smash($1) {',
                '\t$2',
                '} maybe($3) {',
                '\t$4',
                '} pass {',
                '\t$0',
                '}'
            ].join('\n'),
            insertTextRules: 4
        },
        // ... other snippets remain the same
    ];

    // Define the Vibe language tokens with explicit styling
    const defineVibeLanguage = (monaco: any) => {
        // Register language
        monaco.languages.register({ id: 'vibe' });

        // Define token styles with custom theme
        monaco.editor.defineTheme('vibe-purple', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: 'keyword', foreground: 'C586C0', fontStyle: 'bold' },
                { token: 'constant', foreground: '569CD6' },
                { token: 'string', foreground: 'CE9178' },
                { token: 'number', foreground: 'B5CEA8' },
                { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
                { token: 'operator', foreground: 'D4D4D4' },
                { token: 'function', foreground: 'DCDCAA' },
                { token: 'identifier', foreground: '9CDCFE' },
                { token: 'datatype', foreground: '4EC9B0', fontStyle: 'italic' },
            ],
            colors: {
                'editor.background': '#0f0a27', // Custom purple background
                'editor.lineHighlightBackground': '#1b1243', // Slightly lighter for line highlight
                'editorCursor.foreground': '#d4d4d4',
                'editor.selectionBackground': '#264f78',
                'editor.inactiveSelectionBackground': '#3a3d41',
                'editorIndentGuide.background': '#404040',
            }
        });

        // Set syntax highlighting rules - updated with correct syntax
        monaco.languages.setMonarchTokensProvider('vibe', {
            defaultToken: 'invalid',
            tokenizer: {
                root: [
                    // Keywords with special styling
                    [/\b(starterPack|smash|maybe|pass|grind|yeet|serve|staph|wiki)\b/, 'keyword'],
                    // Data Types
                    [/\b(clout|ratio|tea|mood|gang)\b/, 'datatype'],
                    // Functions
                    [/\b(shoutout|chooseYourFighter|itsGiving|spillTheTea)\b/, 'function'],
                    // Constants
                    [/\b(noCap|cap|ghosted)\b/, 'constant'],
                    // Strings
                    [/"([^"\\]|\\.)*"/, 'string'],
                    // Numbers
                    [/\b\d+(\.\d+)?\b/, 'number'],
                    // Comments
                    [/~.*$/, 'comment'],
                    // Brackets
                    [/[{}()\[\]]/, '@brackets'],
                    // Operators
                    [/[+\-*/=<>!&|]+/, 'operator'],
                    // Identifiers
                    [/[a-zA-Z_][\w$]*/, 'identifier'],
                    // Whitespace
                    [/[ \t\r\n]+/, '']
                ],
            },
        });

        // Set language configuration
        monaco.languages.setLanguageConfiguration('vibe', {
            comments: {
                lineComment: '~',
            },
            brackets: [
                ['{', '}'],
                ['[', ']'],
                ['(', ')'],
            ],
            autoClosingPairs: [
                { open: '{', close: '}' },
                { open: '[', close: ']' },
                { open: '(', close: ')' },
                { open: '"', close: '"' },
            ],
            surroundingPairs: [
                { open: '{', close: '}' },
                { open: '[', close: ']' },
                { open: '(', close: ')' },
                { open: '"', close: '"' },
            ],
            folding: {
                markers: {
                    start: new RegExp('^\\s*\\{\\s*$'),
                    end: new RegExp('^\\s*\\}\\s*$')
                }
            },
            wordPattern: /(-?\d*\.\d\w*)|([^\`\~\!\@\#\%\^\&\*\(\)\-\=\+\[\{\]\}\\\|\;\:\'\"\,\.\<\>\/\?\s]+)/g
        });

        // Register completions provider
        monaco.languages.registerCompletionItemProvider('vibe', {
            provideCompletionItems: (model: any, position: any) => {
                // Create the suggestion context
                const suggestions = [...vibeKeywords, ...vibeSnippets].map(item => {
                    // Convert string kind to monaco.languages.CompletionItemKind enum value
                    const kindMap: Record<string, number> = {
                        'keyword': 14, // monaco.languages.CompletionItemKind.Keyword
                        'constant': 17, // monaco.languages.CompletionItemKind.Constant
                        'function': 1,  // monaco.languages.CompletionItemKind.Function
                        'snippet': 27,  // monaco.languages.CompletionItemKind.Snippet
                        'datatype': 7   // monaco.languages.CompletionItemKind.Class (for data types)
                    };

                    return {
                        label: item.label,
                        kind: kindMap[item.kind] || 0,
                        documentation: item.detail,
                        insertText: item.insertText,
                        insertTextRules: item.insertTextRules,
                        range: {
                            startLineNumber: position.lineNumber,
                            startColumn: Math.max(1, position.column - item.label.length),
                            endLineNumber: position.lineNumber,
                            endColumn: position.column
                        }
                    };
                });

                return { suggestions };
            },
            triggerCharacters: ['', ' ', '.', '{', '(']
        });

        // Register hover provider
        monaco.languages.registerHoverProvider('vibe', {
            provideHover: (model: any, position: any) => {
                const word = model.getWordAtPosition(position);
                if (!word) return null;

                const keyword = [...vibeKeywords, ...vibeSnippets].find(k => k.label === word.word);
                if (keyword) {
                    return {
                        contents: [
                            { value: `**${keyword.label}**` },
                            { value: keyword.detail }
                        ]
                    };
                }
                return null;
            }
        });

        // Register signature help provider for functions
        monaco.languages.registerSignatureHelpProvider('vibe', {
            signatureHelpTriggerCharacters: ['('],
            provideSignatureHelp: (model: any, position: any) => {
                // Get content up to cursor to find current function call
                const textUntilPosition = model.getValueInRange({
                    startLineNumber: 1,
                    startColumn: 1,
                    endLineNumber: position.lineNumber,
                    endColumn: position.column
                });

                // Find the function being called
                const keywordMatches = textUntilPosition.match(/(\w+)\s*\([^)]*$/);
                if (keywordMatches) {
                    const keyword = keywordMatches[1];

                    // Define signature help for specific functions
                    const signatures: Record<string, any> = {
                        'shoutout': {
                            label: 'shoutout(message)',
                            documentation: 'Display a message (equivalent to print())',
                            parameters: [{ label: 'message', documentation: 'The message to display' }]
                        },
                        'itsGiving': {
                            label: 'itsGiving(value)',
                            documentation: 'Returns the type of the provided value',
                            parameters: [{ label: 'value', documentation: 'The value to check the type of' }]
                        },
                        // Other signatures remain the same
                    };

                    const sig = signatures[keyword];
                    if (sig) {
                        return {
                            signatures: [
                                {
                                    label: sig.label,
                                    documentation: sig.documentation,
                                    parameters: sig.parameters
                                }
                            ],
                            activeSignature: 0,
                            activeParameter: 0
                        };
                    }
                }
                return null;
            }
        });
    };

    // Effect to update editor content when value prop changes
    useEffect(() => {
        if (editorRef.current) {
            const currentValue = editorRef.current.getValue();
            if (value !== currentValue) {
                editorRef.current.setValue(value);
            }
        }
    }, [value]);

    // Handle editor mounting
    const handleEditorDidMount: OnMount = (editor, monaco) => {
        editorRef.current = editor;
        monacoRef.current = monaco;

        // Define and register our custom language
        defineVibeLanguage(monaco);

        // Apply the custom theme
        monaco.editor.setTheme('vibe-purple');

        // Create a new model with the vibe language
        const model = monaco.editor.createModel(
            value || sampleCode,
            'vibe',
            monaco.Uri.parse('file:///main.vibe')
        );

        // Set the editor's model
        editor.setModel(model);

        // Add change event listener
        editor.onDidChangeModelContent(() => {
            const newValue = editor.getValue();
            if (onChange) {
                onChange(newValue);
            }
        });

        // Focus the editor
        setTimeout(() => {
            editor.focus();
        }, 100);
    };

    return (
        <div className="w-full h-full flex flex-col border border-gray-700 rounded-md overflow-hidden">
            <Editor
                height="100%"
                theme="vibe-purple"
                defaultValue={value || sampleCode}
                options={editorOptions}
                onMount={handleEditorDidMount}
            />
        </div>
    );
};

export default CodeEditor;