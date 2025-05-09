import { useContext } from 'react';
import { 
  Typography, 
  Box, 
  Button, 
  Card, 
  CardContent, 
  Grid, 
  Container 
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { DocumentContext } from '../context/DocumentContext';

function Home() {
  const navigate = useNavigate();
  const { documents } = useContext(DocumentContext);

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 8 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Welcome to Study Assistant
        </Typography>
        <Typography variant="h5" align="center" color="textSecondary" paragraph>
          Upload documents, ask questions, and study smarter with AI-powered assistance
        </Typography>
        <Box display="flex" justifyContent="center" mt={4}>
          <Button 
            variant="contained" 
            color="primary" 
            size="large" 
            onClick={() => navigate('/documents')}
            sx={{ mr: 2 }}
          >
            Upload Documents
          </Button>
          <Button 
            variant="outlined" 
            color="primary" 
            size="large" 
            onClick={() => navigate('/chat')}
            disabled={documents.length === 0}
          >
            Start Chatting
          </Button>
        </Box>
      </Box>

      <Grid container spacing={4}>
        <Grid xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Document Q&A
              </Typography>
              <Typography>
                Upload PDF and Word documents and ask questions about their content in real-time.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Smart Summaries
              </Typography>
              <Typography>
                Get instant summaries of your documents to quickly understand key concepts.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid xs={12} sm={6} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Study Tools
              </Typography>
              <Typography>
                Generate flashcards, quizzes, and study guides from your documents.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {documents.length > 0 && (
        <Box mt={6}>
          <Typography variant="h5" gutterBottom>
            Recent Documents
          </Typography>
          <Grid container spacing={2}>
            {documents.slice(0, 3).map((doc, index) => (
              <Grid xs={12} sm={6} md={4} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">{doc.name}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      Uploaded: {new Date(doc.uploadDate).toLocaleDateString()}
                    </Typography>
                    <Button 
                      size="small" 
                      sx={{ mt: 1 }}
                      onClick={() => navigate('/chat')}
                    >
                      Chat with this document
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );
}

export default Home;