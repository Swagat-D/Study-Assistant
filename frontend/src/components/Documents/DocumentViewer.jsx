import { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Skeleton, 
  Paper, 
  Toolbar, 
  IconButton,
  Tooltip,
  Chip,
  Divider 
} from '@mui/material';
import { 
  ZoomIn, 
  ZoomOut, 
  ChatBubble, 
  School, 
  Article,
  SkipPrevious,
  SkipNext
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

function DocumentViewer({ document }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [zoom, setZoom] = useState(1);
  
  useEffect(() => {
    if (document) {
      // Simulate loading the document content
      setLoading(true);
      const timer = setTimeout(() => {
        setLoading(false);
      }, 1000);
      
      return () => clearTimeout(timer);
    }
  }, [document]);
  
  const handleZoomIn = () => {
    setZoom(prev => Math.min(prev + 0.1, 2.0));
  };
  
  const handleZoomOut = () => {
    setZoom(prev => Math.max(prev - 0.1, 0.5));
  };
  
  const handlePrevPage = () => {
    setCurrentPage(prev => Math.max(prev - 1, 1));
  };
  
  const handleNextPage = () => {
    if (document.pages) {
      setCurrentPage(prev => Math.min(prev + 1, document.pages));
    }
  };
  
  const handleChat = () => {
    navigate('/chat');
  };
  
  const handleStudyTools = () => {
    navigate('/study-tools');
  };
  
  if (!document) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <Typography variant="body1" color="textSecondary">
          Select a document to view
        </Typography>
      </Box>
    );
  }
  
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar 
        variant="dense" 
        sx={{ 
          backgroundColor: theme => theme.palette.background.default,
          borderRadius: 1,
          mb: 2
        }}
      >
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="subtitle1" noWrap>
            {document.name}
          </Typography>
        </Box>
        
        {document.pages && (
          <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
            <IconButton size="small" onClick={handlePrevPage} disabled={currentPage === 1}>
              <SkipPrevious />
            </IconButton>
            <Typography variant="body2" sx={{ mx: 1 }}>
              {currentPage} / {document.pages}
            </Typography>
            <IconButton size="small" onClick={handleNextPage} disabled={currentPage === document.pages}>
              <SkipNext />
            </IconButton>
          </Box>
        )}
        
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
          <IconButton size="small" onClick={handleZoomOut}>
            <ZoomOut />
          </IconButton>
          <Typography variant="body2" sx={{ mx: 1 }}>
            {Math.round(zoom * 100)}%
          </Typography>
          <IconButton size="small" onClick={handleZoomIn}>
            <ZoomIn />
          </IconButton>
        </Box>
        
        <Tooltip title="Chat with this document">
          <IconButton onClick={handleChat}>
            <ChatBubble />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Study tools">
          <IconButton onClick={handleStudyTools}>
            <School />
          </IconButton>
        </Tooltip>
      </Toolbar>
      
      <Box sx={{ mt: 1, mb: 2 }}>
        <Chip 
          icon={document.type.includes('pdf') ? <Article /> : <Description />} 
          label={document.type.includes('pdf') ? 'PDF Document' : 'Word Document'} 
          size="small"
          variant="outlined" 
        />
      </Box>
      
      <Divider sx={{ mb: 2 }} />
      
      <Box 
        sx={{ 
          flex: 1, 
          overflow: 'auto',
          border: theme => `1px solid ${theme.palette.divider}`,
          borderRadius: 1,
          p: 2,
          backgroundColor: theme => theme.palette.background.paper,
          transform: `scale(${zoom})`,
          transformOrigin: 'top left',
          transition: 'transform 0.2s ease',
        }}
      >
        {loading ? (
          <>
            <Skeleton variant="rectangular" width="100%" height={200} />
            <Skeleton variant="text" width="90%" sx={{ mt: 2 }} />
            <Skeleton variant="text" width="95%" />
            <Skeleton variant="text" width="85%" />
            <Skeleton variant="text" width="90%" />
            <Skeleton variant="rectangular" width="100%" height={150} sx={{ mt: 2 }} />
            <Skeleton variant="text" width="80%" sx={{ mt: 2 }} />
            <Skeleton variant="text" width="85%" />
          </>
        ) : (
          <Box>
            <Typography variant="body1" paragraph>
              This is a simulated document viewer. In a real implementation, this would display the actual content of "{document.name}".
            </Typography>
            <Typography variant="body1" paragraph>
              The document content would be processed and rendered using libraries like PDF.js for PDFs or appropriate libraries for Word documents.
            </Typography>
            <Typography variant="body1" paragraph>
              You can use the controls above to navigate between pages, zoom in/out, and access tools like chat and study aids.
            </Typography>
            <Typography variant="body1" paragraph>
              When implemented, this view would show page {currentPage} of the document at {Math.round(zoom * 100)}% zoom level.
            </Typography>
            
            {/* Simulate page content */}
            <Box sx={{ my: 4, py: 2, px: 3, border: '1px solid #ddd', borderRadius: 1 }}>
              <Typography variant="h6" gutterBottom>
                Sample Content - Page {currentPage}
              </Typography>
              <Typography variant="body2">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris. Vivamus hendrerit arcu sed erat molestie vehicula. Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor. 
              </Typography>
              <Typography variant="body2" sx={{ mt: 2 }}>
                Ut in nulla enim. Phasellus molestie magna non est bibendum non venenatis nisl tempor. Suspendisse dictum feugiat nisl ut dapibus. Mauris iaculis porttitor posuere. 
              </Typography>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default DocumentViewer;