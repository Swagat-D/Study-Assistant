import os
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
import logging

from fastapi import UploadFile, HTTPException, status
import fitz  # PyMuPDF
import docx

from app.core.config import settings
from app.utils.text_utils import chunk_text
from app.utils.file_utils import save_upload_file, get_file_extension

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Service for processing uploaded documents and extracting text content.
    Supports PDF and DOCX formats.
    """

    @staticmethod
    async def process_document(
        file: UploadFile, 
        user_id: str,
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process an uploaded document file and extract its text content.
        
        Args:
            file: The uploaded file object
            user_id: ID of the user who uploaded the document
            save_path: Optional path to save the file
            
        Returns:
            Dictionary with document metadata and extracted text
        """
        # Check file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024 * 1024)}MB"
            )
        
        # Get file extension
        file_extension = get_file_extension(file.filename)
        
        if file_extension.lower() not in ["pdf", "docx"]:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported file format. Only PDF and DOCX are supported."
            )
        
        # Create save path if not provided
        if not save_path:
            save_path = os.path.join(
                settings.UPLOAD_DIRECTORY,
                user_id,
                Path(file.filename).name
            )
        
        # Save the file
        file_path = await save_upload_file(file, save_path)
        
        # Extract text content based on file type
        if file_extension.lower() == "pdf":
            text_content, metadata = DocumentProcessor._extract_pdf_text(file_path)
        elif file_extension.lower() == "docx":
            text_content, metadata = DocumentProcessor._extract_docx_text(file_path)
        else:
            text_content, metadata = "", {}
        
        # Chunk the text
        chunks = chunk_text(
            text_content, 
            chunk_size=settings.CHUNK_SIZE, 
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        # Create document result
        document_data = {
            "name": Path(file.filename).name,
            "file_path": file_path,
            "file_type": file_extension.lower(),
            "file_size": file_size,
            "num_pages": metadata.get("num_pages", 1),
            "text_content": text_content,
            "metadata": metadata,
            "chunks": [{"text": chunk, "chunk_index": i} for i, chunk in enumerate(chunks)],
        }
        
        return document_data

    @staticmethod
    def _extract_pdf_text(file_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text content and metadata from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (text_content, metadata)
        """
        try:
            document = fitz.open(file_path)
            
            # Extract metadata
            metadata = {
                "title": document.metadata.get("title", ""),
                "author": document.metadata.get("author", ""),
                "subject": document.metadata.get("subject", ""),
                "keywords": document.metadata.get("keywords", ""),
                "num_pages": len(document),
            }
            
            # Extract text from each page
            text_content = ""
            pages_content = []
            
            for page_index, page in enumerate(document):
                text = page.get_text()
                pages_content.append({
                    "page_number": page_index + 1,
                    "text": text
                })
                text_content += text + "\n\n"
            
            metadata["pages"] = pages_content
            
            return text_content, metadata
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Failed to process PDF file: {str(e)}"
            )

    @staticmethod
    def _extract_docx_text(file_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text content and metadata from a Word document.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Tuple of (text_content, metadata)
        """
        try:
            doc = docx.Document(file_path)
            
            # Extract metadata
            metadata = {
                "title": "",
                "author": "",
                "subject": "",
                "keywords": "",
                "num_pages": None,  # DOCX doesn't have a straightforward way to get page count
            }
            
            # Try to get properties if available
            try:
                core_properties = doc.core_properties
                metadata["title"] = core_properties.title or ""
                metadata["author"] = core_properties.author or ""
                metadata["subject"] = core_properties.subject or ""
                metadata["keywords"] = core_properties.keywords or ""
            except:
                pass  # Ignore if properties aren't available
            
            # Extract text from paragraphs
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            text_content = "\n\n".join(paragraphs)
            
            # Estimate number of pages (very rough)
            # Assuming ~3000 characters per page
            est_pages = max(1, len(text_content) // 3000)
            metadata["num_pages"] = est_pages
            
            return text_content, metadata
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Failed to process Word document: {str(e)}"
            )


# Create a singleton instance
document_processor = DocumentProcessor()