 # Multi-Agent System 🤖

A sophisticated multi-agent AI system that intelligently routes user queries to specialized agents for optimal answers. The system combines PDF processing, academic research, and web search capabilities with intelligent routing powered by Groq LLM.


## 🏢 Project Structure

```
multi_agent_system/
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # FastAPI application entry
│   │   ├── api/                # API route handlers
│   │   │   ├── ask.py          # Main query processing
│   │   │   ├── upload.py       # PDF upload & status
│   │   │   └── logs.py         # System logs
│   │   ├── agents/             # Specialized AI agents
│   │   │   ├── controller.py   # Intelligent routing
│   │   │   ├── pdf_rag.py      # PDF document processing
│   │   │   ├── arxiv_agent.py  # Academic paper search
│   │   │   └── web_search.py   # Web search & synthesis
│   │   └── utils/              # Shared utilities
│   │       ├── logging_utils.py # Decision logging
│   │       ├── security.py     # Upload validation
│   │       └── backoff_utils.py # Retry mechanisms
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   └── data/                   # Data storage
│       ├── uploads/            # Uploaded PDFs
│       └── vectorstore/        # ChromaDB storage
├── frontend/                   # Streamlit Frontend
│   └── streamlit_app.py        # User interface
├── logs/                       # System logs
│   └── decision_logs.jsonl     # Agent routing decisions
└── README.md                   # This file
```

## 🛠️ Technical Details

### Key Technologies

- **Backend Framework**: FastAPI (async/await, automatic OpenAPI docs)
- **Frontend**: Streamlit (rapid prototyping, file uploads)
- **LLM**: Groq (fast inference, multiple models)
- **Vector Database**: ChromaDB (persistent storage, similarity search)
- **Embeddings**: HuggingFace Transformers (local, no API costs)
- **PDF Processing**: PyMuPDF (fast, reliable text extraction)
- **Web Search**: SerpAPI (Google Search API)
- **Academic Search**: ArXiv API (open academic papers)

### Performance Optimizations

1. **Batch Processing**: Large PDFs processed in chunks to prevent hanging
2. **Async Processing**: Non-blocking API with background tasks
3. **Model Caching**: Embedding models cached for faster inference
4. **Connection Pooling**: Efficient database connections
5. **Retry Mechanisms**: Robust error handling with exponential backoff

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│    Backend       │───▶│   External      │
│   (Streamlit)   │    │   (FastAPI)      │    │   Services      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Controller    │
                    │   (Groq LLM)    │
                    └─────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  PDF RAG     │  │  ArXiv       │  │  Web Search  │
    │  Agent       │  │  Agent       │  │  Agent       │
    └──────────────┘  └──────────────┘  └──────────────┘
            │                 │                 │
            ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  ChromaDB    │  │  ArXiv API   │  │  SerpAPI     │
    │  Vector DB   │  │              │  │  (Google)    │
    └──────────────┘  └──────────────┘  └──────────────┘
```

### 🧠 Intelligent Agent Routing

The system employs a **Controller Agent** powered by Groq's LLM that intelligently routes queries to the most appropriate specialized agent:

1. **Rule-Based Routing** (Fast): Pre-defined patterns for common query types
2. **LLM-Based Routing** (Smart): Advanced decision making for complex queries
3. **User Preference Override**: Manual agent selection when needed

### 🔧 Core Agents

#### 1. PDF RAG Agent 📄
- **Purpose**: Answer questions about uploaded PDF documents
- **Technology**: LangChain + ChromaDB + HuggingFace Embeddings
- **Features**:
  - PDF text extraction using PyMuPDF
  - Intelligent text chunking with overlap
  - Batch processing for large documents (prevents hanging)
  - Vector similarity search with metadata filtering
  - Document-specific or global PDF search

#### 2. ArXiv Research Agent 📚
- **Purpose**: Find and analyze recent academic papers
- **Technology**: ArXiv API + Groq LLM analysis
- **Features**:
  - Smart query preprocessing and field-specific search
  - Recent paper filtering (18-month window)
  - Comprehensive paper analysis with structured output
  - Research trend identification
  - Direct ArXiv links and paper recommendations

#### 3. Web Search Agent 🌐
- **Purpose**: Current information and general web queries
- **Technology**: SerpAPI (Google Search) + Groq LLM synthesis
- **Features**:
  - Real-time Google search results
  - Multi-source information synthesis
  - Structured answer generation
  - Source attribution and transparency

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- API Keys:
  - [Groq API Key](https://console.groq.com) (Required)
  - [SerpAPI Key](https://serpapi.com) (Optional - for web search)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ayushchaware08/multi_agent_system.git
   cd multi_agent_system
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

5. **Create required directories**
   ```bash
   mkdir -p data/uploads data/vectorstore logs
   ```

### Running the System

#### Option 1: Full System (Recommended)

1. **Start Backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend** (New terminal)
   ```bash
   cd frontend
   streamlit run streamlit_app.py
   ```

3. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

#### Option 2: API Only
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📝 Environment Configuration

Create a `.env` file in the `backend` directory:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional but recommended
SERPAPI_API_KEY=your_serpapi_key_here

# System Configuration
CHROMA_DB_DIR=data/vectorstore
MAX_UPLOAD_MB=10
LOG_FILE=logs/decision_logs.jsonl
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Optional
ARXIV_API_EMAIL=your_email@example.com
```

## 🔗 API Documentation

### Core Endpoints

