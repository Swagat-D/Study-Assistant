import { 
  Box, 
  Typography, 
  Divider, 
  Paper, 
  Skeleton, 
  IconButton,
  Button,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import { 
  ExpandMore, 
  ContentCopy, 
  Download, 
  Print,
  Check
} from '@mui/icons-material';
import { useState } from 'react';

function Summaries({ document, isGenerating, content }) {
  const [summaryType, setSummaryType] = useState(0);
  const [copied, setCopied] = useState(false);
  
  const handleTabChange = (event, newValue) => {
    setSummaryType(newValue);
  };
  
  const handleCopy = () => {
    if (!content) return;
    
    let textToCopy = `Summary of ${document.name}\n\n`;
    content.sections.forEach(section => {
      textToCopy += `${section.heading}\n${section.content}\n\n`;
    });
    
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  if (isGenerating) {
    return (
      <Box>
        <Skeleton variant="text" height={40} width="60%" />
        <Skeleton variant="text" height={30} width="40%" sx={{ mt: 2 }} />
        <Skeleton variant="rectangular" height={100} sx={{ mt: 1 }} />
        <Skeleton variant="text" height={30} width="35%" sx={{ mt: 2 }} />
        <Skeleton variant="rectangular" height={150} sx={{ mt: 1 }} />
        <Skeleton variant="text" height={30} width="45%" sx={{ mt: 2 }} />
        <Skeleton variant="rectangular" height={120} sx={{ mt: 1 }} />
      </Box>
    );
  }
  
  if (!content) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="300px">
        <Typography variant="h6" color="textSecondary" gutterBottom>
          Generate a summary for {document.name}
        </Typography>
        <Typography variant="body2" color="textSecondary" align="center" sx={{ maxWidth: 500, mb: 3 }}>
          Select the type of summary you'd like to generate and click the "Generate" button above
        </Typography>
        
        <Paper sx={{ width: '100%' }}>
          <Tabs
            value={summaryType}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
          >
            <Tab label="Executive Summary" />
            <Tab label="Key Concepts" />
            <Tab label="Chapter by Chapter" />
          </Tabs>
        </Paper>
      </Box>
    );
  }
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">{content.title}</Typography>
        <Box>
          <IconButton 
            onClick={handleCopy}
            title={copied ? "Copied!" : "Copy to clipboard"}
          >
            {copied ? <Check /> : <ContentCopy />}
          </IconButton>
          <IconButton title="Download as PDF">
            <Download />
          </IconButton>
          <IconButton title="Print">
            <Print />
          </IconButton>
        </Box>
      </Box>
      
      <Divider sx={{ mb: 3 }} />
      
      {content.sections.map((section, index) => (
        <Box key={index} mb={3}>
          <Typography variant="h6" gutterBottom color="primary">
            {section.heading}
          </Typography>
          <Typography variant="body1" paragraph>
            {section.content}
          </Typography>
          <Divider sx={{ mt: 2 }} />
        </Box>
      ))}
      
      <Box mt={4}>
        <Typography variant="h6" gutterBottom>
          Additional Insights
        </Typography>
        
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>Main Themes</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              This would contain a thematic analysis of the document, highlighting recurring patterns and ideas.
            </Typography>
          </AccordionDetails>
        </Accordion>
        
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>Key Terminology</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              This would contain important terms and definitions from the document.
            </Typography>
          </AccordionDetails>
        </Accordion>
        
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography>Further Study Suggestions</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              This would contain recommendations for related topics or materials to explore based on this document.
            </Typography>
          </AccordionDetails>
        </Accordion>
      </Box>
    </Box>
  );
}

export default Summaries;