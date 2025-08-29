from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from backend.config.settings import CHROMA_DB_PATH, GOOGLE_API_KEY, CHROMA_COLLECTION_NAME

def format_docs(docs: list[Document]) -> str:
    """Formats a list of documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def setup_rag_chain():
    """Sets up and returns the main RAG chain using Google Gemini."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set.")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
    
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH, 
        embedding_function=embedding_function,
        collection_name=CHROMA_COLLECTION_NAME
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt_template = """
    You are an expert financial assistant. Answer the question based ONLY on the following context.
    If the context does not contain the answer, state that you don't have enough information.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    rag_chain = (
        # THE FIX: Add the 'format_docs' function to the context pipeline
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("RAG chain with Gemini setup complete.")
    return rag_chain