import api from './api';

const documentService = {
  /**
   * Upload a document to the server
   * @param {File} file - The file to upload
   * @returns {Promise} - Promise with the upload result
   */
  uploadDocument: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    }
  },
  
  /**
   * Get all documents for the current user
   * @returns {Promise} - Promise with the documents
   */
  getDocuments: async () => {
    try {
      const response = await api.get('/documents');
      return response.data;
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  },
  
  /**
   * Get a specific document by ID
   * @param {string} documentId - The document ID
   * @returns {Promise} - Promise with the document
   */
  getDocumentById: async (documentId) => {
    try {
      const response = await api.get(`/documents/${documentId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching document ${documentId}:`, error);
      throw error;
    }
  },
  
  /**
   * Delete a document by ID
   * @param {string} documentId - The document ID to delete
   * @returns {Promise} - Promise with the delete result
   */
  deleteDocument: async (documentId) => {
    try {
      const response = await api.delete(`/documents/${documentId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting document ${documentId}:`, error);
      throw error;
    }
  },
  
  /**
   * Generate a summary for a document
   * @param {string} documentId - The document ID
   * @param {Object} options - Summary options (type, length, etc.)
   * @returns {Promise} - Promise with the summary
   */
  generateSummary: async (documentId, options = {}) => {
    try {
      const response = await api.post(`/documents/${documentId}/summary`, options);
      return response.data;
    } catch (error) {
      console.error(`Error generating summary for document ${documentId}:`, error);
      throw error;
    }
  },
  
  /**
   * Generate flashcards for a document
   * @param {string} documentId - The document ID
   * @param {Object} options - Flashcard options (number, difficulty, etc.)
   * @returns {Promise} - Promise with the flashcards
   */
  generateFlashcards: async (documentId, options = {}) => {
    try {
      const response = await api.post(`/documents/${documentId}/flashcards`, options);
      return response.data;
    } catch (error) {
      console.error(`Error generating flashcards for document ${documentId}:`, error);
      throw error;
    }
  },
  
  /**
   * Generate a quiz for a document
   * @param {string} documentId - The document ID
   * @param {Object} options - Quiz options (type, number of questions, etc.)
   * @returns {Promise} - Promise with the quiz
   */
  generateQuiz: async (documentId, options = {}) => {
    try {
      const response = await api.post(`/documents/${documentId}/quiz`, options);
      return response.data;
    } catch (error) {
      console.error(`Error generating quiz for document ${documentId}:`, error);
      throw error;
    }
  }
};

export default documentService;