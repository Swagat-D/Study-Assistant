import { 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  ListItemSecondaryAction, 
  IconButton, 
  Typography,
  Menu,
  MenuItem,
  Tooltip,
  Box
} from '@mui/material';
import { 
  PictureAsPdf, 
  Description, 
  MoreVert, 
  Delete, 
  Share, 
  Download 
} from '@mui/icons-material';
import { useState } from 'react';

function DocumentList({ documents, activeDocument, onDocumentSelect, compact = false }) {
  const [menuAnchorEl, setMenuAnchorEl] = useState(null);
  const [ setCurrentDocId] = useState(null);
  
  const handleMenuOpen = (event, docId) => {
    event.stopPropagation();
    setMenuAnchorEl(event.currentTarget);
    setCurrentDocId(docId);
  };
  
  const handleMenuClose = (event) => {
    if (event) event.stopPropagation();
    setMenuAnchorEl(null);
  };
  
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };
  
  const getFileTypeIcon = (fileType) => {
    switch (fileType) {
      case 'application/pdf':
        return <PictureAsPdf />;
      case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return <Description />;
      default:
        return <Description />;
    }
  };
  
  return (
    <List>
      {documents.map((doc) => (
        <ListItem 
          button 
          key={doc.id}
          selected={activeDocument && activeDocument.id === doc.id}
          onClick={() => onDocumentSelect(doc)}
          sx={{ borderRadius: 1 }}
        >
          <ListItemIcon>
            {getFileTypeIcon(doc.type)}
          </ListItemIcon>
          
          <ListItemText 
            primary={doc.name}
            secondary={
              !compact && (
                <>
                  <Typography 
                    component="span" 
                    variant="body2" 
                    color="textSecondary"
                    display="block"
                  >
                    {formatFileSize(doc.size)}
                  </Typography>
                  <Typography 
                    component="span" 
                    variant="body2" 
                    color="textSecondary"
                  >
                    {formatDate(doc.uploadDate)}
                  </Typography>
                </>
              )
            }
          />
          
          {!compact && (
            <ListItemSecondaryAction>
              <IconButton 
                edge="end" 
                aria-label="more"
                onClick={(e) => handleMenuOpen(e, doc.id)}
              >
                <MoreVert />
              </IconButton>
            </ListItemSecondaryAction>
          )}
        </ListItem>
      ))}
      
      <Menu
        anchorEl={menuAnchorEl}
        open={Boolean(menuAnchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>
          <ListItemIcon>
            <Download fontSize="small" />
          </ListItemIcon>
          <ListItemText primary="Download" />
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <ListItemIcon>
            <Share fontSize="small" />
          </ListItemIcon>
          <ListItemText primary="Share" />
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <ListItemIcon>
            <Delete fontSize="small" />
          </ListItemIcon>
          <ListItemText primary="Delete" />
        </MenuItem>
      </Menu>
    </List>
  );
}

export default DocumentList;