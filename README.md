# multi_agent_system
```
multi_agent_system/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry
│   │   ├── api/                    # routes
│   │   │   ├── ask.py
│   │   │   ├── upload.py
│   │   │   ├── logs.py
│   │   ├── agents/                 # agent implementations
│   │   │   ├── controller.py
│   │   │   ├── pdf_rag.py
│   │   │   ├── web_search.py
│   │   │   └── arxiv_agent.py
│   │   ├── ingestion/              # ingestion utilities
│   │   │   ├── ingest_nebula.py
│   │   │   └── chunking.py
│   │   ├── utils/
│   │   │   ├── logging_utils.py
│   │   │   ├── backoff_utils.py
│   │   │   └── security.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   └── nebula_pdfs/                 # put 5 sample NebulaByte PDFs here
│
├── logs/
│   └── decision_logs.jsonl
│
└── README.md
```