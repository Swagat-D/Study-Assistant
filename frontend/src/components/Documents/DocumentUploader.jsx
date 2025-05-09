import { useState, useRef, useContext } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  Paper, 
  CircularProgress, 
  Alert,
  Stack,
  Chip
} from '@mui/material';
import { UploadFile, PictureAsPdf, Description } from '@mui/icons-material';
import { DocumentContext } from '../../context/DocumentContext';

function DocumentUploader({ isUploading, setIsUploading }) {
  const fileInputRef = useRef(null);
  const { documents, setDocuments } = useContext(DocumentContext);
  const [uploadError, setUploadError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  
  const allowedFileTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ];
  
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };
  
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };
  
  const handleClick = () => {
    fileInputRef.current.click();
  };
  
  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };
  
  const handleFiles = (files) => {
    setUploadError(null);
    setIsUploading(true);
    
    // Check if files are valid
    const validFiles = Array.from(files).filter(file => 
      allowedFileTypes.includes(file.type)
    );
    
    if (validFiles.length === 0) {
      setUploadError('Only PDF and Word documents are supported.');
      setIsUploading(false);
      return;
    }
    
    // Process each valid file
    const uploadPromises = validFiles.map(file => {
      return new Promise((resolve) => {
        // In a real app, this would be an API call to your backend
        // Simulating upload delay
        setTimeout(() => {
          const newDocument = {
            id: Date.now() + Math.random().toString(36).substr(2, 9),
            name: file.name,
            type: file.type,
            size: file.size,
            uploadDate: new Date().toISOString(),
            content: 'This is a placeholder for the actual document content. In a real application, this would be processed and stored by the backend.',
            pages: file.type === 'application/pdf' ? Math.floor(Math.random() * 20) + 5 : null,
          };
          
          resolve(newDocument);
        }, 1000);
      });
    });
    
    Promise.all(uploadPromises)
      .then(newDocuments => {
        setDocuments([...documents, ...newDocuments]);
        setIsUploading(false);
      })
      .catch(error => {
        console.error('Error uploading documents:', error);
        setUploadError('An error occurred while uploading documents.');
        setIsUploading(false);
      });
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
    <Paper 
      sx={{ 
        p: 3,
        border: dragActive ? `2px dashed ${theme => theme.palette.primary.main}` : '2px dashed #ccc',
        backgroundColor: dragActive ? 'rgba(63, 81, 181, 0.08)' : 'inherit',
        transition: 'all 0.3s ease',
      }}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <Box 
        sx={{ 
          textAlign: 'center', 
          p: 3,
          cursor: 'pointer',
        }}
        onClick={handleClick}
      >
        {isUploading ? (
          <CircularProgress sx={{ mb: 2 }} />
        ) : (
          <UploadFile 
            sx={{ 
              fontSize: 60, 
              color: theme => theme.palette.primary.main,
              mb: 2,
            }} 
          />
        )}
        
        <Typography variant="h6" gutterBottom>
          {isUploading ? 'Uploading...' : 'Upload Documents'}
        </Typography>
        
        <Typography variant="body2" color="textSecondary" paragraph>
          Drag and drop your files here, or click to browse
        </Typography>
        
        <Stack direction="row" spacing={1} justifyContent="center" mb={2}>
          <Chip 
            icon={<PictureAsPdf />} 
            label="PDF" 
            variant="outlined" 
          />
          <Chip 
            icon={<Description />} 
            label="DOCX" 
            variant="outlined" 
          />
        </Stack>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.docx"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        
        <Button 
          variant="contained" 
          component="span"
          disabled={isUploading}
          onClick={(e) => {
            e.stopPropagation();
            handleClick();
          }}
        >
          Browse Files
        </Button>
      </Box>
      
      {uploadError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {uploadError}
        </Alert>
      )}
    </Paper>
  );
}

export default DocumentUploader;