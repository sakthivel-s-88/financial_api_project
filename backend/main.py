from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.routes.v1 import chat, analysis, vectordb
from backend.domain.rag import setup_rag_chain

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application startup and shutdown events."""
    print("Application startup...")
    app.state.rag_chain = setup_rag_chain()
    yield
    print("Application shutdown...")

app = FastAPI(
    title="Financial Analysis & RAG API",
    lifespan=lifespan
)

# Include all the API routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(vectordb.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Financial Analysis API!"}