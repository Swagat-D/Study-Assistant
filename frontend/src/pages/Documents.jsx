import { useState, useContext } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  List, 
  Divider, 
  Grid 
} from '@mui/material';
import { DocumentContext } from '../context/DocumentContext';
import DocumentUploader from '../components/Documents/DocumentUploader';
import DocumentList from '../components/Documents/DocumentList';
import DocumentViewer from '../components/Documents/DocumentViewer';

function Documents() {
  const { documents, activeDocument, setActiveDocument } = useContext(DocumentContext);
  const [isUploading, setIsUploading] = useState(false);

  const handleDocumentSelect = (document) => {
    setActiveDocument(document);
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom>
        Your Documents
      </Typography>
      <Typography variant="body1" paragraph>
        Upload PDF and Word documents to chat with them and generate study materials.
      </Typography>

      <Box mb={3}>
        <DocumentUploader 
          isUploading={isUploading} 
          setIsUploading={setIsUploading} 
        />
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              Your Documents ({documents.length})
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {documents.length > 0 ? (
              <DocumentList 
                documents={documents} 
                activeDocument={activeDocument} 
                onDocumentSelect={handleDocumentSelect} 
              />
            ) : (
              <Typography variant="body2" color="textSecondary" align="center" sx={{ mt: 4 }}>
                No documents uploaded yet
              </Typography>
            )}
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
            {activeDocument ? (
              <DocumentViewer document={activeDocument} />
            ) : (
              <Box 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center'
                }}
              >
                <Typography variant="body1" color="textSecondary">
                  Select a document to view its content
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Documents;