#### 1. Query Processing
```http
POST /ask/
Content-Type: application/json

{
  "text": "What are recent developments in AI safety?",
  "pdf_doc_id": "optional_document_id",
  "prefer_agent": "ARXIV"  // Optional: PDF_RAG, ARXIV, WEB_SEARCH
}

Response:
{
  "answer": "Detailed AI-generated response...",
  "agents_used": "ARXIV",
  "rationale": "User asked about recent papers",
  "trace": {
    "papers": [...],
    "query": "...",
    "llm_duration": 2.34
  }
}
```

#### 2. PDF Upload & Processing
```http
POST /upload/
Content-Type: multipart/form-data

FormData: file=@document.pdf

Response:
{
  "status": "accepted",
  "doc_id": "upload_1703123456",
  "filename": "document.pdf",
  "check_status": "/upload/status/upload_1703123456"
}
```

#### 3. Upload Status Check
```http
GET /upload/status/{doc_id}

Response:
{
  "status": "completed",  // processing, completed, failed
  "message": "Successfully ingested 45 chunks",
  "chunks_count": 45,
  "completed_at": 1703123456
}
```

#### 4. System Health
```http
GET /health

Response:
{
  "status": "healthy",
  "embedding_model": "loaded"
}
```

### Additional Endpoints

- `GET /upload/list` - List all uploaded documents
- `DELETE /upload/{doc_id}` - Delete uploaded document
- `GET /logs/` - View system decision logs
- `DELETE /upload/clear-failed` - Clear failed uploads

## 🎯 Usage Examples

### 1. Academic Research
```
Query: "recent papers on transformer architectures in 2024"
→ Routes to ArXiv Agent
→ Returns: Latest papers with analysis and recommendations
```

### 2. PDF Document Analysis
```
1. Upload PDF via frontend or API
2. Query: "What are the main conclusions of the uploaded document?"
→ Routes to PDF RAG Agent
→ Returns: Document-specific insights with source citations
```

### 3. Current Information
```
Query: "What happened in the tech industry this week?"
→ Routes to Web Search Agent  
→ Returns: Latest news with multiple source synthesis
```

### 4. Mixed Queries
```
Query: "Compare recent AI safety papers with regulations mentioned in my uploaded policy document"
→ Controller intelligently routes to multiple agents
→ Returns: Comprehensive analysis from multiple sources
```
## 🔧 Advanced Configuration

### Custom Model Configuration

The system supports various Groq models. Update in your agents:

```python
# In agents/*.py files
ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.3-70b-versatile",  # Options: llama-3.1-70b-versatile, mixtral-8x7b-32768
    temperature=0.3,
    max_tokens=2048,
    timeout=60.0
)
```

### Vector Database Tuning

ChromaDB settings in `pdf_rag.py`:

```python
# Retrieval settings
search_kwargs = {
    "k": 5,  # Number of similar chunks to retrieve
    "filter": {"doc_id": doc_id}  # Filter by document
}

# Chunking settings
RecursiveCharacterTextSplitter(
    chunk_size=500,      # Characters per chunk
    chunk_overlap=50,    # Overlap between chunks
    length_function=len
)
```

## 🚀 Deployment

### Docker Deployment (Recommended)

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - SERPAPI_API_KEY=${SERPAPI_API_KEY}

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - API_ROOT=http://backend:8000
```

### Cloud Deployment Options

#### 1. AWS EC2/ECS
- Use the Docker setup above
- Configure environment variables in ECS task definitions
- Set up persistent storage for ChromaDB data

#### 2. Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/multi-agent-system
gcloud run deploy --image gcr.io/PROJECT_ID/multi-agent-system --platform managed
```

#### 3. Heroku
```bash
# Add Procfile
echo "web: uvicorn app.main:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Fix transformers/sentence-transformers conflicts
pip uninstall sentence-transformers transformers torch -y
pip install sentence-transformers==2.7.0 transformers==4.41.0
```

#### 2. ChromaDB Issues
```bash
# Clear ChromaDB data
rm -rf data/vectorstore/*

# Restart with fresh database
```

#### 3. Memory Issues
```python
# Reduce batch size in pdf_rag.py
batch_size = 5  # Instead of 10

# Reduce embedding dimensions
dimension = 256  # Instead of 384
```

#### 4. API Timeouts
```python
# Increase timeout in agents
timeout=120.0  # Instead of 60.0
```

### Debug Mode

Enable debug logging:

```python
# In main.py
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Monitoring & Analytics

### Decision Logs
The system logs all routing decisions to `logs/decision_logs.jsonl`:

```json
{
  "timestamp": 1703123456,
  "decision": "ARXIV",
  "rationale": "User asked about recent papers",
  "input": "latest AI developments",
  "trace": {...}
}
```

### Health Monitoring
- `/health` endpoint for system status
- Embedding model loading verification
- API key validation

### Performance Metrics
Access via `/logs/` endpoint:
- Query processing times
- Agent routing statistics
- Error rates and types

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit a pull request

### Adding New Agents

1. Create agent file in `backend/app/agents/`
2. Implement the main function following the pattern:
   ```python
   def run_new_agent(query):
       # Agent logic here
       return answer, trace
   ```
3. Add routing logic in `controller.py`
4. Register in `ask.py` API endpoint

### Code Style
- Follow PEP 8 for Python code
- Use type hints where possible
- Add comprehensive docstrings
- Include error handling

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links & Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [SerpAPI Documentation](https://serpapi.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🆘 Support

For issues and questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/ayushchaware08/multi_agent_system/issues)
3. Create a new issue with:
   - System information
   - Error messages
   - Steps to reproduce
   - Expected vs actual behavior

---

**Made with ❤️ by [ayushchaware08](https://github.com/ayushchaware08)**