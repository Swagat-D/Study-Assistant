import { useState, useContext, useEffect } from 'react';
import { Container, Typography, Box, Paper, Grid, Divider } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { DocumentContext } from '../context/DocumentContext';
import ChatInterface from '../components/chat/ChatInterface';
import DocumentList from '../components/Documents/DocumentList';

function Chat() {
  const navigate = useNavigate();
  const { documents, activeDocument, setActiveDocument } = useContext(DocumentContext);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Hello! I\'m your study assistant. Ask me questions about your documents and I\'ll help you understand them better.',
      timestamp: new Date(),
    }
  ]);

  // Check if documents are available, if not redirect to documents page
  useEffect(() => {
    if (!documents || documents.length === 0) {
      navigate('/documents');
    }
  }, [documents, navigate]);

  const handleDocumentSelect = (document) => {
    if (document) {
      setActiveDocument(document);
      
      // Add a system message
      setMessages(prev => [
        ...prev,
        {
          id: Date.now(),
          sender: 'bot',
          text: `Now focusing on "${document.name}". What would you like to know about this document?`,
          timestamp: new Date(),
        }
      ]);
    }
  };

  const handleSendMessage = (text) => {
    if (!text || !text.trim()) return;
    
    // Add user message
    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Simulate response (this would connect to your backend in production)
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        sender: 'bot',
        text: `I'm analyzing your question about ${activeDocument ? activeDocument.name : 'your documents'}. In a real implementation, this would be answered by the backend using RAG.`,
        timestamp: new Date(),
        // This is where you'd include source info in a real implementation
        source: activeDocument ? { 
          document: activeDocument.name, 
          page: Math.floor(Math.random() * 5) + 1 
        } : null,
      };
      
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom>
        Chat with Your Documents
      </Typography>
      
      <Grid container spacing={3}>
        <Grid xs={12} sm={4} md={3}>
          <Paper sx={{ p: 2, height: '70vh', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Your Documents
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {documents && documents.length > 0 ? (
              <DocumentList 
                documents={documents} 
                activeDocument={activeDocument} 
                onDocumentSelect={handleDocumentSelect}
                compact
              />
            ) : (
              <Typography variant="body2" color="textSecondary" align="center" sx={{ mt: 4 }}>
                No documents uploaded yet
              </Typography>
            )}
          </Paper>
        </Grid>
        
        <Grid xs={12} sm={8} md={9}>
          <Paper sx={{ p: 0, height: '70vh', display: 'flex', flexDirection: 'column' }}>
            {activeDocument && (
              <Box p={2} bgcolor="primary.light" color="white">
                <Typography variant="subtitle1">
                  Chatting with: {activeDocument.name}
                </Typography>
              </Box>
            )}
            
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
            />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Chat;