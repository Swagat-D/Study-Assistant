/**
 * Chunk text into smaller segments for processing
 * @param {String} text - The full text to chunk
 * @param {Number} maxChunkSize - Maximum characters per chunk
 * @param {Number} chunkOverlap - Number of characters to overlap between chunks
 * @returns {Array} - Array of text chunks
 */
export const chunkText = (text, maxChunkSize = 1500, chunkOverlap = 100) => {
  if (!text || text.length === 0) {
    return [];
  }
  
  const chunks = [];
  let startIndex = 0;
  
  while (startIndex < text.length) {
    let endIndex = Math.min(startIndex + maxChunkSize, text.length);
    
    // Try to end at a sentence boundary
    if (endIndex < text.length) {
      const potentialBreaks = ['. ', '? ', '! ', '\n\n'];
      let breakFound = false;
      
      // Look for a sentence break within the last 20% of the chunk
      const minBreakPosition = Math.max(startIndex + maxChunkSize * 0.8, startIndex);
      
      for (let i = endIndex; i >= minBreakPosition; i--) {
        for (const breakChar of potentialBreaks) {
          if (text.substring(i - breakChar.length, i) === breakChar) {
            endIndex = i;
            breakFound = true;
            break;
          }
        }
        if (breakFound) break;
      }
    }
    
    // Extract the chunk
    chunks.push(text.substring(startIndex, endIndex));
    
    // Move to the next chunk with overlap
    startIndex = endIndex - chunkOverlap;
  }
  
  return chunks;
};

/**
 * Extract keywords from text
 * @param {String} text - The text to analyze
 * @param {Number} maxKeywords - Maximum number of keywords to extract
 * @returns {Array} - Array of extracted keywords
 */
export const extractKeywords = (text, maxKeywords = 10) => {
  // This is a simplified keyword extraction
  // In a real implementation, this would use NLP libraries or backend services
  
  // Remove common stop words
  const stopWords = ['a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                    'to', 'of', 'in', 'for', 'with', 'on', 'at', 'from', 'by', 'about',
                    'as', 'into', 'like', 'through', 'after', 'over', 'between', 'out',
                    'this', 'that', 'these', 'those', 'it', 'its', 'we', 'they', 'he', 'she'];
  
  // Tokenize and clean text
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, '') // Remove punctuation
    .split(/\s+/) // Split by whitespace
    .filter(word => word.length > 3 && !stopWords.includes(word)); // Filter out stop words and short words
  
  // Count word frequency
  const wordFrequency = {};
  for (const word of words) {
    wordFrequency[word] = (wordFrequency[word] || 0) + 1;
  }
  
  // Sort by frequency and get top keywords
  return Object.entries(wordFrequency)
    .sort((a, b) => b[1] - a[1])
    .slice(0, maxKeywords)
    .map(entry => entry[0]);
};

/**
 * Generate a summary for text
 * @param {String} text - The text to summarize
 * @param {Number} maxLength - Maximum summary length in characters
 * @returns {String} - Generated summary
 */
export const generateSummary = (text, maxLength = 500) => {
  // This is a placeholder for text summarization
  // In a real implementation, this would call a backend service with NLP capabilities
  
  // Simple extractive summary - get first few sentences
  const sentences = text.match(/[^\.!\?]+[\.!\?]+/g) || [];
  let summary = '';
  let currentLength = 0;
  
  for (const sentence of sentences) {
    if (currentLength + sentence.length <= maxLength) {
      summary += sentence;
      currentLength += sentence.length;
    } else {
      break;
    }
  }
  
  return summary;
};

/**
 * Find relevant text passages based on a query
 * @param {String} query - The search query
 * @param {Array} textChunks - Array of text chunks to search
 * @returns {Array} - Array of relevant text passages with scores
 */
export const findRelevantPassages = (query, textChunks) => {
  // This is a simplified relevance function
  // In a real implementation, this would use vector similarity or other NLP techniques
  
  const queryWords = query.toLowerCase().split(/\s+/);
  
  return textChunks.map(chunk => {
    const chunkLower = chunk.toLowerCase();
    let score = 0;
    
    // Simple scoring based on word matches
    for (const word of queryWords) {
      if (word.length > 3) { // Only consider meaningful words
        const regex = new RegExp(word, 'gi');
        const matches = chunkLower.match(regex);
        if (matches) {
          score += matches.length;
        }
      }
    }
    
    // Boost score if chunk contains all query words
    const containsAllWords = queryWords
      .filter(word => word.length > 3)
      .every(word => chunkLower.includes(word));
      
    if (containsAllWords) {
      score *= 2;
    }
    
    return {
      text: chunk,
      score: score
    };
  })
  .filter(item => item.score > 0) // Only include relevant matches
  .sort((a, b) => b.score - a.score); // Sort by relevance score
};

/**
 * Detect the language of a text
 * @param {String} text - The text to analyze
 * @returns {String} - Detected language code (e.g., 'en', 'es', 'fr')
 */
export const detectLanguage = (text) => {
  // This is a placeholder for language detection
  // In a real implementation, this would use a proper language detection library
  
  // Common language markers (simplified)
  const languageMarkers = {
    en: ['the', 'and', 'of', 'to', 'in', 'is', 'it', 'you', 'that', 'was'],
    es: ['el', 'la', 'de', 'en', 'y', 'es', 'que', 'un', 'por', 'para'],
    fr: ['le', 'la', 'de', 'et', 'est', 'en', 'que', 'un', 'pour', 'dans'],
    de: ['der', 'die', 'und', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'auf']
  };
  
  // Create a map to count matches for each language
  const matches = Object.keys(languageMarkers).reduce((acc, lang) => {
    acc[lang] = 0;
    return acc;
  }, {});
  
  // Lowercase and tokenize the text
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  
  // Count matches for each language
  for (const word of words) {
    for (const [lang, markers] of Object.entries(languageMarkers)) {
      if (markers.includes(word)) {
        matches[lang]++;
      }
    }
  }
  
  // Find the language with the most matches
  let bestMatch = 'en'; // Default to English
  let highestScore = 0;
  
  for (const [lang, score] of Object.entries(matches)) {
    if (score > highestScore) {
      highestScore = score;
      bestMatch = lang;
    }
  }
  
  return bestMatch;
};