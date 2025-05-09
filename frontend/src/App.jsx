import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './styles/theme';

// Pages
import Home from './pages/Home';
import Chat from './pages/Chat';
import Documents from './pages/Documents';
import StudyTools from './pages/StudyTools';

// Components
import Navbar from './components/UI/Navbar';
import Sidebar from './components/UI/Sidebar';
import { DocumentContext } from './context/DocumentContext';

function App() {
  const [documents, setDocuments] = useState([]);
  const [activeDocument, setActiveDocument] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <DocumentContext.Provider value={{ documents, setDocuments, activeDocument, setActiveDocument }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <div className="app-container" style={{ display: 'flex', height: '100vh' }}>
            <Sidebar open={sidebarOpen} />
            
            <div style={{ flex: 1, overflow: 'auto' }}>
              <Navbar toggleSidebar={toggleSidebar} />
              
              <main style={{ padding: '20px' }}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/chat" element={<Chat />} />
                  <Route path="/documents" element={<Documents />} />
                  <Route path="/study-tools" element={<StudyTools />} />
                </Routes>
              </main>
            </div>
          </div>
        </Router>
      </ThemeProvider>
    </DocumentContext.Provider>
  );
}

export default App;