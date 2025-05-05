const Developers = () => {
  // Developer data
  const developers = [
    {
      name: "Goddess Valdehuesa",
      title: "UCLM-BSCS 3A",
      role: "CEO & Co-Founder",
      description: "Leads product vision and sustainability strategy; bridges tech with climate impact.",
      imageUrl: "/GP.svg"
    },
    {
      name: "Johana Taboada",
      title: "UCLM-BSCS 3A",
      role: "CTO & Co-Founder",
      description: "Oversees AI and backend development; builds scalable, automated systems.",
      imageUrl: "/JT.svg"
    },
    {
      name: "Denise Aliah Cabiso",
      title: "UCLM-BSCS 3A",
      role: "CPO & Co-Founder",
      description: "Leads UI/UX and frontend; designs seamless, user-driven experiencesss.",
      imageUrl: "/DA.svg"
    },
    {
      name: "Shania Jaynn Anino",
      title: "UCLM-BSCS 3A",
      role: "CSO & Co-Founder",
      description: "Focuses on security infrastructure and compliance; ensures data protection.",
      imageUrl: null
    }
  ];

  return (
    <div className="py-2 px-4 md:px-8 lg:px-16">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-7"> </div>
          <h2 className="text-navy-900 text-5xl md:text-6xl font-bold">
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
              {/* Display SVG image or placeholder with zoom effect */}
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
                  <p className="text-gray text-sm">{developer.title}</p>
                  
                  <div className="inline-block bg-blue-50 text-cyan-500 rounded-full px-4 py-1 mt-2 text-sm font-medium">
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