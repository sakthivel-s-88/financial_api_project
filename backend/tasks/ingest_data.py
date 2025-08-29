from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.config.settings import TICKERS, CHROMA_DB_PATH, GOOGLE_API_KEY, CHROMA_COLLECTION_NAME
from backend.domain.news import fetch_financial_documents

def build_vector_store(documents):
    #Splits documents, creates embeddings, and stores them in ChromaDB
    print("Splitting documents and building vector store...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
    
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embedding_function,
        persist_directory=CHROMA_DB_PATH,
        collection_name=CHROMA_COLLECTION_NAME
    )
    print(f"Vector store built successfully in collection '{CHROMA_COLLECTION_NAME}'.")

if __name__ == '__main__':
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")
    print("Starting data ingestion process...")
    financial_documents = fetch_financial_documents(TICKERS)
    if financial_documents:
        build_vector_store(financial_documents)
    else:
        print("No documents were loaded. Vector store not built.")