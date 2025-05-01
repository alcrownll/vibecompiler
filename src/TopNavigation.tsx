import { useNavigate } from 'react-router-dom'

const TopNavigation: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div
      className="w-full flex items-center justify-between text-white py-10"
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
        <div style={{ height: '45px', width: '45px' }}>
          <img
            src="/Vibe.svg"
            alt="Vibe Logo"
            style={{ height: '100%', width: '100%', objectFit: 'contain' }}
          />
        </div>
        <span className="text-white font-semibold text-2xl">VIBE</span>
      </div>


      {/* Center - Navigation Links */}
      <div className="flex space-x-10 text-white font-medium">
      <button
          onClick={() => navigate('/vibeprogramminglanguage/home')}
          className="bg-transparent border-none p-0 m-0 text-white transition"
        >
          Home
        </button>
        <button 
          onClick={() => navigate('/vibeprogramminglanguage/docs')} 
          className="bg-transparent border-none p-0 m-0 transition"
        >
          Documentation
        </button>
        <button 
          onClick={() => navigate('/vibeprogramminglanguage/compiler')} 
          className="bg-transparent border-none p-0 m-0 transition"
        >
          Compiler
        </button>
        <button 
          onClick={() => navigate('/vibeprogramminglanguage/compiler')} 
          className="bg-transparent border-none p-0 m-0 transition"
        >
          Developers
        </button>
      </div>



      {/* Right - Language Dropdown */}
      <div>
        <select
          className="bg-transparent border border-white text-white pl-7 pr-10 py-2 rounded-[50px] mr-[90px] appearance-none"
          defaultValue="english"
          onChange={(e) => console.log(`Selected language: ${e.target.value}`)}
        >
          <option value="english">English</option>
          <option value="bisaya">Bisaya</option>
          <option value="tagalog">Tagalog</option>
        </select>
      </div>
    </div>
  )
}

export default TopNavigation