const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-white text-center px-4">
      <h1 className="text-7xl font-bold mb-4">Vibe Programming Language</h1>
      <p className="text-lg mb-6 max-w-4xl">
        Vibe is a fresh, Gen Z–inspired programming language that turns everyday slang and internet lingo into real, expressive code—making development more relatable, fun, and intuitive.
      </p>
      <div className="flex space-x-4">
      <div className="p-[2px] rounded-full bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] inline-block hover:opacity-90 transition">
        <button className="bg-[#0F0A27] text-white font-semibold py-3 px-14 rounded-full">
          Learn More
        </button>
      </div>

        <button className="bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-white font-semibold py-3 px-14 rounded-full hover:opacity-90 transition">
          Code Now
        </button>
      </div>
    </div>
  );
};

export default Home;