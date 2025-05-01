import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate(); // Access the navigate function

  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-white  text-center px-4">
      <div className="flex items-center justify-center py-4 px-10">
        <h2 className="text-2xl mb-2 font-semibold text-[#a5a0bc]">
          Definition of Vibe Coding. Rewritten.
        </h2>
      </div>

      <h1 className="text-7xl font-bold mb-6 leading-[1.15] bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-transparent bg-clip-text">
        Vibe Programming Language
      </h1>

      <p className="text-lg mb-6 max-w-4xl text-white">
        Vibe is a fresh, Gen Z–inspired programming language that turns everyday slang and internet lingo into real, expressive code—making development more relatable, fun, and intuitive.
      </p>

      <div className="flex space-x-4 mt-2 mb-6">
        {/* Learn More Button */}
        <div className="p-[2px] rounded-full bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] inline-block hover:opacity-90 transition">
          <button 
            className="bg-[#0F0A27] text-white font-semibold py-3 px-14 rounded-full"
            onClick={() => navigate('/vibeprogramminglanguage/docs')} // Navigate to Documentation
          >
            Learn More
          </button>
        </div>

        {/* Code Now Button */}
        <button
          className="bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-white font-semibold py-3 px-14 rounded-full hover:opacity-90 transition"
          onClick={() => navigate('/vibeprogramminglanguage/compiler')} // Navigate to Compiler
        >
          Code Now
        </button>
      </div>

      {/* Info Container with Background */}
      <div className="relative w-full max-w-5xl py-12 px-4 rounded-lg text-white overflow-hidden mt-6 mb-12">
        {/* Background Image Layer */}
        <div
          className="absolute inset-0 bg-cover bg-center opacity-10"
          style={{ backgroundImage: "url('/Container.svg')" }}
          aria-hidden="true"
        />

        {/* Foreground Content */}
        <div className="relative z-10 flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-12 text-left">
          {/* Stat 1 */}
          <div className="flex items-center space-x-3">
            <span className="text-4xl text-[#924DC2] font-bold">97%</span>
            <div className="leading-tight text-sm">
              <div>Faster Syntax</div>
              <div>Comprehension</div>
            </div>
          </div>

          {/* Divider */}
          <div className="hidden md:block w-0.5 h-10 bg-[#817D92]"></div>

          {/* Stat 2 */}
          <div className="flex items-center space-x-3">
            <span className="text-4xl text-[#924DC2] font-bold">2.4×</span>
            <div className="leading-tight text-sm">
              <div>Productivity</div>
              <div>Improvement</div>
            </div>
          </div>

          {/* Divider */}
          <div className="hidden md:block w-0.5 h-10 bg-[#817D92]"></div>

          {/* Stat 3 */}
          <div className="flex items-center space-x-3">
            <span className="text-4xl text-[#924DC2] font-bold">10,000+</span>
            <div className="leading-tight text-sm">
              <div>LOC</div>
              <div>Implemented</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
