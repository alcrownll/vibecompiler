const Compiler = () => {
  return (
    <div className="min-h-screen text-white px-4 flex flex-col items-center justify-start">
      
      {/* Flex container for side-by-side layout */}
      <div className="flex w-full max-w-7xl space-x-4 mt-20">
        
        {/* Left Container with more width */}
        <div className="w-3/4 relative rounded-lg overflow-hidden min-h-[500px]">
          {/* Background Overlay */}
          <div
            className="absolute inset-0 bg-cover bg-center opacity-10"
            style={{ backgroundImage: "url('/BiggerContainer.svg')" }}
          ></div>
          
          {/* Add content for the left container */}
          <div className="relative p-6 z-10">
            <h2 className="text-xl font-semibold">Left Container</h2>
            <p>For Code Editor</p>
          </div>
        </div>
        
        {/* Right Container with bigger width */}
        <div className="w-1/2 relative rounded-lg overflow-hidden min-h-[500px]">
          {/* Background Overlay */}
          <div
            className="absolute inset-0 bg-cover bg-center opacity-10"
            style={{ backgroundImage: "url('/BiggerContainer.svg')" }}
          ></div>
          
          {/* Add content for the right container */}
          <div className="relative p-6 z-10">
            <h2 className="text-xl font-semibold">Right Container</h2>
            <p>For Output</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Compiler;