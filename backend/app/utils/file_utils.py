import os
import shutil
from typing import List, Optional
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = ["pdf", "docx"]


def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.
    
    Args:
        filename (str): The filename
        
    Returns:
        str: The file extension (without the dot)
    """
    return Path(filename).suffix.lower().replace(".", "")


def is_valid_file_type(filename: str) -> bool:
    """
    Check if a file has an allowed extension.
    
    Args:
        filename (str): The filename
        
    Returns:
        bool: True if the file has an allowed extension, False otherwise
    """
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """
    Save an uploaded file to a destination path.
    
    Args:
        upload_file (UploadFile): The uploaded file
        destination (str): The destination path
        
    Returns:
        str: The path where the file was saved
    """
    try:
        # Check if file extension is allowed
        if not is_valid_file_type(upload_file.filename):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"File type not allowed. Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Save the file
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        logger.info(f"File saved at {destination}")
        return destination
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )


def delete_file(file_path: str) -> bool:
    """
    Delete a file.
    
    Args:
        file_path (str): The path of the file to delete
        
    Returns:
        bool: True if the file was deleted, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        else:
            logger.warning(f"File not found: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path (str): The path of the file
        
    Returns:
        int: The size of the file in bytes
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {str(e)}")
        return 0