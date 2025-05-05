import { useEffect, useRef, useState } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

interface OutputProps {
    output: string;
}

const Output: React.FC<OutputProps> = ({ output }) => {
    const terminalRef = useRef<HTMLDivElement | null>(null);
    const containerRef = useRef<HTMLDivElement | null>(null);
    const [terminalInstance, setTerminalInstance] = useState<Terminal | null>(null);

    // Create terminal on mount
    useEffect(() => {
        if (!terminalRef.current) return;

        // Apply CSS to xterm container to force it to fill available space
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

        // Force the terminal to fill container
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

    // Handle output changes
    useEffect(() => {
        if (!terminalInstance) return;

        terminalInstance.clear();
        if (output) {
            terminalInstance.write(output);
        } else {
            terminalInstance.write('Click "Run" to see the output here');
        }
    }, [output, terminalInstance]);

    // Update terminal size on container size changes
    useEffect(() => {
        if (!terminalInstance || !containerRef.current) return;

        const updateTerminalSize = () => {
            if (!containerRef.current) return;

            // Get container dimensions
            const containerWidth = containerRef.current.clientWidth;
            const containerHeight = containerRef.current.clientHeight;

            // Calculate approximate character dimensions based on font size
            const charWidth = terminalInstance.options.fontSize ? terminalInstance.options.fontSize * 0.6 : 8;
            const charHeight = terminalInstance.options.fontSize ? terminalInstance.options.fontSize * 1.2 : 17;

            // Calculate cols and rows that would fit in the container
            const cols = Math.floor(containerWidth / charWidth);
            const rows = Math.floor(containerHeight / charHeight);

            // Resize terminal with calculated dimensions
            terminalInstance.resize(Math.max(cols, 10), Math.max(rows, 10));
        };

        // Call once for initial sizing
        updateTerminalSize();

        // Set up resize observer for container
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