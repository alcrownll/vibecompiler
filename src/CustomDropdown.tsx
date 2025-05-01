import { useEffect, useRef, useState } from "react";

const CustomDropdown = () => {
  const [selected, setSelected] = useState("English");
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null); // To track the dropdown element

  const handleSelect = (value: string) => {
    setSelected(value);
    setIsOpen(false);
    console.log(`Selected language: ${value}`);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  // Close dropdown if click happens outside the component
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="relative inline-block" ref={dropdownRef}>
      {/* Gradient border wrapper */}
      <div className="p-[2px] rounded-[50px] bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] inline-block mr-[90px] hover:opacity-90 transition">
        <button
          className="bg-[#0F0A27] text-white py-2 px-12 rounded-[50px] flex items-center justify-between w-auto"
          onClick={toggleDropdown}
        >
          <span>{selected}</span>
        </button>
      </div>

      {/* Dropdown menu */}
      {isOpen && (
        <div className="absolute left-0 mt-2 bg-black rounded-[10px] shadow-lg z-10 w-[150px]">
          <div
            className="text-white py-2 px-4 cursor-pointer hover:bg-gray-700 rounded-t-[10px] focus:outline-none"
            onClick={() => handleSelect("English")}
          >
            English
          </div>
          <div
            className="text-white py-2 px-4 cursor-pointer hover:bg-gray-700 focus:outline-none"
            onClick={() => handleSelect("Bisaya")}
          >
            Bisaya
          </div>
          <div
            className="text-white py-2 px-4 cursor-pointer hover:bg-gray-700 rounded-b-[10px] focus:outline-none"
            onClick={() => handleSelect("Tagalog")}
          >
            Tagalog
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomDropdown;
