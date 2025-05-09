/* eslint-disable react-hooks/rules-of-hooks */
import { useState } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  Avatar, 
  Chip,
  Link,
  Tooltip,
  IconButton,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  useTheme
} from '@mui/material';
import { 
  SmartToy as BotIcon, 
  ContentCopy as CopyIcon,
  Check as CheckIcon,
  MoreVert as MoreVertIcon,
  Delete as DeleteIcon,
  Flag as FlagIcon,
  Bookmark as BookmarkIcon,
  Share as ShareIcon,
  Visibility as VisibilityIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  Article as ArticleIcon
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';

function ChatMessage({ message, onDelete, onViewSource }) {
  // Early return if message is invalid
  if (!message || typeof message !== 'object' || !('sender' in message)) {
    console.error('Invalid message object passed to ChatMessage:', message);
    return null;
  }
  
  const theme = useTheme();
  const [copied, setCopied] = useState(false);
  const [menuAnchorEl, setMenuAnchorEl] = useState(null);
  const [showFullContent, setShowFullContent] = useState(false);
  const isBot = message.sender === 'bot';
  
  // Handle actions
  const handleCopy = () => {
    navigator.clipboard.writeText(message.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  const handleMenuOpen = (event) => {
    setMenuAnchorEl(event.currentTarget);
    event.stopPropagation();
  };
  
  const handleMenuClose = () => {
    setMenuAnchorEl(null);
  };
  
  const handleDelete = () => {
    handleMenuClose();
    if (onDelete) {
      onDelete(message.id);
    }
  };
  
  const handleViewSource = () => {
    handleMenuClose();
    if (onViewSource && message.source) {
      onViewSource(message.source);
    }
  };
  
  // Check if message is long and needs to be collapsed
  const messageText = message.text || '';
  const isLongMessage = messageText.length > 500;
  const displayedContent = !showFullContent && isLongMessage 
    ? messageText.substring(0, 500) + '...' 
    : messageText;
  
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isBot ? 'flex-start' : 'flex-end',
        mb: 2,
        maxWidth: '100%',
        animation: 'messageAppear 0.3s ease-out',
      }}
    >
      {isBot && (
        <Avatar
          sx={{
            bgcolor: theme.palette.primary.main,
            width: 36,
            height: 36,
            mr: 1,
            mt: 1,
          }}
        >
          <BotIcon fontSize="small" />
        </Avatar>
      )}
      
      <Box sx={{ maxWidth: { xs: '85%', md: '75%' } }}>
        <Paper
          elevation={1}
          sx={{
            p: 2,
            borderRadius: 2,
            backgroundColor: isBot 
              ? theme.palette.background.paper
              : theme.palette.primary.main,
            color: isBot ? 'inherit' : 'white',
            position: 'relative',
            overflowWrap: 'break-word',
            wordBreak: 'break-word',
          }}
        >
          <Box sx={{ mr: isBot ? 4 : 0 }}>
            {/* Chat message content */}
            <Typography 
              variant="body1" 
              component="div"
              sx={{ 
                whiteSpace: 'pre-wrap', 
                '& a': {
                  color: isBot ? theme.palette.primary.main : 'white',
                  textDecoration: 'underline',
                },
                '& code': {
                  backgroundColor: isBot ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.1)',
                  padding: '2px 4px',
                  borderRadius: '4px',
                  fontFamily: 'monospace',
                },
                '& pre': {
                  backgroundColor: isBot ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.1)',
                  padding: '8px',
                  borderRadius: '4px',
                  overflowX: 'auto',
                },
              }}
            >
              {isBot ? (
                <ReactMarkdown>
                  {displayedContent}
                </ReactMarkdown>
              ) : (
                displayedContent
              )}
            </Typography>
            
            {/* Show more/less button for long messages */}
            {isLongMessage && (
              <Typography 
                variant="body2" 
                color={isBot ? "primary" : "inherit"}
                sx={{ 
                  mt: 1, 
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  fontWeight: 'medium',
                  opacity: 0.9,
                }}
                onClick={() => setShowFullContent(!showFullContent)}
              >
                {showFullContent ? 'Show less' : 'Show more'}
              </Typography>
            )}
            
            {/* Source citation if available */}
            {isBot && message.source && (
              <Box sx={{ mt: 2, pt: 1, borderTop: `1px solid ${theme.palette.divider}` }}>
                <Box display="flex" alignItems="center">
                  <ArticleIcon fontSize="small" sx={{ mr: 0.5, color: theme.palette.text.secondary }} />
                  <Typography variant="caption" color="textSecondary">
                    Source: {message.source.document}, Page {message.source.page}
                  </Typography>
                </Box>
                <Link 
                  href="#" 
                  variant="caption" 
                  sx={{ display: 'inline-block', mt: 0.5 }}
                  onClick={(e) => {
                    e.preventDefault();
                    handleViewSource();
                  }}
                >
                  View in document
                </Link>
              </Box>
            )}
          </Box>
          
          {/* Action buttons for messages */}
          <Box 
            sx={{ 
              position: 'absolute', 
              top: 8, 
              right: 8, 
              display: 'flex',
              gap: 0.5,
            }}
          >
            <Tooltip title={copied ? "Copied!" : "Copy text"}>
              <IconButton
                size="small"
                onClick={handleCopy}
                sx={{
                  opacity: 0.6,
                  color: isBot ? 'inherit' : 'white',
                  '&:hover': {
                    opacity: 1,
                  },
                }}
              >
                {copied ? <CheckIcon fontSize="small" /> : <CopyIcon fontSize="small" />}
              </IconButton>
            </Tooltip>
            
            <IconButton
              size="small"
              onClick={handleMenuOpen}
              sx={{
                opacity: 0.6,
                color: isBot ? 'inherit' : 'white',
                '&:hover': {
                  opacity: 1,
                },
              }}
            >
              <MoreVertIcon fontSize="small" />
            </IconButton>
            
            <Menu
              id="message-menu"
              anchorEl={menuAnchorEl}
              open={Boolean(menuAnchorEl)}
              onClose={handleMenuClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
            >
              <MenuItem onClick={handleCopy}>
                <ListItemIcon>
                  <CopyIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Copy text</ListItemText>
              </MenuItem>
              
              {isBot && message.source && (
                <MenuItem onClick={handleViewSource}>
                  <ListItemIcon>
                    <VisibilityIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>View source</ListItemText>
                </MenuItem>
              )}
              
              <MenuItem>
                <ListItemIcon>
                  <BookmarkIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Save response</ListItemText>
              </MenuItem>
              
              <MenuItem>
                <ListItemIcon>
                  <ShareIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Share</ListItemText>
              </MenuItem>
              
              {isBot && (
                <MenuItem>
                  <ListItemIcon>
                    <FlagIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Report issue</ListItemText>
                </MenuItem>
              )}
              
              <MenuItem onClick={handleDelete}>
                <ListItemIcon>
                  <DeleteIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>Delete</ListItemText>
              </MenuItem>
            </Menu>
          </Box>
        </Paper>
        
        {/* Timestamp and feedback options */}
        <Box 
          sx={{ 
            display: 'flex', 
            alignItems: 'center',
            justifyContent: isBot ? 'flex-start' : 'flex-end',
            mt: 0.5,
          }}
        >
          <Typography 
            variant="caption" 
            color="textSecondary"
          >
            {message.timestamp ? new Date(message.timestamp).toLocaleTimeString([], { 
              hour: '2-digit', 
              minute: '2-digit' 
            }) : ''}
          </Typography>
          
          {isBot && (
            <Box sx={{ display: 'flex', ml: 1 }}>
              <Tooltip title="Helpful">
                <IconButton size="small">
                  <ThumbUpIcon fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Not helpful">
                <IconButton size="small">
                  <ThumbDownIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
          )}
        </Box>
      </Box>
      
      {!isBot && (
        <Avatar
          sx={{
            bgcolor: theme.palette.secondary.main,
            width: 36,
            height: 36,
            ml: 1,
            mt: 1,
          }}
        >
          {/* User initial */}
          U
        </Avatar>
      )}
    </Box>
  );
}

export default ChatMessage;