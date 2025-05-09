import { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Button, 
  IconButton, 
  Skeleton,
  Grid,
  Card,
  CardContent,
  CardActions,
  Divider,
  Chip,
  TextField,
  InputAdornment
} from '@mui/material';
import { 
  NavigateNext, 
  NavigateBefore, 
  Shuffle, 
  Add,
  Edit,
  Delete,
  Search,
  Download
} from '@mui/icons-material';

function Flashcards({ document, isGenerating, flashcards }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredCards, setFilteredCards] = useState([]);
  
  useEffect(() => {
    if (flashcards) {
      setFilteredCards(flashcards);
    }
  }, [flashcards]);
  
  const handleNextCard = () => {
    setFlipped(false);
    setTimeout(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % filteredCards.length);
    }, 300);
  };
  
  const handlePrevCard = () => {
    setFlipped(false);
    setTimeout(() => {
      setCurrentIndex((prevIndex) => (prevIndex - 1 + filteredCards.length) % filteredCards.length);
    }, 300);
  };
  
  const handleFlip = () => {
    setFlipped(!flipped);
  };
  
  const handleShuffle = () => {
    setFlipped(false);
    setFilteredCards(prevCards => {
      const shuffled = [...prevCards];
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
      }
      return shuffled;
    });
    setCurrentIndex(0);
  };
  
  const handleSearch = (e) => {
    const term = e.target.value;
    setSearchTerm(term);
    
    if (!term.trim() && flashcards) {
      setFilteredCards(flashcards);
      return;
    }
    
    if (flashcards) {
      const filtered = flashcards.filter(card => 
        card.front.toLowerCase().includes(term.toLowerCase()) || 
        card.back.toLowerCase().includes(term.toLowerCase())
      );
      setFilteredCards(filtered);
      setCurrentIndex(0);
      setFlipped(false);
    }
  };
  
  if (isGenerating) {
    return (
      <Box>
        <Skeleton variant="rectangular" height={250} sx={{ borderRadius: 2 }} />
        <Box display="flex" justifyContent="center" mt={2}>
          <Skeleton variant="circular" width={40} height={40} sx={{ mx: 1 }} />
          <Skeleton variant="circular" width={40} height={40} sx={{ mx: 1 }} />
          <Skeleton variant="circular" width={40} height={40} sx={{ mx: 1 }} />
        </Box>
        <Skeleton variant="text" height={30} width="60%" sx={{ mt: 2, mx: 'auto' }} />
      </Box>
    );
  }
  
  if (!flashcards || flashcards.length === 0) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="300px">
        <Typography variant="h6" color="textSecondary" gutterBottom>
          Generate flashcards for {document.name}
        </Typography>
        <Typography variant="body2" color="textSecondary" align="center" sx={{ maxWidth: 500, mb: 3 }}>
          Click the "Generate" button above to create flashcards from key concepts in this document
        </Typography>
      </Box>
    );
  }
  
  const currentCard = filteredCards[currentIndex];
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5">Flashcards for {document.name}</Typography>
        <Box>
          <IconButton title="Download flashcards">
            <Download />
          </IconButton>
          <IconButton title="Add new flashcard">
            <Add />
          </IconButton>
          <IconButton onClick={handleShuffle} title="Shuffle flashcards">
            <Shuffle />
          </IconButton>
        </Box>
      </Box>
      
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search flashcards..."
        value={searchTerm}
        onChange={handleSearch}
        sx={{ mb: 3 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
      />
      
      <Box sx={{ mb: 3 }}>
        <Paper
          sx={{
            height: 300,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            cursor: 'pointer',
            transition: 'transform 0.6s',
            transformStyle: 'preserve-3d',
            transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
            position: 'relative',
            borderRadius: 2,
          }}
          onClick={handleFlip}
          elevation={3}
        >
          {/* Front of card */}
          <Box
            sx={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              backfaceVisibility: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              p: 3,
            }}
          >
            <Typography variant="h5" align="center">
              {currentCard.front}
            </Typography>
            <Typography
              variant="caption"
              sx={{ position: 'absolute', bottom: 10, right: 10 }}
            >
              Click to flip
            </Typography>
          </Box>
          
          {/* Back of card */}
          <Box
            sx={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              backfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              p: 3,
              bgcolor: 'primary.light',
              color: 'white',
              borderRadius: 2,
            }}
          >
            <Typography variant="h6" align="center">
              {currentCard.back}
            </Typography>
            <Typography
              variant="caption"
              sx={{ position: 'absolute', bottom: 10, right: 10 }}
            >
              Click to flip
            </Typography>
          </Box>
        </Paper>
      </Box>
      
      <Box display="flex" justifyContent="center" alignItems="center" mb={3}>
        <IconButton onClick={handlePrevCard} disabled={filteredCards.length <= 1}>
          <NavigateBefore />
        </IconButton>
        <Typography variant="body2" sx={{ mx: 2 }}>
          {currentIndex + 1} of {filteredCards.length}
        </Typography>
        <IconButton onClick={handleNextCard} disabled={filteredCards.length <= 1}>
          <NavigateNext />
        </IconButton>
      </Box>
      
      <Divider sx={{ mb: 3 }} />
      
      <Typography variant="h6" gutterBottom>
        All Flashcards
      </Typography>
      
      <Grid container spacing={2}>
        {filteredCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={4} key={card.id}>
            <Card 
              variant="outlined" 
              sx={{ 
                height: '100%',
                bgcolor: currentIndex === index ? 'rgba(63, 81, 181, 0.05)' : 'inherit',
                border: currentIndex === index ? '1px solid' : 'inherit',
                borderColor: currentIndex === index ? 'primary.main' : 'inherit',
              }}
            >
              <CardContent>
                <Typography variant="subtitle1" gutterBottom noWrap>
                  {card.front}
                </Typography>
                <Typography variant="body2" color="textSecondary" noWrap>
                  {card.back}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => {
                  setCurrentIndex(index);
                  setFlipped(false);
                }}>
                  Study
                </Button>
                <IconButton size="small">
                  <Edit fontSize="small" />
                </IconButton>
                <IconButton size="small">
                  <Delete fontSize="small" />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default Flashcards;