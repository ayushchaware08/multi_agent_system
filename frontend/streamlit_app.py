import streamlit as st
import requests
import os
import time

API_ROOT = os.getenv("API_ROOT", "http://localhost:8000")

st.title("Multi-Agent Search")
st.text("Ask questions, find research papers, upload PDFs, and get answers from multiple agents!")

# st.sidebar.header("Upload PDF (NebulaByte demo)")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    
    try:
        # Upload PDF
        with st.spinner("📤 Uploading PDF..."):
            resp = requests.post(f"{API_ROOT}/upload/", files=files, timeout=100)
            resp.raise_for_status()
        
        data = resp.json()
        doc_id = data.get("doc_id")
        
        st.success(f"✅ Uploaded: {data.get('filename')}")
        st.info(f"📄 Doc ID: `{doc_id}`")
        
        # Show processing status
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        max_wait = 120  # Wait up to 2 minutes
        for i in range(max_wait):
            try:
                status_resp = requests.get(f"{API_ROOT}/upload/status/{doc_id}", timeout=5)
                status_data = status_resp.json()
                
                current_status = status_data.get("status")
                message = status_data.get("message", "Processing...")
                
                if current_status == "processing":
                    progress_bar.progress(25)
                    status_placeholder.info(f"⏳ {message}")
                elif current_status == "embedding":
                    progress_bar.progress(50)
                    status_placeholder.info(f"🔄 {message}")
                elif current_status == "completed":
                    progress_bar.progress(100)
                    chunks = status_data.get("chunks_count", 0)
                    status_placeholder.success(f"✅ Ready to query! ({chunks} chunks created)")
                    # Store doc_id in session state for queries
                    st.session_state['current_doc_id'] = doc_id
                    break
                elif current_status == "failed":
                    progress_bar.progress(0)
                    status_placeholder.error(f"❌ Failed: {message}")
                    break
                
                time.sleep(1)
                
            except Exception as e:
                status_placeholder.warning(f"⏳ Processing... ({i}s)")
                time.sleep(1)
        else:
            status_placeholder.warning("⚠️ Processing is taking longer than expected. Check back later.")
        
    except requests.exceptions.Timeout:
        st.error("⏱️ Upload timeout (server may still be processing)")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Upload failed: {e}")


# add simple architecture of the system
st.sidebar.markdown("""
## System Architecture
- Frontend: Streamlit app for user interaction  
- Backend: FastAPI server with multiple agents
- Agents: Arxiv search, PDF RAG, Web search (SerpAPI)
- LLM: Groq LLM for routing and responses
- Vector Store: FAISS for PDF Vector embeddings
""")

query = st.text_input("Enter your question", "")

# search suggestions
st.info("**Suggestions:** recent papers on AI safety | summarize the uploaded PDF | find papers about reinforcement learning"
            " | what are the latest developments in AI in 2025")

if st.button("Ask"):
    st.write(f"Query: {query}")  # Debugging line to show the query
    if not query:
        st.warning("Please enter a query")
    else:
        payload = {"text": query}
        
        try:
            # Add spinner and timeout
            with st.spinner("🔍 Processing your query... "):
                r = requests.post(
                    f"{API_ROOT}/ask/", 
                    json=payload,
                    timeout=120  # 2 minute timeout
                )
                r.raise_for_status()
                
            try:
                data = r.json()
                
                st.subheader("Answer")
                
                with st.expander("Agents used & rationale", expanded=True):
                    st.markdown(f"**Agent:** {data.get('agents_used', 'Unknown')}")
                    st.markdown(f"**Rationale:** {data.get('rationale', 'No rationale')}")
                st.write(data.get("answer", "No answer returned"))
                
                if data.get("trace"):
                    st.subheader("Trace / retrieved docs")
                    st.json(data.get("trace"))
                    
            except ValueError:
                st.error("Backend returned non-JSON response: " + r.text[:500])
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out after 3 minutes. The PDF might be too large or the server is overloaded.")
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request failed: {e}")

# Show search suggestions
# st.info("**Suggestions:** recent papers on AI safety | summarize the uploaded PDF | find papers about reinforcement learning")
