import { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  TextField, 
  IconButton, 
  InputAdornment, 
  Typography,
  CircularProgress
} from '@mui/material';
import { 
  Send as SendIcon, 
  Mic as MicIcon, 
  AttachFile as AttachFileIcon 
} from '@mui/icons-material';
import ChatMessage from './ChatMessage';

function ChatInterface({ messages = [], onSendMessage }) {
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };
  
  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
      setIsTyping(true);
      
      // Simulate bot typing
      setTimeout(() => {
        setIsTyping(false);
      }, 1000);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box sx={{ 
        flex: 1, 
        overflowY: 'auto', 
        p: 2, 
        display: 'flex', 
        flexDirection: 'column' 
      }}>
        {Array.isArray(messages) && messages.length > 0 ? (
          messages.map((message) => (
            message && typeof message === 'object' && 'id' in message ? (
              <ChatMessage 
                key={message.id} 
                message={message} 
              />
            ) : null
          ))
        ) : (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100%' 
          }}>
            <Typography variant="body1" color="textSecondary">
              No messages yet. Start a conversation!
            </Typography>
          </Box>
        )}
        
        {isTyping && (
          <Box sx={{ display: 'flex', alignItems: 'center', ml: 2, mt: 1 }}>
            <CircularProgress size={16} sx={{ mr: 1 }} />
            <Typography variant="caption" color="textSecondary">
              AI is typing...
            </Typography>
          </Box>
        )}
        
        <div ref={messagesEndRef} />
      </Box>
      
      <Paper
        elevation={3}
        sx={{
          p: 2,
          borderTop: '1px solid',
          borderColor: 'divider',
          backgroundColor: theme => theme.palette.background.paper,
        }}
      >
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask a question about your documents..."
          value={inputValue}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          multiline
          maxRows={4}
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            },
          }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton color="primary">
                  <AttachFileIcon />
                </IconButton>
                <IconButton color="primary">
                  <MicIcon />
                </IconButton>
                <IconButton 
                  color="primary" 
                  onClick={handleSend}
                  disabled={!inputValue.trim()}
                >
                  <SendIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Paper>
    </Box>
  );
}

export default ChatInterface;