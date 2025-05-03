import { useNavigate, useLocation } from 'react-router-dom';
import CustomDropdown from './CustomDropdown';



const TopNavigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

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
        className="cursor-pointer flex items-center ml-[90px] space-x-2"
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

      {/* Center - Navigation Links */}
      <div className="flex space-x-12 font-semibold">
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

      {/* Right - Language Dropdown */}
      <div>
        <CustomDropdown />
      </div>
    </div>
  );
};

export default TopNavigation;