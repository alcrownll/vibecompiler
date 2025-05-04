import { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

interface OutputProps {
    output: string;
}

const Output: React.FC<OutputProps> = ({ output }) => {
    const terminalRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const terminal = new Terminal({
            theme: {
                background: '#1e1e1e',
                foreground: '#ffffff',
            },
            fontSize: 14,
            scrollback: 1000,
        });

        if (terminalRef.current) {
            terminal.open(terminalRef.current);

            if (output) {
                terminal.write(output);
            } else {
                terminal.write('Click "Run" to see the output here');
            }
        }

        return () => {
            terminal.dispose();
        };
    }, [output]);

    return (
        <div className="w-full h-[50vh] border border-gray-600 rounded-md">
            <div
                ref={terminalRef}
                className="w-full h-full"
            />
        </div>
    );
};

export default Output;
