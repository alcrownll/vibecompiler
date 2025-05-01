import { Routes, Route } from 'react-router-dom';
import TopNavigation from './TopNavigation';
import Home from './pages/Home';
import Documentation from './pages/Documentation';
import Compiler from './pages/Compiler';

const VibeCompiler = () => {
  return (
    // Full-page black background and white text
    <div className="text-white h-full flex flex-col">

      <div className="w-full h-[60px] flex">
        <TopNavigation />
      </div>

      {/* Content Area: flex-1 to fill remaining space */}
      <div className="flex-1 p-4 overflow-y-auto">
        <Routes>
          <Route path="home" element={<Home />} />
          <Route path="docs" element={<Documentation />} />
          <Route path="compiler" element={<Compiler />} />
        </Routes>
      </div>
    </div>
  );
};

export default VibeCompiler;
