const Developers = () => {

  const developers = [
    {
      name: "Goddess Valdehuesa",
      role: "UCLM-BSCS 3A",
      description: "Led frontend development, UI design, and language syntax creation for Vibe.",
      imageUrl: "/GP.svg"
    },
    {
      name: "Johana Taboada",
      role: "UCLM-BSCS 3A",
      description: "Managed security and database systems for the project.",
      imageUrl: "/JT.svg"
    },
    {
      name: "Denise Aliah Cabiso",
      role: "UCLM-BSCS 3A",
      description: "Worked on Vibe’s frontend interface for seamless user experience.",
      imageUrl: "/DA.svg"
    },
    {
      name: "Shania Jaynn Anino",
      role: "UCLM-BSCS 3A",
      description: "Led compiler integration and backend execution flow.",
      imageUrl: "/SJ.svg"
    }
  ];

  return (
    <div className="py-2 px-4 md:px-8 lg:px-16">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-7"> </div>
          <h2 className="text-navy-900 text-4xl md:text-5xl font-bold">
            The Team Building<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#BF2ECE] to-[#881CE5]">VIBE</span> Compiler
          </h2>
        </div>

        {/* Developers Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {developers.map((developer, index) => (
            <div 
              key={index} 
              className="rounded-2xl overflow-hidden shadow-md transform transition duration-300 hover:scale-105 hover:shadow-xl"
            >
              {/* Display */}
              <div className="h-60 bg-black/10 overflow-hidden">
                {developer.imageUrl ? (
                  <div className="h-full w-full overflow-hidden">
                    <img 
                      src={developer.imageUrl} 
                      alt={`${developer.name}`}
                      className="h-full w-full object-cover transition duration-300 transform hover:scale-110"
                    />
                  </div>
                ) : (
                  <div className="text-gray-400 h-full flex items-center justify-center">Developer Image</div>
                )}
              </div>
              
              <div className="p-6 bg-white/10">
                <div className="text-center mb-4">
                  <h3 className="text-navy-900 font-bold text-xl">{developer.name}</h3>
                  
                  <div className="inline-block bg-blue-50 text-[#881CE5] rounded-full px-4 py-1 mt-2 text-sm font-medium">
                    {developer.role}
                  </div>
                </div>
                
                <p className="text-white/50 text-center text-sm">
                  {developer.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Developers;