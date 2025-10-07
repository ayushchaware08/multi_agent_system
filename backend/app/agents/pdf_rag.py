from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_groq.chat_models import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import fitz  # PyMuPDF
import os, time

CHROMA_DIR = os.getenv("CHROMA_DB_DIR", "data/vectorstore")
GROQ_KEY = os.getenv("GROQ_API_KEY")

def get_embeddings():
    """Get HuggingFace embeddings model"""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def chunk_text(text, doc_id):
    """Break text into chunks and create Document objects"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text)
    documents = []
    
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "doc_id": doc_id,
                "chunk_id": f"{doc_id}_chunk_{i}",
                "source": "pdf_upload"
            }
        )
        documents.append(doc)
    
    return documents

def ingest_pdf_to_chroma(pdf_path, doc_id):
    """Complete PDF ingestion pipeline: extract -> chunk -> embed -> store"""
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        if not text.strip():
            return {"status": "error", "message": "No text extracted from PDF"}
        
        # Chunk text into documents
        documents = chunk_text(text, doc_id)
        
        # Get embeddings and vectorstore
        embeddings = get_embeddings()
        vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
        
        # Add documents to vectorstore
        vectorstore.add_documents(documents)
        vectorstore.persist()
        
        return {
            "status": "success", 
            "message": f"Ingested {len(documents)} chunks for doc_id: {doc_id}",
            "chunks_count": len(documents)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Ingestion failed: {str(e)}"}

def get_rag_chain(doc_id=None):
    """Get RAG chain for querying, optionally filtered by doc_id"""
    embeddings = get_embeddings()
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    # Configure retriever with optional filtering
    search_kwargs = {"k": 5}
    if doc_id:
        search_kwargs["filter"] = {"doc_id": doc_id}
    
    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    # Only Groq LLM is supported
    if not GROQ_KEY:
        raise ValueError("GROQ_API_KEY environment variable is required")
    
    llm = ChatGroq(api_key=GROQ_KEY, temperature=0)
    
    chain = RetrievalQA.from_chain_type(
        llm=llm, 
        retriever=retriever,
        return_source_documents=True
    )
    return chain

def run_pdf_rag_query(query, doc_id=None):
    """Run RAG query against ingested PDFs"""
    try:
        chain = get_rag_chain(doc_id)
        
        start = time.time()
        response = chain.invoke({"query": query})
        duration = time.time() - start
        
        # Extract answer and source documents
        answer = response["result"]
        source_docs = response.get("source_documents", [])
        
        # Build trace with retrieved document info
        retrieved_docs = []
        for doc in source_docs:
            retrieved_docs.append({
                "doc_id": doc.metadata.get("doc_id"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "content_preview": doc.page_content[:100] + "..."
            })
        
        trace = {
            "retrieved_docs": retrieved_docs,
            "duration": duration,
            "retriever_filter": {"doc_id": doc_id} if doc_id else "all_docs"
        }
        
        return answer, trace
        
    except Exception as e:
        return f"RAG query failed: {str(e)}", {"error": str(e)}