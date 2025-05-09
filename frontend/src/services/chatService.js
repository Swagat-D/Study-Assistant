import api from './api';

const chatService = {
  /**
   * Send a chat message to the server for processing
   * @param {string} message - The user's message
   * @param {string} documentId - The document ID (optional)
   * @param {Array} conversationHistory - Previous messages for context
   * @returns {Promise} - Promise with the AI response
   */
  sendMessage: async (message, documentId = null, conversationHistory = []) => {
    try {
      const payload = {
        message,
        documentId,
        conversationHistory
      };
      
      const response = await api.post('/chat/message', payload);
      return response.data;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  },
  
  /**
   * Get chat history for a specific document
   * @param {string} documentId - The document ID
   * @returns {Promise} - Promise with the chat history
   */
  getChatHistory: async (documentId) => {
    try {
      const response = await api.get(`/chat/history/${documentId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching chat history for document ${documentId}:`, error);
      throw error;
    }
  },
  
  /**
   * Save chat history to the server
   * @param {string} documentId - The document ID
   * @param {Array} messages - The chat messages to save
   * @returns {Promise} - Promise with the save result
   */
  saveChatHistory: async (documentId, messages) => {
    try {
      const payload = {
        documentId,
        messages
      };
      
      const response = await api.post('/chat/history/save', payload);
      return response.data;
    } catch (error) {
      console.error(`Error saving chat history for document ${documentId}:`, error);
      throw error;
    }
  },
  
  /**
   * Export chat transcript as a file
   * @param {string} documentId - The document ID
   * @param {string} format - Export format (pdf, txt, etc.)
   * @returns {Promise} - Promise with the export result
   */
  exportChatTranscript: async (documentId, format = 'pdf') => {
    try {
      const response = await api.get(`/chat/export/${documentId}?format=${format}`, {
        responseType: 'blob'
      });
      
      // Create a download link and trigger it
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `chat-transcript-${documentId}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      return true;
    } catch (error) {
      console.error(`Error exporting chat transcript for document ${documentId}:`, error);
      throw error;
    }
  }
};

export default chatService;