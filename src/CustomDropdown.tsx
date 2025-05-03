import { useEffect, useRef, useState } from "react";
import { FiChevronDown } from "react-icons/fi";
import i18next from "i18next";

const CustomDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const getLanguageLabel = (lng: string) => {
    switch (lng) {
      case "en":
        return "English";
      case "bis":
        return "Bisaya";
      case "tl":
        return "Tagalog";
      default:
        return "English";
    }
  };
  
  const [selected, setSelected] = useState(getLanguageLabel(i18next.language));

  const handleSelect = (value: string) => {
    setSelected(value);
    setIsOpen(false);
    console.log(`Selected language: ${value}`);

    // Update i18next language based on selection
    switch(value) {
      case "English":
        i18next.changeLanguage("en");
        break;
      case "Bisaya":
        i18next.changeLanguage("bis");
        break;
      case "Tagalog":
        i18next.changeLanguage("tl");
        break;
      default:
        i18next.changeLanguage("en");
        break;
    }
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

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
          className="bg-[#0F0A27] text-white py-2 px-8 rounded-[50px] flex items-center justify-between w-auto"
          onClick={toggleDropdown}
        >
          <span>{selected}</span>
          <FiChevronDown
            className={`ml-3 w-5 h-5 transition-transform duration-200 ${
              isOpen ? "rotate-180" : ""
            }`}
          />
        </button>
      </div>

      {/* Dropdown menu */}
      {isOpen && (
        <div className="absolute left-0 mt-2 bg-black rounded-[10px] shadow-lg z-10 w-[160px]">
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