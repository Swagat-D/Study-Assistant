import { useState } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  IconButton, 
  InputAdornment,
  Popover,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import { 
  Send as SendIcon, 
  Mic as MicIcon, 
  AttachFile as AttachFileIcon,
  Image as ImageIcon,
  Description as DocumentIcon,
  FormatQuote as QuoteIcon,
  HelpOutline as HelpIcon
} from '@mui/icons-material';

function ChatInput({ onSendMessage, disabled = false }) {
  const [message, setMessage] = useState('');
  const [anchorEl, setAnchorEl] = useState(null);
  
  const handleAttachClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleAttachClose = () => {
    setAnchorEl(null);
  };
  
  const handleChange = (e) => {
    setMessage(e.target.value);
  };
  
  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  const open = Boolean(anchorEl);
  const id = open ? 'attach-popover' : undefined;
  
  const helpExamples = [
    "Summarize the key concepts in this document",
    "Explain the relationship between X and Y",
    "Create flashcards for the main terms",
    "What are the main arguments for this topic?",
    "Generate practice questions about this material"
  ];
  
  const handleInsertExample = (example) => {
    setMessage(example);
    handleAttachClose();
  };
  
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', p: 2 }}>
      <TextField
        fullWidth
        multiline
        maxRows={4}
        value={message}
        onChange={handleChange}
        onKeyPress={handleKeyPress}
        placeholder="Ask a question about your documents..."
        disabled={disabled}
        sx={{ mr: 1 }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton 
                aria-describedby={id}
                onClick={handleAttachClick}
                disabled={disabled}
              >
                <AttachFileIcon />
              </IconButton>
              <IconButton disabled={disabled}>
                <MicIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
      
      <Button
        variant="contained"
        color="primary"
        endIcon={<SendIcon />}
        onClick={handleSend}
        disabled={!message.trim() || disabled}
      >
        Send
      </Button>
      
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleAttachClose}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
      >
        <List sx={{ width: 250 }}>
          <ListItem button>
            <ListItemIcon>
              <DocumentIcon />
            </ListItemIcon>
            <ListItemText primary="Upload Document" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <ImageIcon />
            </ListItemIcon>
            <ListItemText primary="Upload Image" />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemIcon>
              <HelpIcon />
            </ListItemIcon>
            <ListItemText primary="Example Questions" secondary="Click to insert" />
          </ListItem>
          {helpExamples.map((example, index) => (
            <ListItem 
              button 
              key={index}
              onClick={() => handleInsertExample(example)}
              sx={{ pl: 4 }}
            >
              <ListItemIcon sx={{ minWidth: 36 }}>
                <QuoteIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText 
                primary={example} 
                primaryTypographyProps={{ 
                  variant: 'body2',
                  noWrap: true
                }}
              />
            </ListItem>
          ))}
        </List>
      </Popover>
    </Box>
  );
}

export default ChatInput;