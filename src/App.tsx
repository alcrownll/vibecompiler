import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import VibeCompiler from './VibeCompiler'
import './index.css'

function App() {
  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/vibeprogramminglanguage/home" replace />} />

        {/* Main route */}
        <Route path="/vibeprogramminglanguage/*" element={<VibeCompiler />} />
      </Routes>
    </Router>
  )
}

export default App
