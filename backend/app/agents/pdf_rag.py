from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_groq.chat_models import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from functools import lru_cache
import logging
import time
import fitz
import os

logger = logging.getLogger(__name__)

GROQ_KEY = os.getenv("GROQ_API_KEY")

# Global in-memory FAISS vector store
_vectorstore = None

# embedding
@lru_cache(maxsize=1)
def get_embeddings():
    """Get HuggingFace embeddings (compatible with FAISS)"""
    logger.info("🔄 Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        # model_name='all-MiniLM-L6-v2',
        model_name='paraphrase-MiniLM-L3-v2',
        model_kwargs={'device': 'cpu'}
    )
    logger.info("✅ Embedding model loaded")
    return embeddings

# pdf parse
def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def chunk_text(text, doc_id):
    """Split text into chunks with metadata"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    
    chunks = splitter.split_text(text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "doc_id": doc_id,
                "chunk_id": i,
                "source": "pdf_upload"
            }
        )
        documents.append(doc)
    
    return documents

# FAISS INGESTION
def ingest_pdf_to_chroma(pdf_path, doc_id):
    """
    Ingest PDF using FAISS vector store
    """
    global _vectorstore
    
    try:
        logger.info("="*60)
        logger.info(f"📄 Starting ingestion: {doc_id}")
        
        # Extract
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            return {"status": "error", "message": "No text found in PDF"}
        logger.info(f"✅ Extracted {len(text)} characters")
        
        # Chunk
        documents = chunk_text(text, doc_id)
        logger.info(f"✅ Created {len(documents)} chunks")
        
        # Get embeddings
        embeddings = get_embeddings()
        logger.info("✅ Embeddings ready")
        
        # Add to FAISS
        logger.info("📥 Adding to FAISS vectorstore...")
        
        if _vectorstore is None:
            logger.info("Creating new FAISS index...")
            _vectorstore = FAISS.from_documents(documents, embeddings)
            logger.info("✅ FAISS index created")
        else:
            logger.info("Adding to existing FAISS index...")
            _vectorstore.add_documents(documents)
            logger.info("✅ Documents added")
        
        logger.info("="*60)
        logger.info(f"✅ INGESTION COMPLETE")
        logger.info(f"📊 Total documents in FAISS: {_vectorstore.index.ntotal}")
        logger.info("="*60)
        
        return {
            "status": "success",
            "message": f"Successfully ingested {len(documents)} chunks",
            "chunks_count": len(documents)
        }
        
    except Exception as e:
        import traceback
        logger.error("="*60)
        logger.error(f"❌ INGESTION FAILED: {str(e)}")
        logger.error(traceback.format_exc())
        logger.error("="*60)
        return {"status": "error", "message": str(e)}


# RAG QUERY
def run_pdf_rag_query(query, doc_id=None):
    """
    Query the FAISS vector database with RAG
    """
    global _vectorstore
    
    try:
        logger.info("="*60)
        logger.info(f"🔍 RAG Query: '{query}'")
        
        if _vectorstore is None:
            logger.warning("⚠️ No documents uploaded yet")
            return "No documents have been uploaded yet. Please upload a PDF first.", {
                "error": "No documents in vectorstore"
            }
        
        logger.info(f"📚 FAISS index contains {_vectorstore.index.ntotal} documents")
        
        # Setup retriever
        if doc_id:
            logger.info(f"🔍 Filtering by doc_id: {doc_id}")
            retriever = _vectorstore.as_retriever(search_kwargs={"k": 20})
        else:
            retriever = _vectorstore.as_retriever(search_kwargs={"k": 5})
        
        # Setup LLM
        llm = ChatGroq(
            api_key=GROQ_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=2048,
            timeout=60.0,
            max_retries=2
        )
        
        # Create RAG chain
        logger.info("🔗 Building RAG chain...")
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
        
        # Execute query
        logger.info("🤖 Executing query...")
        start = time.time()
        response = chain.invoke({"query": query})
        duration = time.time() - start
        
        answer = response["result"]
        sources = response.get("source_documents", [])
        
        # Filter by doc_id if specified
        if doc_id:
            sources = [s for s in sources if s.metadata.get("doc_id") == doc_id]
            sources = sources[:5]
            logger.info(f"✅ Filtered to {len(sources)} documents")
        
        logger.info(f"✅ Retrieved {len(sources)} source documents")
        
        # Build trace
        trace = {
            "chunks_retrieved": len(sources),
            "duration_sec": round(duration, 2),
            "total_docs_in_index": _vectorstore.index.ntotal,
            "filter_applied": {"doc_id": doc_id} if doc_id else None,
            "sources": [
                {
                    "doc_id": s.metadata.get("doc_id"),
                    "chunk_id": s.metadata.get("chunk_id"),
                    "preview": s.page_content[:100] + "..."
                }
                for s in sources
            ]
        }
        
        logger.info("="*60)
        logger.info(f"✅ QUERY COMPLETE in {duration:.2f}s")
        logger.info("="*60)
        
        return answer, trace
        
    except Exception as e:
        import traceback
        logger.error("="*60)
        logger.error(f"❌ QUERY FAILED: {str(e)}")
        logger.error(traceback.format_exc())
        logger.error("="*60)
        return f"Query failed: {str(e)}", {"error": str(e)}
