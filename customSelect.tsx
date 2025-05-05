// components/CustomSelect.tsx
import React, { useState, useRef, useEffect } from 'react';

interface Option {
  value: string;
  label: string;
}

interface CustomSelectProps {
  options: Option[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

const CustomSelect: React.FC<CustomSelectProps> = ({ options, value, onChange, placeholder }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedLabel = options.find(opt => opt.value === value)?.label;

  return (
    <div ref={dropdownRef} className="relative w-[20rem]">
      <button
        className="w-full text-left p-2 bg-gray-800 text-white rounded focus:outline-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        {selectedLabel || placeholder || 'Select an option'}
      </button>

      {isOpen && (
        <ul className="absolute z-10 mt-1 w-full bg-gray-900 text-white border border-gray-700 rounded shadow-lg max-h-60 overflow-y-auto">
          {options.map(option => (
            <li
              key={option.value}
              onClick={() => {
                onChange(option.value);
                setIsOpen(false);
              }}
              className={`p-2 hover:bg-gray-700 cursor-pointer ${
                option.value === value ? 'bg-gray-700' : ''
              }`}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomSelect;
