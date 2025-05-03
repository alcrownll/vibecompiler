const Playground = () => {
  return (
    <div className="min-h-screen text-white px-4 flex flex-col items-center justify-start py-10">
      
      {/* Top Container */}
      <div className="w-full max-w-7xl flex justify-between items-center mb-6 px-2">
        {/* Left Text */}
        <span className="text-gray-300 text-sm">
          Don’t know where to start? <a href="/docs" className="underline text-blue-400">Check Documentation</a>
        </span>

        {/* Right Buttons */}
        <div className="flex space-x-3">
          <button className="bg-gray-700 hover:bg-gray-600 text-white px-10 py-2 rounded-[50px]">Save</button>
          <button className="bg-gradient-to-r from-[#BF2ECE] to-[#881CE5] text-white px-10 py-2 rounded-[50px]">Run</button>
        </div>
      </div>

      {/* Bottom Container */}
      <div className="flex w-full max-w-7xl space-x-4">
        
        {/* Left Container */}
        <div className="w-3/4 relative rounded-lg overflow-hidden min-h-[500px]">
          <div
            className="absolute inset-0 bg-cover bg-center opacity-10"
            style={{ backgroundImage: "url('/BiggerContainer.svg')" }}
          ></div>
          <div className="relative p-6 z-10">
            <h2 className="text-xl font-semibold">Left Container</h2>
            <p>For Code Editor</p>
          </div>
        </div>

        {/* Right Container */}
        <div className="w-1/2 relative rounded-lg overflow-hidden min-h-[500px]">
          <div
            className="absolute inset-0 bg-cover bg-center opacity-10"
            style={{ backgroundImage: "url('/BiggerContainer.svg')" }}
          ></div>
          <div className="relative p-6 z-10">
            <h2 className="text-xl font-semibold">Right Container</h2>
            <p>For Output</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;