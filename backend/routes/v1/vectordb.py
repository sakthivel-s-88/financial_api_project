import chromadb
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.config.settings import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME

router = APIRouter()

class DocumentResponse(BaseModel):
    id: str
    metadata: Optional[Dict[str, Any]] = None
    document: Optional[str] = None

class VectorDBViewResponse(BaseModel):
    collection_name: str
    count: int
    documents: List[DocumentResponse]

@router.get("/vectordb/view", response_model=VectorDBViewResponse, tags=["VectorDB Admin"])
def view_vectordb_contents():
    """Retrieves all documents and metadata from the ChromaDB collection."""
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = client.get_collection(name=CHROMA_COLLECTION_NAME)


        data = collection.get(include=["metadatas", "documents"])

        docs = [
            DocumentResponse(id=id, metadata=meta, document=doc)
            for id, meta, doc in zip(data['ids'], data['metadatas'], data['documents']) # pyright: ignore[reportArgumentType]
        ]

        return VectorDBViewResponse(
            collection_name=CHROMA_COLLECTION_NAME,
            count=collection.count(), 
            documents=docs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not access VectorDB: {e}")