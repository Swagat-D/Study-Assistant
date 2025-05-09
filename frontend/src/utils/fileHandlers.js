import * as pdfjsLib from 'pdfjs-dist';
import { Document, Packer, Paragraph, TextRun } from 'docx';

// Set the PDF.js worker source
pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

/**
 * Extract text content from a PDF file
 * @param {File} file - The PDF file
 * @returns {Promise<Object>} - Promise with the extracted text and metadata
 */
export const extractPdfText = async (file) => {
  try {
    // Get the PDF file data as an ArrayBuffer
    const arrayBuffer = await file.arrayBuffer();
    
    // Load the PDF document
    const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
    const pdf = await loadingTask.promise;
    
    // Get document metadata
    const metadata = await pdf.getMetadata().catch(() => ({}));
    
    // Extract text from each page
    const numPages = pdf.numPages;
    const pages = [];
    
    for (let i = 1; i <= numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map(item => item.str).join(' ');
      
      pages.push({
        pageNumber: i,
        text: pageText
      });
    }
    
    return {
      text: pages.map(page => page.text).join(' '),
      pages,
      metadata: metadata.info || {},
      numPages
    };
  } catch (error) {
    console.error('Error extracting text from PDF:', error);
    throw new Error('Failed to extract text from PDF');
  }
};

/**
 * Extract text content from a Word document
 * @param {File} file - The Word document file
 * @returns {Promise<Object>} - Promise with the extracted text and metadata
 */
export const extractDocxText = async (file) => {
  try {
    // Get the docx file data as an ArrayBuffer
    const arrayBuffer = await file.arrayBuffer();
    
    // Load the Word document
    const doc = new Document(arrayBuffer);
    
    // Get document content
    const content = await doc.getText();
    
    // Extract document properties if available
    const properties = doc.getProperties() || {};
    
    return {
      text: content,
      metadata: {
        title: properties.title || '',
        author: properties.creator || '',
        createdAt: properties.createdAt || new Date(),
        modifiedAt: properties.modifiedAt || new Date()
      }
    };
  } catch (error) {
    console.error('Error extracting text from Word document:', error);
    throw new Error('Failed to extract text from Word document');
  }
};

/**
 * Create a new Word document with the given text
 * @param {String} text - Text content to include
 * @param {String} filename - Name for the saved file
 * @returns {Promise<Blob>} - Promise with the generated document as a Blob
 */
export const createWordDocument = async (text, filename = 'document.docx') => {
  // Create a new document
  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          new Paragraph({
            children: [
              new TextRun(text)
            ]
          })
        ]
      }
    ]
  });
  
  // Generate the document as a blob
  const blob = await Packer.toBlob(doc);
  
  // Create a download link and trigger it
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  
  return blob;
};

/**
 * Validate if a file is of an allowed type
 * @param {File} file - The file to validate
 * @param {Array} allowedTypes - Array of allowed MIME types
 * @returns {Boolean} - Whether the file is valid
 */
export const validateFileType = (file, allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']) => {
  return allowedTypes.includes(file.type);
};

/**
 * Format file size in a human-readable format
 * @param {Number} bytes - File size in bytes
 * @returns {String} - Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * Get a file extension from a filename
 * @param {String} filename - The filename
 * @returns {String} - The file extension
 */
export const getFileExtension = (filename) => {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
};

/**
 * Check if a file is a PDF
 * @param {File} file - The file to check
 * @returns {Boolean} - Whether the file is a PDF
 */
export const isPdf = (file) => {
  return file.type === 'application/pdf';
};

/**
 * Check if a file is a Word document
 * @param {File} file - The file to check
 * @returns {Boolean} - Whether the file is a Word document
 */
export const isDocx = (file) => {
  return file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
};

/**
 * Create a thumbnail preview for a document 
 * @param {File} file - The document file
 * @returns {Promise<String>} - Promise with a data URL for the thumbnail
 */
export const createDocumentThumbnail = async (file) => {
  if (isPdf(file)) {
    try {
      const arrayBuffer = await file.arrayBuffer();
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      const pdf = await loadingTask.promise;
      const page = await pdf.getPage(1);
      
      // Create a canvas to render the PDF page
      const viewport = page.getViewport({ scale: 0.5 });
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      
      // Render the PDF page on the canvas
      await page.render({
        canvasContext: context,
        viewport: viewport
      }).promise;
      
      // Convert the canvas to a data URL
      return canvas.toDataURL('image/png');
    } catch (error) {
      console.error('Error creating PDF thumbnail:', error);
      return null;
    }
  } else {
    // For Word documents and other files, return a generic thumbnail
    return null;
  }
};

/**
 * Read a file and return its contents as text
 * @param {File} file - The file to read
 * @returns {Promise<String>} - Promise with the file contents as text
 */
export const readFileAsText = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (event) => {
      resolve(event.target.result);
    };
    
    reader.onerror = (error) => {
      reject(error);
    };
    
    reader.readAsText(file);
  });
};

/**
 * Read a file and return its contents as an array buffer
 * @param {File} file - The file to read
 * @returns {Promise<ArrayBuffer>} - Promise with the file contents as an array buffer
 */
export const readFileAsArrayBuffer = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (event) => {
      resolve(event.target.result);
    };
    
    reader.onerror = (error) => {
      reject(error);
    };
    
    reader.readAsArrayBuffer(file);
  });
};