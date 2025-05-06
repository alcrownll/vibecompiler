import { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

interface OutputProps {
    output: string;
    hasRun: boolean;
}

const Output: React.FC<OutputProps> = ({ output, hasRun }) => {
    const terminalRef = useRef<HTMLDivElement | null>(null);
    const containerRef = useRef<HTMLDivElement | null>(null);
    const [terminalInstance, setTerminalInstance] = useState<Terminal | null>(null);

    useEffect(() => {
        if (!terminalRef.current) return;

        const style = document.createElement('style');
        style.textContent = `
            .xterm-screen, .xterm-viewport {
                width: 100% !important;
                height: 100% !important;
            }
            .xterm {
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100%;
                width: 100%;
            }
            .xterm-viewport {
                background-color: #000000 !important;
            }
        `;
        document.head.appendChild(style);

        const terminal = new Terminal({
            theme: {
                background: '#000000',
                foreground: '#ffffff',
            },
            fontSize: 14,
            scrollback: 1000,
            cursorBlink: false,
            disableStdin: true,
            convertEol: true,
            allowTransparency: true,
        });

        terminal.open(terminalRef.current);

        const xtermElement = terminalRef.current.querySelector('.xterm');
        if (xtermElement) {
            (xtermElement as HTMLElement).style.height = '100%';
            (xtermElement as HTMLElement).style.width = '100%';
        }

        setTerminalInstance(terminal);

        return () => {
            terminal.dispose();
            document.head.removeChild(style);
            setTerminalInstance(null);
        };
    }, []);

    useEffect(() => {
        if (!terminalInstance) return;

        terminalInstance.clear();

        if (output) {
            terminalInstance.write(output.endsWith('\n') ? output : output + '\n');
        } else if (!hasRun) {
            terminalInstance.write('Click "Run" to see the output here\n');
        }
    }, [output, terminalInstance, hasRun]);

    useEffect(() => {
        if (!terminalInstance || !containerRef.current) return;

        const updateTerminalSize = () => {
            if (!containerRef.current) return;

            const containerWidth = containerRef.current.clientWidth;
            const containerHeight = containerRef.current.clientHeight;

            const charWidth = terminalInstance.options.fontSize ? terminalInstance.options.fontSize * 0.6 : 8;
            const charHeight = terminalInstance.options.fontSize ? terminalInstance.options.fontSize * 1.2 : 17;

            const cols = Math.floor(containerWidth / charWidth);
            const rows = Math.floor(containerHeight / charHeight);

            terminalInstance.resize(Math.max(cols, 10), Math.max(rows, 10));
        };

        updateTerminalSize();

        const resizeObserver = new ResizeObserver(() => {
            updateTerminalSize();
        });

        resizeObserver.observe(containerRef.current);

        return () => {
            resizeObserver.disconnect();
        };
    }, [terminalInstance]);

    return (
        <div
            ref={containerRef}
            className="w-full h-full flex flex-col bg-black rounded-md overflow-hidden"
            style={{ position: 'relative', padding: '4px' }}
        >
            <div
                ref={terminalRef}
                className="absolute inset-0"
                style={{
                    height: '100%',
                    width: '100%',
                    overflow: 'hidden'
                }}
            />
        </div>
    );
};

export default Output;
