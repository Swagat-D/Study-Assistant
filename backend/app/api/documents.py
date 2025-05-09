from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas import document as schemas
from app.core.security import get_current_active_user
from app.services.document_processor import document_processor
from app.services.embedding import embedding_service
from app.utils.vector_store import vector_store

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post("/upload", response_model=schemas.DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document for processing and extraction.
    """
    # Process the document
    try:
        document_data = await document_processor.process_document(file, str(user.id))
        
        # Create document record in database
        db_document = models.Document(
            name=document_data["name"],
            file_path=document_data["file_path"],
            file_type=document_data["file_type"],
            file_size=document_data["file_size"],
            num_pages=document_data["num_pages"],
            text_content=document_data["text_content"],
            metadata=document_data["metadata"],
            is_processed=True,
            owner_id=user.id
        )
        
        db.add(db_document)
        db.flush()
        
        # Create document chunks records
        for chunk_data in document_data["chunks"]:
            db_chunk = models.DocumentChunk(
                document_id=db_document.id,
                chunk_index=chunk_data["chunk_index"],
                text_content=chunk_data["text"],
                page_number=chunk_data.get("page_number")
            )
            db.add(db_chunk)
        
        db.commit()
        
        # Generate embeddings for chunks in the background
        # In a production system, this should be done asynchronously
        chunk_texts = [chunk["text"] for chunk in document_data["chunks"]]
        embeddings = embedding_service.generate_embeddings(chunk_texts)
        
        # Update chunks with embeddings
        db_chunks = db.query(models.DocumentChunk).filter(
            models.DocumentChunk.document_id == db_document.id
        ).all()
        
        for i, db_chunk in enumerate(db_chunks):
            if i < len(embeddings):
                # Store embedding in vector store
                vector_store.add_embedding(
                    document_id=str(db_document.id),
                    chunk_id=str(db_chunk.id),
                    text=db_chunk.text_content,
                    embedding=embeddings[i],
                    metadata={
                        "chunk_index": db_chunk.chunk_index,
                        "page_number": db_chunk.page_number
                    }
                )
                
                # Update chunk with binary embedding
                db_chunk.embedding = embedding_service.serialize_embedding(embeddings[i])
                db.add(db_chunk)
        
        db.commit()
        
        return schemas.DocumentUploadResponse(
            id=db_document.id,
            name=db_document.name,
            file_type=db_document.file_type,
            file_size=db_document.file_size,
            num_pages=db_document.num_pages,
            is_processed=db_document.is_processed,
            message="Document uploaded and processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@router.get("/", response_model=List[schemas.Document])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all documents for the current user.
    """
    documents = db.query(models.Document).filter(
        models.Document.owner_id == user.id
    ).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=schemas.DocumentWithChunks)
async def get_document(
    document_id: UUID,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID.
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document by ID.
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Remove embeddings from vector store
    vector_store.delete_document(str(document_id))
    
    # Delete document from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/search", response_model=List[schemas.DocumentSearchResult])
async def search_documents(
    search_query: schemas.DocumentSearchQuery,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search documents using vector similarity.
    """
    # Generate embedding for the query
    query_embedding = embedding_service.generate_embeddings([search_query.query])[0]
    
    # Search vector store
    document_ids = []
    if search_query.document_id:
        document_ids.append(str(search_query.document_id))
        
        # Check if document belongs to user
        document = db.query(models.Document).filter(
            models.Document.id == search_query.document_id,
            models.Document.owner_id == user.id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
    else:
        # Get all document IDs for the user
        documents = db.query(models.Document.id).filter(
            models.Document.owner_id == user.id
        ).all()
        document_ids = [str(doc.id) for doc in documents]
    
    # Perform search
    results = vector_store.search(
        query_embedding=query_embedding,
        document_ids=document_ids,
        top_k=search_query.max_results
    )
    
    # Format and return results
    search_results = []
    for result in results:
        # Get document info
        document = db.query(models.Document).filter(
            models.Document.id == UUID(result["document_id"])
        ).first()
        
        if document:
            search_results.append(
                schemas.DocumentSearchResult(
                    document_id=document.id,
                    document_name=document.name,
                    chunks=result["chunks"],
                    score=result["score"]
                )
            )
    
    return search_results