import { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import CustomDropdown from './CustomDropdown';
import { FaBars } from 'react-icons/fa';

const TopNavigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        sidebarRef.current && !sidebarRef.current.contains(event.target as Node) &&
        overlayRef.current && !overlayRef.current.contains(event.target as Node)
      ) {
        setSidebarOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Utility function to check if the link is active
  const isActive = (path: string) => location.pathname === path;

  return (
    <div
      className="sticky top-0 w-full flex items-center justify-between text-white py-10"
      style={{
        backgroundImage: "url('/TopNavBG.png')",
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
        backgroundSize: 'cover',
      }}
    >
      {/* Left - Logo */}
      <div
        className="cursor-pointer flex items-center ml-4 sm:ml-[90px] space-x-2"
        onClick={() => navigate('/vibeprogramminglanguage/home')}
      >
        <div style={{ height: '40px', width: '40px' }}>
          <img
            src="/VibeLangLogo.svg"
            alt="Vibe Logo"
            style={{ height: '100%', width: '100%', objectFit: 'contain' }}
          />
        </div>
        <span className="text-white font-semibold text-2xl">VIBE</span>
      </div>

      {/* Center - Navigation Links (Desktop Only) */}
      <div className="hidden sm:flex space-x-12 font-semibold">
        <button
          onClick={() => navigate('/vibeprogramminglanguage/home')}
          className={`bg-transparent border-none p-0 m-0 transition ${isActive('/vibeprogramminglanguage/home') ? 'text-transparent bg-clip-text bg-gradient-to-r from-[#BF2ECE] to-[#881CE5]' : 'text-white'}`}
        >
          Home
        </button>
        <button
          onClick={() => navigate('/vibeprogramminglanguage/docs')}
          className={`bg-transparent border-none p-0 m-0 transition ${isActive('/vibeprogramminglanguage/docs') ? 'text-transparent bg-clip-text bg-gradient-to-r from-[#BF2ECE] to-[#881CE5]' : 'text-white'}`}
        >
          Documentation
        </button>
        <button
          onClick={() => navigate('/vibeprogramminglanguage/playground')}
          className={`bg-transparent border-none p-0 m-0 transition ${isActive('/vibeprogramminglanguage/playground') ? 'text-transparent bg-clip-text bg-gradient-to-r from-[#BF2ECE] to-[#881CE5]' : 'text-white'}`}
        >
          Playground
        </button>
        <button
          onClick={() => navigate('/vibeprogramminglanguage/developers')}
          className={`bg-transparent border-none p-0 m-0 transition ${isActive('/vibeprogramminglanguage/developers') ? 'text-transparent bg-clip-text bg-gradient-to-r from-[#BF2ECE] to-[#881CE5]' : 'text-white'}`}
        >
          Developers
        </button>
      </div>

      {/* Right - Language Dropdown (Desktop Only) */}
      <div className="hidden sm:block">
        <CustomDropdown />
      </div>

      {/* Mobile Burger Icon */}
      <div className="sm:hidden flex items-center mr-5">
        <FaBars size={24} onClick={() => setSidebarOpen(true)} />
      </div>

      {/* Mobile Sidebar (From the Right) */}
      {sidebarOpen && (
  <div
    ref={overlayRef}
    className="fixed inset-0 bg-black bg-opacity-60 sm:hidden"
    onClick={() => setSidebarOpen(false)} // Close sidebar when overlay is clicked
    style={{ pointerEvents: 'auto' }} // Allow clicks on the overlay to close it
  >
    <div
      ref={sidebarRef}
      className="absolute top-0 right-0 w-[250px] h-full bg-[#0F0A27] p-6 flex flex-col mt-4 space-y-5 transform transition-transform ease-in-out duration-300"
      style={{ transform: sidebarOpen ? 'translateX(0)' : 'translateX(100%)', pointerEvents: 'auto' }} // Sidebar content is clickable
      onClick={(e) => e.stopPropagation()} // Prevent click on sidebar from closing it
    >
      <button
        onClick={() => navigate('/vibeprogramminglanguage/home')}
        className="text-base sm:text-2xl font-semibold"
      >
        Home
      </button>
      <button
        onClick={() => navigate('/vibeprogramminglanguage/docs')}
        className="text-base sm:text-2xl font-semibold"
      >
        Documentation
      </button>
      <button
        onClick={() => navigate('/vibeprogramminglanguage/playground')}
        className="text-base sm:text-2xl font-semibold"
      >
        Playground
      </button>
      <button
        onClick={() => navigate('/vibeprogramminglanguage/developers')}
        className="text-base sm:text-2xl font-semibold"
      >
        Developers
      </button>
      <div className="flex-col ml-6 justify-center text-base sm:text-2xl font-semibold">
        <CustomDropdown />
      </div>
    </div>
  </div>
)}


    </div>
  )
};

export default TopNavigation;