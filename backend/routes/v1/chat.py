from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse, tags=["RAG Chat"])
async def handle_chat(request: Request, chat_request: ChatRequest):
    """Handles a user chat query by invoking the RAG chain."""
    rag_chain = request.app.state.rag_chain
    if not rag_chain:
        raise HTTPException(status_code=500, detail="RAG chain is not initialized.")
    
    try:
        answer = rag_chain.invoke(chat_request.query)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")